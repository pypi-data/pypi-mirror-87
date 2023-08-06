"""Utilities for color printing."""

from sty import fg
from typing import Tuple


class Color:
    """Colors for color printing."""

    GREEN = (110, 220, 100)
    RED = (200, 80, 90)


def print_rgb(s: str,
              rgb: Tuple[int, int, int],
              *args,
              **kwargs):
    """
    Print to stdout with color.

    :param s: String to print to stdout.
    :param rgb: Tuple with rgb values in the range [0, 255].
    """
    print(f"{fg(*rgb)}{s}{fg.rs}", *args, **kwargs)
