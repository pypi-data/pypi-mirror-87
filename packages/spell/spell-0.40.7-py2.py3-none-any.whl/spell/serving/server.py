from pathlib import Path
from typing import Any, Dict, Optional

from prometheus_client import make_asgi_app as make_custom_metrics_app

from starlette.applications import Starlette
from starlette.exceptions import ExceptionMiddleware
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.routing import Mount
import yaml

from spell.serving import settings
from spell.serving.exceptions import InvalidServerConfiguration
from spell.serving.api import BatchedAPI, API

READY_FILE = "/ready"


def get_config(path: Optional[Path]) -> Dict[str, Any]:
    if path is None:
        return {}
    if not path.is_file():
        raise InvalidServerConfiguration("Config file must be a file")
    try:
        with path.open() as f:
            return yaml.safe_load(f)
    except yaml.scanner.ScannerError as e:
        raise InvalidServerConfiguration("Could not read config file") from e


def make_api() -> API:
    config = get_config(settings.CONFIG_FILE)
    api_class = BatchedAPI if settings.USE_BATCH_PREDICT else API
    api = api_class.from_settings()
    api.initialize_predictor(config)
    return api


def create_ready_file() -> None:
    open(READY_FILE, "a").close()


def make_app(api: Optional[API] = None, debug: bool = False) -> Starlette:
    if not api:
        api = make_api()
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
            allow_credentials=True,
        ),
        Middleware(ExceptionMiddleware),
        Middleware(GZipMiddleware),
    ]
    routes = api.get_routes()
    routes.append(Mount("/metrics", make_custom_metrics_app()))
    return Starlette(
        debug=debug,
        routes=routes,
        middleware=middleware,
        on_startup=[create_ready_file],
    )
