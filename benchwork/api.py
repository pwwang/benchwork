from __future__ import annotations

from abc import ABC, abstractproperty
from typing import TYPE_CHECKING

from .utils import Subclasses

if TYPE_CHECKING:
    from argparse import Namespace


class BenchAPI(Subclasses, ABC):

    _SUBCLASSES = None

    def __init__(self, args: Namespace) -> None:
        self.args = args

    @abstractproperty
    def name(self):
        ...
