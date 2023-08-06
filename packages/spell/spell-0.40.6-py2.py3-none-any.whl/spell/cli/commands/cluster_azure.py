import click
import uuid
import json
import requests
import subprocess
import random
import time
import re

from halo import Halo

from spell.cli.exceptions import (
    api_client_exception_handler,
    ExitException,
)
from spell.cli.utils import (
    cluster_utils,
    sentry,
    get_star_spinner_frames,
)

CLUSTER_VERSION = 1
DEFAULT_REGION = "westus2"
CONTAINER_NAME = "spell-blob-container"
VNET_NAME = "spell-vnet"
SUBNET_NAME = "spell-subnet"
SECURITY_GROUP_NAME = "spell-security-group"
NUM_RETRIES = 5  # Retries for getting sp/app
# SSH, Docker Daemon, and Jupyter respectively
INGRESS_PORTS = [22, 2376, 9999]

required_permissions = [
    "Microsoft.Compute/*",
    "Microsoft.Network/*",
    "Microsoft.Storage/*",
    "Microsoft.Support/*",
    "Microsoft.Authorization/*/read",
    "Microsoft.Resources/deployments/*",
    "Microsoft.Resources/subscriptions/resourceGroups/read",
]


@click.command(name="az", short_help="Sets up an Azure VNet as a Spell cluster", hidden=True)
@click.pass_context
@click.option(
    "-n", "--name", "name", help="This will be used by Spell for you to identify the cluster"
)
@click.option(
    "-r",
    "--resource-group",
    "resource_group_name",
    help="This will be the name of the Resource Group Spell will create and "
    "store all its resources in within your Azure account",
    default="rg-spell",
)
@click.option(
    "-s",
    "--service-principal",
    "service_principal_name",
    help="Command to name your Service Principal",
    default="sp-spell",
)
def create_azure(ctx, name, resource_group_name, service_principal_name):
    """
    This command creates an Azure VNet of your choosing as an external Spell cluster.
    This will let your organization create runs in that VNet, so your data never leaves
    your VNet. You create an Azure Blob Container of your choosing for all run outputs to be written to.
    After this cluster is set up you will be able to select the types and number of machines
    you would like Spell to create in this cluster.
    """

    # Verify the owner is the admin of an org
    spell_client = ctx.obj["client"]
    cluster_utils.validate_org_perms(spell_client, ctx.obj["owner"])

    try:
        from azure.graphrbac import GraphRbacManagementClient
        from azure.mgmt.resource import ResourceManagementClient
        from azure.mgmt.authorization import AuthorizationManagementClient
        from azure.mgmt.resource.subscriptions import SubscriptionClient
        from azure.mgmt.storage import StorageManagementClient
        from azure.mgmt.storage.models import StorageAccountCreateParameters, Sku, SkuName, Kind
        from spell.cli.utils.azure_credential_wrapper import AzureIdentityCredentialAdapter
        from azure.core.exceptions import ClientAuthenticationError
        from azure.storage.blob import BlobServiceClient
        from azure.mgmt.network import NetworkManagementClient
        from azure.identity import DefaultAzureCredential

    except ImportError:
        click.echo("Please `pip install --upgrade 'spell[cluster-azure]'` and rerun this command")
        return

    click.echo(
        """This command will help you
        - Select a region to create resources in and a subscription for billing
        - Create an App and Service Principal
        - Create a Resource group in the specified region to manage your resources
        - Assign a role to your Service Principal that allows Spell to spin up and
            down machines and access your Blobs
        - Create a uniquely-named storage account
        - Set up an Blob Container to store your run outputs in
        - Set up a VNet and Subnet which Spell will spin up workers in to run your jobs
        - Set up a Security Group providing Spell SSH and Docker access to workers """
    )

    # Create Credentials
    """
    DefaultAzureCredential is the new credential that Microsoft recommends. However,
    this credential only works for packages with the prefix `azure-mgmt`.
    The hope is that eventually everything will use this credential. Until that happens,
    they recommend using the wrapper AzureIdentityCredentialAdapter().

    The resource id argument supplied to the wrapper dictates which token is returned. Different
    APIs require different tokens.

    credentials (Default Azure Credential): Azure's new credential that uses the azure identity
    library.
    management_creds (wrapper/default resource id): used for tenant id and authorization client
    graph_rbac_creds (wrapper/graph.windows.net resource id): used to create app/sp - library is
    being deprecated and will eventually use the following credential
    microsoft_graph_creds (wrapper/graph.microsoft.com resource id): This uses the new Microsoft
    Graph API to set client secret.

    https://docs.microsoft.com/en-us/azure/developer/python/azure-sdk-authenticate?tabs=cmd
    """
    # TODO(sruthi): Figure out a better way to authenticate
    try:
        credentials = DefaultAzureCredential(
            exclude_environment_credential=True,
            exclude_managed_identity_credential=True,
            exclude_visual_studio_code_credential=True,
            exclude_shared_token_cache_credential=True,
        )
        management_cred = AzureIdentityCredentialAdapter()
        management_cred.set_token()
        graph_rbac_creds = AzureIdentityCredentialAdapter(resource_id="https://graph.windows.net/")
        graph_rbac_creds.set_token()
        microsoft_graph_creds = AzureIdentityCredentialAdapter(
            resource_id="https://graph.microsoft.com/"
        )
        microsoft_graph_creds.set_token()
    except ClientAuthenticationError:
        # NOTE: Default Azure Credential raises its own error
        raise ExitException("Please try again after logging into azure in your terminal")

    # Validate cluster name
    if not name:
        cluster_utils.echo_delimiter()
        name = click.prompt("Enter a display name for this Azure cluster within Spell")

    with api_client_exception_handler():
        spell_client.validate_cluster_name(name)

    # Queries for Subscription ID
    subscription_client = SubscriptionClient(credentials)
    subscription_id = get_subscription(subscription_client)
    if subscription_id is None:
        raise ExitException("No active subscriptions found")
    tenant_id = get_tenant_id(name)

    # Get Region
    cluster_utils.echo_delimiter()
    available_regions = [
        location.name
        for location in subscription_client.subscriptions.list_locations(subscription_id)
    ]
    region = click.prompt(
        "Please choose a region for your cluster. This might affect machine availability",
        type=click.Choice(available_regions),
        default=DEFAULT_REGION,
    )
    supports_no_gpu = region in (
        "canadaeast",
        "centralus",
        "westcentralus",
        "southafricawest",
        "eastasia",
        "australiacentral",
        "australiacentral2",
        "australiasoutheast",
        "brazilsoutheast",
        "chinaeast",
        "chinanorth",
        "francesouth",
        "germany",
        "germanycentral",
        "germanynorth",
        "germanywestcentral",
        "southindia",
        "westindia",
        "japanwest",
        "koreasouth",
        "switzerlandnorth",
        "switzerlandwest",
        "uaecentral",
        "ukwest",
    )
    if supports_no_gpu:
        if not click.confirm(
            f"Azure does not support GPU types in {region}. You can still create a cluster, but it will "
            "only have access to CPU types - continue?"
        ):
            return

    if ctx.obj["interactive"]:
        spinner = Halo(spinner=get_star_spinner_frames(ctx.obj["utf8"]))

    # Create Service Principal
    cluster_utils.echo_delimiter()
    client = GraphRbacManagementClient(graph_rbac_creds, tenant_id)
    client_id, sp_object_id, app_object_id = create_service_principal(
        client, service_principal_name, name, spinner
    )
    client_secret = set_client_secret(microsoft_graph_creds, sp_object_id, spinner)

    # Create Resource Group
    resource_client = ResourceManagementClient(credentials, subscription_id)
    resource_group = create_resource_group(resource_client, resource_group_name, region, spinner)

    # Creates and Assigns Custom Role to Service Principal
    authorization_client = AuthorizationManagementClient(management_cred, subscription_id)
    create_and_assign_role(
        management_cred,
        subscription_id,
        authorization_client,
        resource_group.id,
        sp_object_id,
        resource_group_name,
        spinner,
    )

    # Create Networking
    network_client = NetworkManagementClient(credentials, subscription_id)
    create_network(network_client, resource_group_name, region, spinner)

    # Creates Storage Account
    storage_client = StorageManagementClient(credentials, subscription_id)
    params = StorageAccountCreateParameters(
        sku=Sku(name=SkuName.standard_ragrs), kind=Kind.storage_v2, location=region,
    )
    storage_account, storage_account_name = create_storage_account(
        storage_client, name, resource_group_name, params, spinner
    )

    # Get Storage Key
    click.echo(f"Fetching Storage Account `{storage_account_name}` access key...")
    list_keys = storage_client.storage_accounts.list_keys(resource_group_name, storage_account_name)
    storage_keys = {v.key_name: v.value for v in list_keys.keys}
    storage_key = storage_keys["key1"]

    # Creates Blob Container
    blob_service_client = BlobServiceClient(
        account_url=storage_account.primary_endpoints.blob, credential=storage_key
    )
    create_blob_container(storage_account_name, blob_service_client, spinner)

    with api_client_exception_handler():
        click.echo("Uploading cluster information to Spell...")
        cluster = spell_client.create_azure_cluster(
            name,
            app_object_id,
            client_id,
            client_secret,
            region,
            resource_group_name,
            sp_object_id,
            storage_account_name,
            storage_key,
            subscription_id,
            tenant_id,
            CLUSTER_VERSION,
        )
        cluster_utils.echo_delimiter()
        url = f"{ctx.obj['web_url']}/{ctx.obj['owner']}/clusters/{cluster['name']}"
        click.echo(
            f"Your cluster {cluster['name']} is initialized! Head over to the web console to create machine types "
            f"to execute your runs on - {url}"
        )


