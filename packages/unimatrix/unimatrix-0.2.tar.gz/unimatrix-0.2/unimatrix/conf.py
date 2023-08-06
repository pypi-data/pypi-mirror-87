"""Exposes the settings declared in the environment variable
``UNIMATRIX_SETTINGS_MODULE``."""
import importlib
import os
import sys

from unimatrix.exceptions import ImproperlyConfigured


if not os.getenv('UNIMATRIX_SETTINGS_MODULE'):
    raise ImproperlyConfigured("UNIMATRIX_SETTINGS_MODULE is not defined.")
module_qualname = os.getenv('UNIMATRIX_SETTINGS_MODULE')
try:
    settings = importlib.import_module(module_qualname)
except ImportError:
    raise ImproperlyConfigured(
        "Can not import settings module %s" % module_qualname)
