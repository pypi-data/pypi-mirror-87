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
from sqlalchemy.exc import OperationalError
from unittest.mock import patch
from jerrycan.initialize import init_flask
from jerrycan.test.TestFramework import _TestFramework


class TestInitialization(_TestFramework):
    """
    Tests the initialization of the flask application
    """

    def test_missing_environment_variables(self):
        """
        Tests if missing environment variables are detected correctly
        :return: None
        """
        os.environ.pop("FLASK_SECRET")
        try:
            init_flask("jerrycan", "", "", self.config, [], [])
            self.fail()
        except SystemExit:
            pass

    def test_missing_required_template(self):
        """
        Tests if missing template files are detected correctly
        :return: None
        """
        for required in self.config.REQUIRED_TEMPLATES.values():
            path = os.path.join(self.temp_templates_dir, required)
            os.remove(path)
            try:
                init_flask("jerrycan", "", "", self.config, [], [])
                self.fail()
            except SystemExit:
                with open(path, "w") as f:
                    f.write("")

    def test_no_extra_jinja(self):
        """
        Tests if not providing any additional jinja variables works as intended
        :return: None
        """
        init_flask("jerrycan", "", "", self.config, [], [])

    def test_db_connection_error(self):
        """
        Tests if a database connection error is handled correctly
        :return: None
        """
        class MockDb:
            @staticmethod
            def create_all():
                raise OperationalError("a", "a", "a")

            @staticmethod
            def init_app(app):
                pass

        with patch("jerrycan.initialize.db", MockDb):
            try:
                init_flask("jerrycan", "", "", self.config, [], [])
                self.fail()
            except SystemExit:
                pass
