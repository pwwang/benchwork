from __future__ import annotations

from abc import ABC, abstractproperty
from typing import TYPE_CHECKING, Type, List

from .api import BenchAPI
from .case import BenchCaseVersion

if TYPE_CHECKING:
    from argparse import Namespace
    from .case import BenchCase


class BenchSet(ABC):
    """The test set base class"""

    __slots__ = ("args", "cases")

    def __init__(self, args: Namespace) -> None:
        self.args = args
        self.cases = [
            self.case(args, api_class)
            for api_class in self.api_base._SUBCLASSES
        ]

    @abstractproperty
    def case(self) -> Type[BenchCase]:
        """The test case"""

    @property
    def api_base(self) -> Type[BenchAPI]:
        """The API base class"""
        return BenchAPI

    @abstractproperty
    def title(self) -> str:
        """The title of the test set"""

    def prepare_cases(self):
        """Prepare all cases"""
        for case in self.cases:
            case.prepare()

    def run_cases(self):
        """Run all cases"""
        out = []
        for case in self.cases:
            out.append(f"{case.run()}\n")
        return "\n".join(out)


class BenchSetTable(BenchSet, ABC):
    """Test set with table as output"""

    _SUBCLASSES = None

    @abstractproperty
    def header(self) -> str:
        ...

    def run_cases(self):
        out = [
            f"| |{self.header}|",
            "|-|-----------------------|",
        ]
        for case in self.cases:
            ret = str(case.run())
            ret = ret.replace("\n", "<br />")
            out.append(f"|{case.api.name}|{ret}|")
        return "\n".join(out)


class BenchSetMultiColTable(BenchSet, ABC):
    """Test set with multi-column table as output"""

    _SUBCLASSES = None

    @abstractproperty
    def header(self) -> List[str]:
        ...

    def run_cases(self):
        out = [
            f"| |{'|'.join(self.header)}|",
            f"|-|{'|'.join(['-'] * len(self.header))}|",
        ]
        for case in self.cases:
            ret = case.run()
            ret = [str(r).replace("\n", "<br />") for r in ret]
            out.append(f"|{case.api.name}|{'|'.join(ret)}|")
        return "\n".join(out)


class BenchSetSection(BenchSet, ABC):
    """Test set with table as output"""

    _SUBCLASSES = None

    def run_cases(self):
        out = []
        for case in self.cases:
            ret = str(case.run())
            ret = ret.replace("\n", "<br />")
            out.append(f"### {case.api.name}\n")
            out.append(ret)
        return "\n".join(out)


class BenchSetVersion(BenchSetTable):
    """Show versions of testing packages"""

    _SUBCLASSES = None
    header = "Version"
    title = "Versions"
    api_base = BenchAPI
    case = BenchCaseVersion


class BenchSetSpeed(BenchSetTable):
    """Running speed of testing packages"""

    _SUBCLASSES = None
    header = "Speed"
    title = "Running speed"
    api_base = BenchAPI
