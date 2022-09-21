# benchwork

A framework for benchmarking in python

## Installation

```python
pip install -U benchwork
```

## Usage

```python
from benchwork import (
    BenchAPI,
    BenchCaseSpeed,
    BenchSuite,
    BenchSetSpeed,
    BenchSetVersion,
    run_suite,
)


class BenchAPIPackage1(BenchAPI):
    name = "package1"
    version = "0.0.1"


class BenchAPIPackage2(BenchAPI):
    name = "package2"
    version = "0.0.2"


class BenchCaseSpeed(BenchCaseSpeed):
    timeit_number = 10

    def run_core(self):
        import time
        time.sleep(.1)


class BenchSetSpeed(BenchSetSpeed):
    case = BenchCaseSpeed


class BenchSuite(BenchSuite):
    """Benchmarking suite"""
    set_classes = [BenchSetVersion, BenchSetSpeed]


if __name__ == "__main__":
    run_suite(BenchSuite, None, "Benchmarking")
```

Output:

```markdown
# Benchmarking

Benchmarking suite

## Versions

Show versions of testing packages

| |Version|
|-|-----------------------|
|package1|0.0.1|
|package2|0.0.2|

## Running speed

| |Speed|
|-|-----------------------|
|package1|1.003228693996789|
|package2|1.0028911930057802|
```
