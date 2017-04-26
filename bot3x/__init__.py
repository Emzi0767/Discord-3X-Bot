"""
3X - A Fuyu guild welcome bot.

A Discord bot by Emzi0767. Just to have another greeting message.
"""

__name__ = "bot3x"
__author__ = "Emzi0767"
__version__ = "1.0.0"
__license__ = "Apache License 2.0"
__copyright__ = "Copyright 2017 Emzi0767"

version_info = tuple(__version__.split("."))

# core modules
from .bot3x import Bot3X
from .bot3x import is_authorized
from .bot3xcmd import Bot3XCommands

# utilities
from .utils import log
