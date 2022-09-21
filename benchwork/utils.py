"""Utils for benchwork"""
import textwrap
from abc import ABC
from typing import Any


class Subclasses(ABC):
    """Base class to collect subclasses"""

    _SUBCLASSES = None

    def __init_subclass__(cls) -> None:
        base = cls.__bases__[0]
        if base._SUBCLASSES is None:
            base._SUBCLASSES = []
        base._SUBCLASSES.append(cls)
        return super().__init_subclass__()


def get_docstring(obj: Any) -> str:
    """Get the docstring of an object

    If the docstring is indented, try to dedent it.

    Args:
        obj: The object to get the docstring from

    Returns:
        The docstring. It not found, returns an empty string
    """
    docstr = getattr(obj, "__doc__", None)
    if docstr is None:
        return ""

    try:
        firstline, rest = docstr.split("\n", 1)
    except ValueError:
        return docstr
    else:
        return f"{firstline}\n{textwrap.dedent(rest)}"
