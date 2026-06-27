"""
MagicSniffer v0.1
Inspector determinista de file-spoofing mediante análisis de magic numbers.
"""

__version__ = "0.1.0"
__author__ = "secroses"

from .scanner import inspect_file
from .database import MAGIC_DATABASE

__all__ = ["inspect_file", "MAGIC_DATABASE", "__version__"]
