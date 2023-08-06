from pathlib import Path

from starlette.config import Config


config = Config("/config/.env")


# TODO(Justin): When all environment variables are prefixed with SPELL_,
# remove this function just use, e.g. SPELL_CONFIG_FILE
def optional_spell_prefix(name, default=None, **kwargs):
    value = config(f"SPELL_{name}", default=default, **kwargs)
    if value == default:
        value = config(name, default=default, **kwargs)
    return value


# Path to the config file"
CONFIG_FILE = optional_spell_prefix("CONFIG_FILE", cast=Path, default=None)
# Path to the Python module containing predictor"
MODULE_PATH = optional_spell_prefix("MODULE_PATH", cast=Path, default=None)
# Python path to the module containing the predictor"
PYTHON_PATH = optional_spell_prefix("PYTHON_PATH", default=None)
# Path to the module containing the predictor
ENTRYPOINT = optional_spell_prefix("ENTRYPOINT", cast=Path, default=None)
# Name of the predictor class"
CLASSNAME = optional_spell_prefix("CLASSNAME", default=None)
# Should the /predict endpoint expect batch requests?
USE_BATCH_PREDICT = optional_spell_prefix("USE_BATCH_PREDICT", cast=bool, default=False)
# Run the server in debug mode
DEBUG = optional_spell_prefix("DEBUG", cast=bool, default=False)