def get_tenant_id(name):
    """
    Shells out to Azure CLI to get Tenant ID
    """
    try:
        process = subprocess.run(
            ["az", "account", "show"], check=True, stdout=subprocess.PIPE, universal_newlines=True
        )
        output = process.stdout
        data = json.loads(output)
        tenant_id = data["tenantId"]
    except Exception as e:
        # TODO(sruthi): Remove for customer when we are finished developing
        click.echo(f"ERROR: While extracting tenant id. Error was: {e}", err=True)
        sentry.capture_message(
            f"Error occured when extracting tenant id using the Azure CLI for cluster {name}: "
            f"Error was '{e}''"
        )
        tenant_id = click.prompt("Enter tenant id of Azure Active Directory")
    return tenant_id


def get_subscription(client):
    cluster_utils.echo_delimiter()
    click.echo("Querying for Subscription ID...")
    sub_ids = [sub.subscription_id for sub in client.subscriptions.list() if sub.state == "Enabled"]
    if not sub_ids:
        return None
    elif len(sub_ids) == 1:
        click.echo(
            f"One Subscription found: {sub_ids[0]}. "
            "Defaulting to this subscription for this cluster"
        )
        return sub_ids[0]
    else:
        return click.prompt(
            "Please choose a subscription id from your active subscriptions",
            type=click.Choice(sub_ids),
        )


