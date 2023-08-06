import inspect
from typing import Callable

from starlette.responses import JSONResponse

from spell.serving.endpoint import (
    Endpoint,
    BatchEndpointPair,
    BatchEndpointPairBase,
    GeneratedBatchEndpointPair,
)
from spell.serving.exceptions import InvalidPredictor
from spell.serving.types import PredictorResponse


class BasePredictor:
    def health(self) -> PredictorResponse:
        return JSONResponse({"status": "ok"})

    @classmethod
    def validate(cls) -> None:
        cls.get_predict_endpoint()
        cls.get_health_endpoint()
        if hasattr(cls, "prepare"):
            cls._create_endpoint("prepare", 1)

    @classmethod
    def get_health_endpoint(cls) -> Endpoint:
        return cls._create_endpoint("health", 0)

    @classmethod
    def get_predict_endpoint(cls) -> Endpoint:
        return cls._create_endpoint("predict", 1)

    @classmethod
    def get_batched_predict_endpoint(cls) -> BatchEndpointPairBase:
        predict = cls.get_predict_endpoint()
        if predict.request:
            raise InvalidPredictor("Batching-enabled predict methods cannot accept Requests")
        if hasattr(cls, "prepare"):
            prepare = cls._create_endpoint("prepare", 1)
            return BatchEndpointPair(prepare, predict)
        else:
            return GeneratedBatchEndpointPair(predict)

    @classmethod
    def _create_endpoint(cls, func_name: str, min_args: int) -> Endpoint:
        func = cls._get_func_or_raise(func_name)
        is_staticmethod = cls._is_staticmethod(func_name)
        is_classmethod = cls._is_classmethod(func)
        return Endpoint.from_func(func, min_args, is_staticmethod, is_classmethod)

    @classmethod
    def _get_func_or_raise(cls, func_name: str) -> Callable:
        func = getattr(cls, func_name, None)
        if not func:
            raise InvalidPredictor(f'Required function "{func_name}" is not defined')
        if not callable(func):
            raise InvalidPredictor(f'"{func_name}" is defined, but is not a function')
        return func

    @classmethod
    def _is_staticmethod(cls, func_name: str) -> bool:
        # Unfortunately, getattr won't work properly here, so we need to directly use cls.__dict__,
        # but calling this on a subclass won't look in its base classes, which is a problem for the
        # health function. We could use cls.__base__, but this won't look further up a class
        # hierarchy, or mixins, so we need to manually traverse the entire method resolution order
        # (__mro__).
        cls_with_definition = next(
            (cls_ for cls_ in cls.__mro__ if cls_.__dict__.get(func_name) is not None), None
        )
        if cls_with_definition is None:
            # This should never happen because when this method is called,
            # getattr(cls, func_name) has returned a valid callable, so the user is doing
            # something seriously pathological here. We'll optimistically return False.
            return False
        return isinstance(cls_with_definition.__dict__[func_name], staticmethod)

    @classmethod
    def _is_classmethod(cls, func: Callable) -> bool:
        return inspect.ismethod(func) and func.__self__ is cls
