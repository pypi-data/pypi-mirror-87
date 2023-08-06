"""
This module is here to disable the auto-config-resolving logic in the config module,
so that it is easier to tell which config is loaded during test execution.
"""
import feyn._config
import os

UNITTEST_QLATTICE_URL = "http://localhost:5000"
UNITTEST_API_TOKEN = None


def override_config_resolver():
    feyn._config._config_resolver = _unittest_config_resolver


def _unittest_config_resolver(section):
    if "CI" in os.environ:
        return feyn._config._try_load_from_environment_vars()

    return feyn._config.Config(UNITTEST_QLATTICE_URL, UNITTEST_API_TOKEN)
