from __future__ import annotations

from abc import ABC, abstractmethod, abstractproperty
from typing import TYPE_CHECKING, Type

from .utils import Subclasses

if TYPE_CHECKING:
    from argparse import Namespace
    from .api import BenchAPI


class BenchCase(Subclasses, ABC):
    """The test case base class.

    This will be instantiated in to instances with different API classes
    """
    _SUBCLASSES = None

    def __init__(self, args: Namespace, api_class: Type[BenchAPI]) -> None:
        self.args = args
        self.api = api_class(args)

    def prepare(self):
        """Prepare the case"""

    def run(self):
        """Run the case"""


class BenchCaseVersion(BenchCase, ABC):
    """Versions of packages tested."""

    _SUBCLASSES = None

    def run(self):
        return self.api.version


class BenchCaseSpeed(BenchCase, ABC):

    _SUBCLASSES = None

    @abstractproperty
    def timeit_number(self) -> int | str:
        ...

    @abstractmethod
    def run_core(self):
        ...

    def run(self):
        from timeit import timeit
        number = self.timeit_number
        if not isinstance(number, int):
            number = getattr(self.args, number)

        return timeit(self.run_core, number=number)