def create_service_principal(client, service_principal_name, name, spinner):
    """
    Creates an App `spell-sp` and Service Principal
    Returns the client id aka. appID and object id of the sp
    TODO(sruthi): Switch to use Microsoft Graph REST API instead of deprecated AD Graph API
    """
    from azure.graphrbac.models.graph_error import GraphErrorException

    if spinner:
        spinner.text = "Creating Service Principal..."
        spinner.start()
    else:
        click.echo("Creating Service Principal...")
    try:
        app = client.applications.create(
            {"available_to_other_tenants": False, "display_name": service_principal_name}
        )
        sp = client.service_principals.create({"app_id": app.app_id, "account_enabled": True})
    except GraphErrorException as e:
        sentry.capture_message(
            f"Error occured when attempting to create service principal for cluster {name}: "
            f"Error was '{e}'"
        )
        raise ExitException(
            "Please ensure that your user has the appropriate Azure Active Directory Admin Role "
            "needed to create service principals in your local tenant."
        )

    # Waits for App and Service Principal to be created
    for i in range(NUM_RETRIES):
        if spinner:
            spinner.text = "Verifying Service Principal was created..."
        try:
            client.applications.get(app.object_id)
            client.service_principals.get(sp.object_id)
        except GraphErrorException as e:
            is_app_exception = f"Resource '{app.object_id}' does not exist" in str(e)
            is_sp_exception = f"Resource '{sp.object_id}' does not exist" in str(e)
            if not is_app_exception and not is_sp_exception:
                sentry.capture_exception(e)
                raise ExitException(
                    f"Was not able to read newly created Service Principal `{service_principal_name}`"
                )
            if i == NUM_RETRIES - 1:
                sentry.capture_message(
                    f"Retried {NUM_RETRIES} times to get service principal `{service_principal_name}` for "
                    f"cluster `{name}`. Error was '{e}'"
                )
                raise ExitException(
                    f"Was not able to Get Service Principal `{service_principal_name}`"
                )
            time.sleep(3)
        else:
            break
    if spinner:
        spinner.stop()
    click.echo(f"Successfully created Service Principal `{service_principal_name}`")
    return app.app_id, sp.object_id, app.object_id


