import click

from spell.serving.main import main


@click.command()
@click.option(
    "--enable-batching",
    "is_batching_enabled",
    is_flag=True,
    help="Enable server-side batching. This will spawn both a proxy and workers",
)
@click.option(
    "--num-server-workers",
    type=int,
    help="Number of worker processes to run the model server with.",
)
def run_server(is_batching_enabled, num_server_workers):
    # TODO(Justin): Delete is_batching_enabled
    main(num_server_workers)


run_server()
