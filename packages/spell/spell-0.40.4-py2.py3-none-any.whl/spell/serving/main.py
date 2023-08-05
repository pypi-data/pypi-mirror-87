import multiprocessing
from typing import Optional

from hypercorn.config import Config as HypercornConfig
from hypercorn.run import run as hypercorn_run

from spell.serving import settings as server_settings
from spell.serving.proxy import settings as proxy_settings


def run_proxy() -> None:
    from spell.serving.proxy import server_conf

    config = HypercornConfig.from_object(server_conf)
    config.application_path = "spell.serving.proxy.app:app"
    hypercorn_run(config)


def run_servers(num_workers: Optional[int]) -> None:
    from spell.serving import server_conf

    config = HypercornConfig.from_object(server_conf)
    if num_workers:
        config.workers = num_workers
    if server_settings.USE_BATCH_PREDICT:
        if proxy_settings.MODEL_SERVER_SOCKET:
            config.bind = f"unix:{proxy_settings.MODEL_SERVER_SOCKET}"
        else:
            config.bind = "localhost:5000"
    config.application_path = "spell.serving.app:app"
    hypercorn_run(config)


def main(num_server_workers):
    if server_settings.USE_BATCH_PREDICT:
        proxy_process = multiprocessing.Process(target=run_proxy, daemon=True)
        proxy_process.start()
    run_servers(num_server_workers)
