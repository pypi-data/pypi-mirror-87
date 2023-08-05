"""Python package to build simple toy accelerator.
"""
import logging

from . import elements
from .beam import Beam
from .constraints import (
    TargetDispersion,
    TargetGlobal,
    TargetPhasespace,
    TargetTwiss,
    TargetTwissSolution,
)
from .elements import *
from .lattice import Lattice

__all__ = [
    "Beam",
    "Lattice",
    "TargetPhasespace",
    "TargetTwiss",
    "TargetTwissSolution",
    "TargetDispersion",
    "TargetGlobal",
]
__all__.extend(elements.__all__)

__version__ = "0.1.7"

logger = logging.getLogger("pyaccelerator")
