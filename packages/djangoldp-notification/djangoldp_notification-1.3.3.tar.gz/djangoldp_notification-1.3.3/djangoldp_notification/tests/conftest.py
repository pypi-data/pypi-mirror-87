from importlib import import_module
from os import environ

from pytest import fail

settings_module = environ.get("DJANGO_SETTINGS_MODULE")
if settings_module is None or len(settings_module) == 0:
    fail("DJANGO_SETTINGS_MODULE needs to be defined and point to your SIB app installation settings")

try:
    import_module(settings_module)
except ImportError:
    initial_module = [token for token in settings_module.split(".") if len(token) > 0][0]
    fail("Unable to import {}. Try to configure PYTHONPATH to point the "
         "directory containing the {} module".format(settings_module, initial_module))
