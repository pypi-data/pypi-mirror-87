from configparser import ConfigParser
import logging
import os
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

resolve_config_failed_message = """Could not resolve `url` and `api_token` from environment variables or configuration file.
Please either set the environment variables [FEYN_QLATTICE_URL] and [FEYN_QLATTICE_API_TOKEN].
Or put a configuration file named [.feynrc] or [feyn.ini] in your home folder."""

QLATTICE_URL_ENV_KEY = "FEYN_QLATTICE_URL"
API_TOKEN_ENV_KEY = "FEYN_QLATTICE_API_TOKEN"

CONFIG_FILE_SEARCH_PATHS = [
    Path.home().joinpath(".config/.feynrc"),
    Path.home().joinpath(".config/feyn.ini"),
    Path.home().joinpath(".feynrc"),
    Path.home().joinpath("feyn.ini"),
]

_config_resolver = None


class Config:
    def __init__(self, url, api_token):
        self.url = url
        self.api_token = api_token


def resolve_config(section=None) -> Optional[Config]:
    # This is here in order to be able to override the configs from tests
    if _config_resolver:
        return _config_resolver(section)  # noqa

    return _resolve_config(section, config_search_paths=CONFIG_FILE_SEARCH_PATHS)


def _resolve_config(section, config_search_paths) -> Optional[Config]:
    # If section specified. Find it in one of the possible configuration file paths
    if section:
        logger.debug("Section [{section}] specified. Searching for config files..")
        config_file = _find_config_file(config_search_paths)

        if config_file is None:
            raise FileNotFoundError(f"Configuration file not found. Searched: {[str(x) for x in config_search_paths]}.")

        logger.debug(f"Found [{config_file}]. Loading the configuration.")
        return _load_from_ini_file(config_file, section)

    # Use env vars if no section specified
    logger.debug("Trying to resolve configuration from environment variables..")
    config = _try_load_from_environment_vars()
    if config:
        logger.debug(f"Configuration resolved from environment variables: {config}.")
        return config

    # Fall back to first section in a config file
    logger.debug("No luck. Searching for a configuration file instead..")
    config_file = _find_config_file(config_search_paths)
    if config_file:
        logger.debug(f"Found [{config_file}]. Loading the configuration from the first section.")
        first_section = _get_first_section(config_file)
        return _load_from_ini_file(config_file, first_section)

    # Found no configs anywhere
    logger.debug(f"Configuration not resolved. Searched for the configuration in env-vars and files. No luck.")
    return None


def _load_from_ini_file(path, section_name) -> Config:
    parser = ConfigParser()
    parser.read(path)

    if section_name not in parser.sections():
        raise ValueError(f"[{section_name}] not found in configuration file.")

    section = parser[section_name]

    if "url" not in section:
        raise ValueError(f"[url] not found in configuration.")

    return Config(section["url"], section.get("api_token"))


def _try_load_from_environment_vars():
    url = os.getenv(QLATTICE_URL_ENV_KEY, None)
    api_token = os.getenv(API_TOKEN_ENV_KEY, None)

    if url:
        return Config(url, api_token)

    return None


def _find_config_file(search_paths):
    existing_config_files = [x for x in search_paths if Path(x).exists()]

    if len(existing_config_files) > 1:
        raise ValueError(f"Multiple configuration files found: {[str(x) for x in existing_config_files]}.")

    if existing_config_files:
        return existing_config_files[0]

    return None


def _get_first_section(path):
    parser = ConfigParser()
    parser.read(path)
    section_names = parser.sections()

    if not section_names:
        raise ValueError(f"No sections found in configuration file.")

    return section_names[0]
