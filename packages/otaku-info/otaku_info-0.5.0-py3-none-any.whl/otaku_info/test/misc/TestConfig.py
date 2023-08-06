"""LICENSE
Copyright 2020 Hermann Krumrey <hermann@krumreyh.com>

This file is part of otaku-info.

otaku-info is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

otaku-info is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with otaku-info.  If not, see <http://www.gnu.org/licenses/>.
LICENSE"""

import os
import pathlib
from otaku_info import sentry_dsn
from otaku_info.test.TestFramework import _TestFramework
from otaku_info.Config import Config


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
        os.environ["DB_MODE"] = "mysql"
        os.environ["MYSQL_USER"] = "abc"
        os.environ["MYSQL_PASSWORD"] = "def"
        os.environ["MYSQL_HOST"] = "ghi"
        os.environ["MYSQL_PORT"] = "1000"
        os.environ["MYSQL_DATABASE"] = "xyz"
        Config.load_config(self.root_path, "otaku_info", sentry_dsn)
        self.assertEqual(Config.DB_URI, "mysql://abc:def@ghi:1000/xyz")

    def test_version(self):
        """
        Tests if the version is fetched correctly
        :return: None
        """
        version_file = os.path.join(
            pathlib.Path(__file__).parent.absolute(),
            "../../../version"
        )
        with open(version_file, "r") as f:
            version = f.read()
        self.assertEqual(version, Config.VERSION)