def set_client_secret(credentials, object_id, spinner):
    """
    Uses Microsoft Graph REST API to generate a client secret
    Returns the client secret and the end date (date the client secret expires)

    NOTE: There is no Python client library for this, so we do raw HTTP requests to the API.
    In the future we will use the python client API that has not yet been released.
    """

    if spinner:
        spinner.text = "Creating SP Client secret..."
        spinner.start()
    else:
        click.echo("Creating SP Client secret...")
    # Create Request
    header = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {credentials.token['access_token']}",
    }
    url = f"https://graph.microsoft.com/v1.0/servicePrincipals/{object_id}/addPassword"
    payload = {
        "passwordCredential": {
            "displayName": "spellClientSecret",
            "endDateTime": "2222-01-01T00:00:00Z",  # Never expires
        },
    }
    # POST request
    try:
        response = requests.post(url, data=json.dumps(payload), headers=header)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise ExitException(f"Error setting client secret: {e.response.text}")

    # Return Client Secret
    secret_info = json.loads(response.text)
    if spinner:
        spinner.stop()
    return secret_info["secretText"]


def create_resource_group(resource_client, resource_group_name, region, spinner):
    cluster_utils.echo_delimiter()
    if spinner:
        spinner.text = "Creating Resource Group..."
        spinner.start()
    else:
        click.echo("Creating Resource Group...")

    if resource_client.resource_groups.check_existence(resource_group_name):
        if spinner:
            spinner.stop()
        raise ExitException(
            f"Resource group `{resource_group_name}` already exists - "
            "please select a different name"
        )
    resource_group = resource_client.resource_groups.create_or_update(
        resource_group_name, {"location": region}
    )
    if spinner:
        spinner.stop()
    click.echo(f"Successfully created Resource Group `{resource_group_name}`")
    return resource_group


def create_and_assign_role(
    credentials,
    subscription_id,
    authorization_client,
    group_id,
    object_id,
    resource_group_name,
    spinner,
):
    """Creates a custom `Spell-Access` role with the specified permissions """
    cluster_utils.echo_delimiter()
    role_definition_id = str(uuid.uuid4())
    role_name = f"SpellAccess_{str(random.randint(10 ** 6, 10 ** 7))}"
    header = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {credentials.token['access_token']}",
    }
    scope = f"subscriptions/{subscription_id}/resourceGroups/{resource_group_name}"
    url = (
        f"https://management.azure.com/{scope}/providers/Microsoft.Authorization/"
        f"roleDefinitions/{role_definition_id}?api-version=2015-07-01"
    )
    payload = {
        "name": role_definition_id,
        "properties": {
            "roleName": role_name,
            "description": "Spell Access Role to let Spell spin up and down worker machines and access your blobs",
            "type": "CustomRole",
            "permissions": [{"actions": required_permissions}],
            "assignableScopes": [scope],
        },
    }
    permissions = "\n".join("\t" + p for p in required_permissions)
    click.echo(f"Creating role {role_name} with the following permissions: \n{permissions}")
    if spinner:
        spinner.text = "Creating Role..."
        spinner.start()
    try:
        response = requests.put(url, data=json.dumps(payload), headers=header)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if spinner:
            spinner.stop()
        raise ExitException(f"Error creating role: {e.response.text}")

    if spinner:
        spinner.stop()
    click.echo(f"Successfully created Role `{role_name}`")
    if spinner:
        spinner.text = f"Assigning Role `{role_name}` to Service Principal..."
        spinner.start()
    else:
        click.echo(f"Assigning Role `{role_name}` to Service Principal...")

    roles = list(
        authorization_client.role_definitions.list(group_id, filter=f"roleName eq '{role_name}'")
    )
    assert len(roles) == 1, (
        f"Found unexpected number of roles ({len(roles)}) with name {role_name}."
        "Expected exactly 1"
    )
    spell_role = roles[0]

    # Assign Custom Role to Service Principal
    authorization_client.role_assignments.create(
        group_id,
        uuid.uuid4(),
        {
            "role_definition_id": spell_role.id,
            "principal_id": object_id,
            "principal_type": "ServicePrincipal",
        },
    )
    if spinner:
        spinner.stop()
    click.echo(f"Successfully assigned Role `{role_name}` to Service Principal `{object_id}")


