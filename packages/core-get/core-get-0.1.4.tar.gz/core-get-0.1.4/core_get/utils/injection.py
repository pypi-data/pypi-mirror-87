from typing import List, Type, Dict, Any, Callable

from injector import Provider, T, Injector


class MultiMapClassProvider(Provider):
    """Provides instances from a given dict of classes, created using an Injector."""

    def __init__(self, clss: Dict[Any, Type[T]]) -> None:
        self._clss = clss

    def get(self, injector: Injector) -> T:
        return {key: injector.create_object(cls) for key, cls in self._clss.items()}


class MultiClassProvider(Provider):
    """Provides instances from a given list of classes, created using an Injector."""

    def __init__(self, clss: List[Type[T]]) -> None:
        self._clss = clss

    def get(self, injector: Injector) -> T:
        return [injector.create_object(cls) for cls in self._clss]


class _Lazy:
    def __getitem__(self, t):
        return Callable[[], t]


Lazy = _Lazy()
