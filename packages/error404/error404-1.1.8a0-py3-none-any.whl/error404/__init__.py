"""
error404
========

A simple testing module for Python


"""


from .results import test_results, clear_results
from .tests import test

__version__ = "1.1.7"
__all__ = ["test", "test_results", "clear_results"]