def create_network(network_client, resource_group_name, region, spinner):
    from azure.mgmt.network.v2020_06_01.models import SecurityRule
    from azure.mgmt.network.v2020_06_01.models import NetworkSecurityGroup
    from azure.core.exceptions import HttpResponseError

    cluster_utils.echo_delimiter()
    if spinner:
        spinner.text = "Creating VNet..."
        spinner.start()
    else:
        click.echo("Creating VNet...")

    # Create VPC
    cidr = "10.0.0.0/16"
    async_vnet_creation = network_client.virtual_networks.begin_create_or_update(
        resource_group_name,
        VNET_NAME,
        {"location": region, "address_space": {"address_prefixes": [cidr]}},
    )
    async_vnet_creation.wait()

    # Create Subnet
    if spinner:
        spinner.text = "Creating Subnet..."
    else:
        click.echo("Creating Subnet...")
    async_subnet_creation = network_client.subnets.begin_create_or_update(
        resource_group_name, VNET_NAME, SUBNET_NAME, {"address_prefix": cidr}
    )
    async_subnet_creation.result()

    # Create Security Group
    if spinner:
        spinner.text = "Creating Security Group..."
    else:
        click.echo("Creating Security Group...")
    nsg_params = NetworkSecurityGroup(
        id=SECURITY_GROUP_NAME, location=region, tags={"name": VNET_NAME}
    )
    try:
        nsg = network_client.network_security_groups.begin_create_or_update(
            resource_group_name, SECURITY_GROUP_NAME, parameters=nsg_params
        )
    except HttpResponseError as e:
        raise ExitException(f"Unable to create new security group. Azure error: {e}")

    # Add Outbound Security Rules for Ingress Ports
    if spinner:
        spinner.text = "Adding Ingress/Egress rules to Security Group..."
    else:
        click.echo("Adding Ingress/Egress rules to Security Group...")
    priority = 100  # Determines the order in which Security Rules get processed, lower numbers have higher priority
    for port in INGRESS_PORTS:
        security_rule_name = f"spell-security-rule-{port}"
        security_rule_parameters = SecurityRule(
            name=security_rule_name,
            description="Allows the Spell API SSH and Docker access to worker machines",
            protocol="Tcp",
            source_port_range="*",
            destination_port_range=port,
            source_address_prefix="*",
            destination_address_prefix="*",
            access="Allow",
            direction="Inbound",
            priority=priority,
        )
        try:
            network_client.security_rules.begin_create_or_update(
                resource_group_name,
                SECURITY_GROUP_NAME,
                security_rule_name,
                security_rule_parameters,
            )
        except HttpResponseError as e:
            raise ExitException(f"Error creating Security Rule. Azure error: {e}")
        priority += 1

    if spinner:
        spinner.stop()
    click.echo(f"Successfully created Security Group `{nsg.result().name}`")


