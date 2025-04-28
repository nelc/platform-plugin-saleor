"""Utility functions for pipelines."""

import importlib


def module_member(name):
    """Imports module path and module member."""
    mod, member = name.rsplit(".", 1)
    module = importlib.import_module(mod)
    return getattr(module, member)
