from collections import namedtuple
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from starlette.routing import Route

from spell.serving import BasePredictor, settings
from spell.serving.exceptions import InvalidPredictor, InvalidServerConfiguration
from spell.serving.types import PredictorClass
from spell.serving.utils import import_from_entrypoint, import_user_module

ModelInfo = namedtuple("ModelInfo", ("name", "version"), defaults=(None, None))


class API:
    __slots__ = ["predictor_class", "predictor", "predict", "health"]

    def __init__(self, predictor_class: PredictorClass) -> None:
        self.predictor_class = predictor_class
        self.predict = predictor_class.get_predict_endpoint()
        self.health = predictor_class.get_health_endpoint()
        self.predictor = None

    @classmethod
    def from_settings(cls):
        if settings.ENTRYPOINT:
            return cls.from_entrypoint(settings.ENTRYPOINT, classname=settings.CLASSNAME)
        if not (settings.MODULE_PATH and settings.PYTHON_PATH):
            raise InvalidServerConfiguration(
                "Either Module path and Python path must be specified or entrypoint must be specified"
            )
        if not settings.MODULE_PATH.is_dir():
            raise InvalidServerConfiguration("Module path must be a directory")
        return cls.from_module(
            settings.MODULE_PATH,
            settings.PYTHON_PATH,
            classname=settings.CLASSNAME,
        )

    @classmethod
    def from_entrypoint(cls, entrypoint: Path, classname: Optional[str] = None):
        # TODO(Justin) Rename this to from_module after migration from module_path + python_path to entrypoint
        import_from_entrypoint(entrypoint)
        predictor_class = cls.get_predictor_class(classname)
        return cls(predictor_class)

    @classmethod
    def from_module(
        cls,
        module_path: Union[Path, str],
        python_path: Union[Path, str],
        classname: Optional[str] = None,
    ):
        # module_path is the path in the filesystem to the module
        # python_path is the python path to the predictor in the form path.to.module
        import_user_module(module_path=module_path, python_path=python_path)
        predictor_class = cls.get_predictor_class(classname)
        return cls(predictor_class)

    @classmethod
    def get_predictor_class(cls, classname: Optional[str]) -> PredictorClass:
        predictors = {p.__name__: p for p in BasePredictor.__subclasses__()}
        if not predictors:
            raise InvalidPredictor(
                "No predictors found. Make sure your predictors extend BasePredictor."
            )
        if not classname:
            if len(predictors) > 1:
                raise InvalidPredictor(
                    "More than one predictor found, but no classname was specified."
                )
            predictor_name = next(iter(predictors))
            return predictors[predictor_name]
        try:
            return predictors[classname]
        except KeyError:
            raise InvalidPredictor(
                f"No predictor named {classname} was found. The predictors found were ({', '.join(predictors)})"
            )

    def initialize_predictor(self, config: Dict[str, Any]) -> None:
        # We use a two-step initialization process, first create the API with a predictor class,
        # then initialize the prediction. We do this so that we can validate the predictor without
        # loading the entire module
        model_info = config.get("model_info", {})
        user_config = config.get("user_config", {})
        self.predictor = self.predictor_class(**user_config)
        if not hasattr(self.predictor, "model_info"):
            self.predictor.model_info = ModelInfo(**model_info)
        self._bind()

    def _bind(self) -> None:
        """This is required because we need an uninitialized class to validate in the CLI"""
        self.predict.bind(self.predictor)
        self.health.bind(self.predictor)

    def get_routes(self) -> List[Route]:
        return [
            Route("/health", self.health.call, methods=["GET"]),
            Route("/ready", self.health.call, methods=["GET"]),
            Route("/predict", self.predict.call, methods=["POST"]),
        ]


class BatchedAPI(API):
    __slots__ = ["batched_endpoints", "prepare"]

    def __init__(self, predictor_class: PredictorClass) -> None:
        super().__init__(predictor_class)
        self.batched_endpoints = predictor_class.get_batched_predict_endpoint()
        self.prepare = self.batched_endpoints.prepare
        self.predict = self.batched_endpoints.process

    def _bind(self) -> None:
        """This is required because we need an uninitialized class to validate in the CLI"""
        self.batched_endpoints.bind(self.predictor)
        self.health.bind(self.predictor)

    def get_routes(self) -> List[Route]:
        return [
            Route("/health", self.health.call, methods=["GET"]),
            Route("/ready", self.health.call, methods=["GET"]),
            Route("/predict", self.predict, methods=["POST"]),
            Route("/prepare", self.prepare, methods=["POST"]),
        ]