def create_storage_account(storage_client, cluster_name, resource_group_name, params, spinner):
    from azure.core.exceptions import HttpResponseError
    from azure.mgmt.storage.v2019_06_01.models import StorageAccountCheckNameAvailabilityParameters

    """Creates a Storage Account and returns Storage Client, Storage Account"""

    cluster_utils.echo_delimiter()
    default_name = "".join(filter(str.isalnum, f"spell{cluster_name[:13].lower()}storage"))
    storage_account_name = click.prompt(
        "Please enter a name for the Azure Storage Account Spell will create to store run outputs.\n"
        "NOTE: Storage account names must be between 3 and 24 characters in length and may only contain "
        "numbers and lowercase letters.\nYour storage account name must be UNIQUE within Azure. "
        "No two storage accounts can have the same name.",
        default=default_name,
    ).strip()
    if spinner:
        spinner.text = "Validating name..."
        spinner.start()
    account_name = StorageAccountCheckNameAvailabilityParameters(name=storage_account_name)
    # Built in Azure Storage Account name validator
    availability = storage_client.storage_accounts.check_name_availability(account_name)
    if not availability.name_available:
        click.echo(
            f"Azure does not support this name for the following reason: {availability.reason}"
        )
        if spinner:
            spinner.stop()
        return create_storage_account(
            storage_client, cluster_name, resource_group_name, params, spinner
        )

    # Create Storage Account
    try:
        if spinner:
            spinner.text = f"Creating Storage Account `{storage_account_name}`"
        storage_async_operation = storage_client.storage_accounts.begin_create(
            resource_group_name, storage_account_name, params,
        )
        storage_account = storage_async_operation.result()
    except HttpResponseError as e:
        if spinner:
            spinner.stop()
        click.echo(f"Unable to create storage account. Azure error: {e}", err=True)
        return create_storage_account(
            storage_client, cluster_name, resource_group_name, params, spinner
        )

    if spinner:
        spinner.stop()
    click.echo(
        f"Successfully created Storage Account `{storage_account_name}` under resource group `{resource_group_name}`"
    )
    return storage_account, storage_account_name


def create_blob_container(storage_account_name, blob_service_client, spinner):
    """Creates a Blob Container and returns the Container Client"""
    if spinner:
        spinner.text = "Creating Blob Container..."
        spinner.start()
    else:
        click.echo("Creating Blob Container...")

    for i in range(3):
        try:
            blob_service_client.create_container(storage_account_name)
            if spinner:
                spinner.stop()
            click.echo(f"Created your new blob container `{storage_account_name}`!")
            return
        except Exception as e:
            click.echo(f"Unable to create blob container. Azure error: {e}", err=True)

    if spinner:
        spinner.stop()
    raise ExitException("Could not create blob container after three retries.")


