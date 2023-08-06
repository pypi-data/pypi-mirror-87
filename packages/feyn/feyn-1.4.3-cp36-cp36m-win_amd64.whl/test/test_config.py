import tempfile
import unittest
from unittest.mock import patch

from feyn._config import _resolve_config


@patch.dict('os.environ', {}, clear=True)
class TestConfig(unittest.TestCase):

    def test_resolve_returns_none_when_env_vars_and_config_not_present(self):
        self.assertIsNone(_resolve_config(section=None, config_search_paths=[]))


@patch.dict('os.environ', {}, clear=True)
class TestConfig_WithEnvironmentVars(unittest.TestCase):

    def test_resolve_loads_from_env_vars(self):
        env = {
            "FEYN_QLATTICE_URL": "my-url",
            "FEYN_QLATTICE_API_TOKEN": "my-token"
        }

        with patch.dict('os.environ', env):
            config = _resolve_config(section=None, config_search_paths=[])

            self.assertEqual(config.url, "my-url")
            self.assertEqual(config.api_token, "my-token")


@patch.dict('os.environ', {}, clear=True)
class TestConfig_WithConfigFiles(unittest.TestCase):
    def setUp(self):
        self.test_config_file = tempfile.NamedTemporaryFile()

    def tearDown(self):
        # Clean up temp config file
        if self.test_config_file:
            self.test_config_file.close()

    def test_resolve_section_in_config_file(self):
        _write_config(self.test_config_file,
        """
        [Section1]
        url = section1-url
        api_token = section1-token

        [Section2]
        url = section2-url
        api_token = section2-token
        """)

        config = _resolve_config(section="Section2",
                                 config_search_paths=[self.test_config_file.name])

        self.assertEqual(config.url, "section2-url")
        self.assertEqual(config.api_token, "section2-token")

    def test_resolve_when_section_not_specified_uses_first_section_in_config(self):
        _write_config(self.test_config_file,
        """
        [Section1]
        url = section1-url
        api_token = section1-token

        [Section2]
        url = section2-url
        api_token = section2-token
        """)

        config = _resolve_config(section=None,
                                 config_search_paths=[self.test_config_file.name])

        self.assertEqual(config.url, "section1-url")
        self.assertEqual(config.api_token, "section1-token")

    def test_resolve_uses_section_even_if_env_vars_exist(self):
        _write_config(self.test_config_file,
        """
        [Section1]
        url = section1-url
        api_token = section1-token
        """)

        env = {
            "FEYN_QLATTICE_URL": "env-url",
            "FEYN_QLATTICE_API_TOKEN": "env-token"
        }

        with patch.dict('os.environ', env):
            config = _resolve_config("Section1",
                                     config_search_paths=[self.test_config_file.name])

            self.assertEqual(config.url, "section1-url")
            self.assertEqual(config.api_token, "section1-token")

    def test_resolve_raises_when_config_file_missing(self):
        # It is a temporary file that will be deleted upon close
        self.test_config_file.close()

        with self.assertRaises(FileNotFoundError) as ctx:
            _resolve_config(section="MonkeyViruses",
                            config_search_paths=[self.test_config_file.name])

        # Ensure we tell the user which files we have looked for.
        self.assertRegex(str(ctx.exception), self.test_config_file.name)

    def test_resolve_raises_when_specified_section_missing(self):
        _write_config(self.test_config_file,
        """
        [MouseExperiments]
        url = mouse-url
        api_token = mouse-token
        """)

        with self.assertRaisesRegex(ValueError, "NonExistingSection"):
            _resolve_config(section="NonExistingSection",
                            config_search_paths=[self.test_config_file.name])

    def test_resolve_raises_when_section_is_malformatted(self):
        _write_config(self.test_config_file,
        """
        [MissingUrl]
        api_token = mouse-token
        """)

        with self.assertRaisesRegex(ValueError, "url"):
            _resolve_config("MissingUrl",
                            config_search_paths=[self.test_config_file.name])

    def test_resolve_raises_when_multiple_configuration_files_found(self):
        self.test_config_file.close()

        # Emulate that both an rc and .ini file is found
        rc_file = tempfile.NamedTemporaryFile()
        ini_file = tempfile.NamedTemporaryFile()

        _write_config(rc_file,
        """
        [MouseExperiments]
        url = mouse-url
        api_token = mouse-token
        """)

        _write_config(ini_file,
        """
        [MouseExperiments]
        url = mouse-url
        api_token = mouse-token
        """)

        with self.assertRaisesRegex(ValueError, "Multiple configuration files"):
            _resolve_config("MouseExperiments",
                            config_search_paths=[rc_file.name,
                                                 ini_file.name]
            )


def _write_config(file, cfg: str):
    file.write(cfg.encode())
    file.seek(0)
