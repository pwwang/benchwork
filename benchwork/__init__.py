from .api import BenchAPI
from .case import BenchCase, BenchCaseVersion, BenchCaseSpeed
from .set_ import (
    BenchSet,
    BenchSetTable,
    BenchSetSpeed,
    BenchSetVersion,
    BenchSetMultiColTable,
)
from .suite import BenchSuite, run_suite

__version__ = "0.0.2"