def delete_azure_cluster(ctx, cluster):
    """
    Deletes an Azure cluster, including the Spell Cluster, Machine Types,
    Security Principal, Resource Group, Vnet, Storage Accounts, and Roles associated with this cluster.
    """

    spell_client = ctx.obj["client"]
    cluster_utils.validate_org_perms(spell_client, ctx.obj["owner"])

    try:
        from azure.graphrbac import GraphRbacManagementClient
        from azure.mgmt.resource import ResourceManagementClient
        from spell.cli.utils.azure_credential_wrapper import AzureIdentityCredentialAdapter
        from azure.core.exceptions import ClientAuthenticationError
        from azure.identity import DefaultAzureCredential

    except ImportError:
        click.echo("Please `pip install --upgrade 'spell[cluster-azure]'` and rerun this command")
        return

    click.echo(
        "This command will delete the Spell Cluster, Machine Types, Service Principal, "
        "VNet, Custom Role, Resource Group, and Storage Account associated with this cluster. "
    )
    if not click.confirm(f"Are you SURE you want to delete the spell cluster {cluster['name']}?"):
        return
    # Create Credentials
    try:
        credentials = DefaultAzureCredential(
            exclude_environment_credential=True,
            exclude_managed_identity_credential=True,
            exclude_visual_studio_code_credential=True,
            exclude_shared_token_cache_credential=True,
        )
        management_cred = AzureIdentityCredentialAdapter()
        management_cred.set_token()
        graph_rbac_creds = AzureIdentityCredentialAdapter(resource_id="https://graph.windows.net/")
        graph_rbac_creds.set_token()
    except ClientAuthenticationError:
        # NOTE: Default Azure Credential raises its own error
        raise ExitException("Please try again after logging into azure in your terminal")

    if ctx.obj["interactive"]:
        spinner = Halo(spinner=get_star_spinner_frames(ctx.obj["utf8"]))

    # Delete Machine Types and Model Servers on cluster first
    cluster_utils.echo_delimiter()
    with api_client_exception_handler():
        click.echo(
            "Sending message to Spell to remove all Machine Types "
            f"from the cluster {cluster['name']}..."
        )
        spell_client.delete_cluster_contents(cluster["name"])

    # Block until cluster is drained. This is necessary because the API will fail to
    # drain if we delete the IAM role before the machine types are marked as drained
    cluster_utils.block_until_cluster_drained(spell_client, cluster["name"], spinner)

    subscription_id = cluster["role_credentials"]["azure"]["subscription_id"]
    tenant_id = cluster["role_credentials"]["azure"]["tenant_id"]
    resource_client = ResourceManagementClient(credentials, subscription_id)
    rg_name = cluster["networking"]["azure"]["resource_group_name"]

    # Delete Resource group and everything in it
    cluster_utils.echo_delimiter()
    if not click.confirm(
        "WARNING: All the stored run outputs and uploads will be deleted with this command, as they are within "
        "the cluster's resource group. If you would like to save this data, please copy it to a different storage "
        "account in a different resource group before re-running this command. Continue?"
    ):
        return
    if spinner:
        spinner.text = f"Deleting Resource Group `{rg_name}`..."
        spinner.start()
    else:
        click.echo(f"Deleting Resource Group `{rg_name}`...")
    delete_async_operation = resource_client.resource_groups.begin_delete(rg_name)
    delete_async_operation.wait()
    if spinner:
        spinner.stop()
    click.echo(f"Resource Group `{rg_name}` deleted")

    # Delete App/SP
    cluster_utils.echo_delimiter()
    if spinner:
        spinner.text = "Deleting App and Service Principal..."
        spinner.start()
    else:
        click.echo("Deleting App and Service Principal...")
    client = GraphRbacManagementClient(graph_rbac_creds, tenant_id)
    client.service_principals.delete(cluster["role_credentials"]["azure"]["sp_object_id"])
    client.applications.delete(cluster["role_credentials"]["azure"]["app_object_id"])
    if spinner:
        spinner.stop()
    click.echo("Deleted App and Service Principal `spell-app`")

    # Last step is to mark the cluster as deleted
    cluster_utils.echo_delimiter()
    click.echo("Deleting cluster on Spell...")
    with api_client_exception_handler():
        spell_client.delete_cluster(cluster["name"])
        click.echo("Successfully deleted cluster on Spell")


