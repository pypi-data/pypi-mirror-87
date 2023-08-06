"""LICENSE
Copyright 2020 Hermann Krumrey <hermann@krumreyh.com>

This file is part of jerrycan.

jerrycan is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

jerrycan is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with jerrycan.  If not, see <http://www.gnu.org/licenses/>.
LICENSE"""

import os
import pathlib
from unittest.mock import patch
from jerrycan.test.TestFramework import _TestFramework
from jerrycan.Config import Config


class TestConfig(_TestFramework):
    """
    Class that tests the config class
    """

    def test_db_config(self):
        """
        Tests the database configuration
        :return: None
        """
        os.environ.pop("FLASK_TESTING")
        os.environ["DB_MODE"] = "sqlite"
        Config.load_config(self.root_path, "jerrycan", "sentry_dsn")
        self.assertEqual(Config.DB_URI, "sqlite:////tmp/jerrycan.db")
        os.environ["SQLITE_PATH"] = "/tmp/test.db"
        Config.load_config(self.root_path, "jerrycan", "sentry_dsn")
        self.assertEqual(Config.DB_URI, "sqlite:////tmp/test.db")

        os.environ["DB_MODE"] = "mysql"
        os.environ["MYSQL_USER"] = "abc"
        os.environ["MYSQL_PASSWORD"] = "def"
        os.environ["MYSQL_HOST"] = "ghi"
        os.environ["MYSQL_PORT"] = "1000"
        os.environ["MYSQL_DATABASE"] = "xyz"
        Config.load_config(self.root_path, "jerrycan", "sentry_dsn")
        self.assertEqual(Config.DB_URI, "mysql://abc:def@ghi:1000/xyz")
        os.environ["DB_MODE"] = "postgresql"
        os.environ["POSTGRES_USER"] = "ABC"
        os.environ["POSTGRES_PASSWORD"] = "DEF"
        os.environ["POSTGRES_HOST"] = "GHI"
        os.environ["POSTGRES_PORT"] = "2000"
        os.environ["POSTGRES_DATABASE"] = "XYZ"

        try:
            Config.load_config(self.root_path, "jerrycan", "sentry_dsn")
            self.fail()
        except SystemExit:
            pass

        os.environ["POSTGRES_DB"] = "XYZ"

        Config.load_config(self.root_path, "jerrycan", "sentry_dsn")
        self.assertEqual(Config.DB_URI, "postgresql://ABC:DEF@GHI:2000/XYZ")

    def test_version(self):
        """
        Tests if the version is fetched correctly
        :return: None
        """
        version_file = os.path.join(
            pathlib.Path(__file__).parent.absolute(),
            "../../../../jerrycan/version"
        )
        with open(version_file, "r") as f:
            version = f.read()
        self.assertEqual(version, Config.VERSION)

    def test_environment_variables_definitions(self):
        """
        Tests the definition of the environent variables
        :return: None
        """
        if "DB_MODE" in os.environ:
            os.environ.pop("DB_MODE")
        variables = Config.environment_variables()
        first_required = variables["required"]
        first_optional = variables["optional"]
        self.assertTrue("FLASK_SECRET" in first_required)
        self.assertFalse("SQLITE_PATH" in first_optional)
        self.assertFalse("MYSQL_USER" in first_required)
        self.assertFalse("MYSQL_DATABASE" in first_required)
        self.assertFalse("MYSQL_DB" in first_required)
        self.assertFalse("POSTGRES_USER" in first_required)
        self.assertFalse("POSTGRES_DATABASE" in first_required)
        self.assertFalse("POSTGRES_DB" in first_required)
        self.assertTrue("LOGGING_PATH" in first_optional)

        os.environ["DB_MODE"] = "sqlite"
        variables = Config.environment_variables()
        required = variables["required"]
        optional = variables["optional"]
        self.assertEqual(first_required, required)
        self.assertNotEqual(first_optional, optional)
        self.assertTrue("SQLITE_PATH" in optional)
        self.assertFalse("MYSQL_USER" in required)
        self.assertFalse("MYSQL_DATABASE" in required)
        self.assertFalse("MYSQL_DB" in required)
        self.assertFalse("POSTGRES_USER" in required)
        self.assertFalse("POSTGRES_DATABASE" in required)
        self.assertFalse("POSTGRES_DB" in required)

        os.environ["DB_MODE"] = "mysql"
        variables = Config.environment_variables()
        required = variables["required"]
        optional = variables["optional"]
        self.assertNotEqual(first_required, required)
        self.assertEqual(first_optional, optional)
        self.assertFalse("SQLITE_PATH" in optional)
        self.assertTrue("MYSQL_USER" in required)
        self.assertTrue("MYSQL_DATABASE" in required)
        self.assertFalse("MYSQL_DB" in required)
        self.assertFalse("POSTGRES_USER" in required)
        self.assertFalse("POSTGRES_DATABASE" in required)
        self.assertFalse("POSTGRES_DB" in required)

        os.environ["DB_MODE"] = "postgresql"
        variables = Config.environment_variables()
        required = variables["required"]
        optional = variables["optional"]
        self.assertNotEqual(first_required, required)
        self.assertEqual(first_optional, optional)
        self.assertFalse("SQLITE_PATH" in optional)
        self.assertFalse("MYSQL_USER" in required)
        self.assertFalse("MYSQL_DATABASE" in required)
        self.assertFalse("MYSQL_DB" in required)
        self.assertTrue("POSTGRES_USER" in required)
        self.assertFalse("POSTGRES_DATABASE" in required)
        self.assertTrue("POSTGRES_DB" in required)

    def test_dumping_environment_variables(self):
        """
        Tests dumping environment variables
        :return: None
        """
        dumpfile = "/tmp/envdump"
        os.environ["FLASK_SECRET"] = "ABCXYZ"
        Config.dump_env_variables(dumpfile)

        def verify(output: str):
            with open(dumpfile, "r") as f:
                self.assertEqual(output, f.read())

        with patch("builtins.print", verify):
            Config.dump_env_variables()

    def test_building_base_url(self):
        """
        Tests building the base URL
        :return: None
        """
        os.environ["DOMAIN_NAME"] = "example.org"
        os.environ["HTTP_PORT"] = "1000"
        os.environ["BEHIND_PROXY"] = "0"
        Config.load_config(self.root_path, "jerrycan", "sentry_dsn")
        self.assertEqual(Config.base_url(), "http://example.org:1000")

        os.environ["BEHIND_PROXY"] = "1"
        Config.load_config(self.root_path, "jerrycan", "sentry_dsn")
        self.assertEqual(Config.base_url(), "https://example.org")

    def test_initializing_telegram_bot_connection(self):
        """
        'Tests' initializing the telegram bot connection
        :return: None
        """
        class DummyBot:
            def __init__(self, settings):
                self.settings = settings

        os.environ["TELEGRAM_API_KEY"] = "ABC"
        Config.load_config(self.root_path, "jerrycan", "sentry_dsn")

        try:
            self.assertIsNone(Config.TELEGRAM_BOT_CONNECTION)
            self.fail()
        except AttributeError:
            pass

        with patch("jerrycan.Config.TelegramBotConnection", DummyBot):
            Config.initialize_telegram()
        self.assertIsNotNone(Config.TELEGRAM_BOT_CONNECTION)
