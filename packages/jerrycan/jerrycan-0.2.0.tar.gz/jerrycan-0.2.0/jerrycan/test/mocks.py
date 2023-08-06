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

from unittest.mock import patch

verify_recaptcha_mock = patch("jerrycan.routes.user_management."
                              "verify_recaptcha",
                              lambda x, y, z: True)
negative_verify_recaptcha_mock = patch("jerrycan.routes.user_management."
                                       "verify_recaptcha",
                                       lambda x, y, z: False)
send_email_mock = patch("jerrycan.routes.user_management.send_email")
generate_random_mock = patch("jerrycan.routes.user_management.generate_random",
                             lambda x: "testpass")