def add_az_bucket(spell_client, cluster, account_name):
    """
    This command adds a cloud storage bucket to SpellFS, which enables interaction with the bucket objects
    via ls, cp, and mounts.

    NOTE: This command uses your Azure credentials - you will need to set the proper AD Admin Role on the portal
    """
    from azure.core.exceptions import ClientAuthenticationError
    from azure.identity import DefaultAzureCredential
    from azure.mgmt.storage import StorageManagementClient
    from azure.mgmt.resource.subscriptions import SubscriptionClient
    from azure.storage.blob import BlobServiceClient

    # Create Credentials
    try:
        credentials = DefaultAzureCredential(
            exclude_environment_credential=True,
            exclude_managed_identity_credential=True,
            exclude_visual_studio_code_credential=True,
            exclude_shared_token_cache_credential=True,
        )
    except ClientAuthenticationError:
        # NOTE: Default Azure Credential raises its own error
        raise ExitException("Please try again after logging into azure in your terminal")

    cluster_name = cluster["name"]
    subscription_client = SubscriptionClient(credentials)
    subscription_id = get_subscription(subscription_client)

    click.echo(
        """This command will
    - List your storage accounts to generate an options menu of storage accounts thatcan be added to Spell
    - Get the storage account access key so Spell can access your storage account"""
    )
    # Get storage client
    storage_client = StorageManagementClient(credentials, subscription_id)

    # Get storage account name
    click.echo(f"Available storage accounts in subscription {subscription_id}")
    account_names = {}
    for account in storage_client.storage_accounts.list():
        account_names[account.name] = account.id
    if account_name is None:
        for account in account_names.keys():
            click.echo(f"- {account}")
        account_name = click.prompt(
            "Please choose a storage account", type=click.Choice(account_names), show_choices=False,
        )
    # Get resource group from storage account id
    rg_name = get_rg_from_sa_id(account_names[account_name])
    # Get storage key
    list_keys = storage_client.storage_accounts.list_keys(rg_name, account_name)
    storage_keys = {v.key_name: v.value for v in list_keys.keys}
    storage_key = storage_keys["key1"]

    blob_service_client = BlobServiceClient.from_connection_string(
        get_connection_string(account_name, storage_key)
    )
    # Get all containers
    click.echo(f"\nAvailable blob containers in storage account {account_name}")
    container_names = [container.name for container in blob_service_client.list_containers()]
    # Prompt for container name
    for container in container_names:
        click.echo("- {}".format(container))
    container_name = click.prompt(
        "Please choose a container", type=click.Choice(container_names), show_choices=False,
    )
    bucket_name = account_name + "_" + container_name

    # Register new bucket to cluster in API
    with api_client_exception_handler():
        spell_client.add_bucket(bucket_name, cluster_name, "azblob", storage_key)
    click.echo(
        f"Blob container {container_name} from storage account {account_name} has been added to cluster {cluster_name}!"
    )


def get_rg_from_sa_id(id):
    """
    This helper parses the resource group name from the storage account id

    Storage Account ids are of the form '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/
        providers/{resourceProviderNamespace}/{resourceType}/{resourceName}.'
    """
    result = re.findall("resourceGroups/(.*?)/providers/", id)
    if len(result) > 1:
        return ExitException("Unexpected parsing")
    else:
        return result[0]


def get_connection_string(storage_account_name, storage_key):
    """
    This helper creates a connection string from the storage account name and storage key which can
    be used to authenticate a Blob Service Client (needed to list containers)
    """
    connection_str = (
        "DefaultEndpointsProtocol=https;"
        + f"AccountName={storage_account_name};"
        + f"AccountKey={storage_key};"
        + "EndpointSuffix=core.windows.net"
    )
    return connection_str


def rotate_cluster_storage_key(spell_client, cluster):
    """ This command rotates the storage key for the customer's storage account """
    from azure.core.exceptions import ClientAuthenticationError
    from azure.identity import DefaultAzureCredential
    from azure.mgmt.storage import StorageManagementClient

    # Create Credentials
    try:
        credentials = DefaultAzureCredential(
            exclude_environment_credential=True,
            exclude_managed_identity_credential=True,
            exclude_visual_studio_code_credential=True,
            exclude_shared_token_cache_credential=True,
        )
    except ClientAuthenticationError:
        # NOTE: Default Azure Credential raises its own error
        raise ExitException("Please try again after logging into azure in your terminal")

    cluster_name = cluster["name"]
    subscription_id = cluster["role_credentials"]["azure"]["subscription_id"]
    click.echo(
        """This command will let you rotate your storage keys for your Cluster's primary Storage Account"""
    )
    # Get storage client
    storage_client = StorageManagementClient(credentials, subscription_id)
    account_name = cluster["storage_uri"]
    rg_name = cluster["networking"]["azure"]["resource_group_name"]

    # Get storage key
    list_keys = storage_client.storage_accounts.list_keys(rg_name, account_name)
    storage_keys = {v.key_name: v.value for v in list_keys.keys}
    key_rotate = click.prompt(
        "Enter 'key1' to use Key 1 or 'key2' to use Key 2?",
        type=click.Choice(["key1", "key2"]),
        show_choices=False,
    )
    new_storage_key = storage_keys[key_rotate]

    # Register new bucket to cluster in API
    with api_client_exception_handler():
        spell_client.rotate_cluster_storage_key(cluster_name, new_storage_key)
    click.echo(
        f"Storage account {account_name} is updated to use new {key_rotate} for cluster {cluster_name}!"
    )
