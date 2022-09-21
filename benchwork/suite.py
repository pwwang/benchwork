from __future__ import annotations

from abc import ABC, abstractproperty
from typing import TYPE_CHECKING, Type

from .utils import get_docstring

if TYPE_CHECKING:
    from argparse import Namespace
    from .set_ import BenchSet

STDOUT = "<stdout>"


class BenchSuite(ABC):
    """The benchmarking suite"""

    __slots__ = ("args", "sets", "results")

    def __init__(self, args: Namespace) -> None:
        self.args = args
        self.sets = [setclass(args) for setclass in self.set_classes]
        self.results = []

    @abstractproperty
    def set_classes(self) -> Type[BenchSet]:
        """Test set classes"""

    def prepare(self) -> BenchSuite:
        """Preparation for tests"""
        for s in self.sets:
            s.prepare_cases()
        return self

    def run(self) -> BenchSuite:
        """Run the tests"""
        for s in self.sets:
            self.results.append(s.run_cases())
        return self

    def collect(self, title: str, outfile: str) -> None:
        """Collect the results

        Args:
            title: The title of the report
            outfile: The output file to save the report
        """
        if outfile == STDOUT:
            from sys import stdout
            h = stdout
        else:
            h = open(outfile, "w")

        try:
            h.write(f"# {title}\n\n")
            doc = get_docstring(self)
            if doc:
                h.write(f"{doc}\n\n")

            for s, r in zip(self.sets, self.results):
                h.write(f"## {s.title}\n\n")
                sdoc = get_docstring(s)
                if sdoc:
                    h.write(f"{sdoc}\n\n")
                h.write(f"{r}\n\n")

        finally:
            if outfile != STDOUT:
                h.close()


def run_suite(
    suite_class: Type[BenchSuite],
    args: Namespace,
    title: str,
    outfile: str = STDOUT,
) -> None:
    """Run a benchmarking suite

    Args:
        suite_class: The suite class, a subclass of BenchSuite
        args: The arguments parsed from command line
        title: The title of the report
        outfile: The output file to save the report.
            `<stdout>` to print to stdout.
    """

    suite = suite_class(args)
    suite.prepare().run().collect(title, outfile)
