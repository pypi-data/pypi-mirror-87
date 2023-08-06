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

from jerrycan.test.TestFramework import _TestFramework
from jerrycan.db.TelegramChatId import TelegramChatId


class TestRegisterTelegramRoute(_TestFramework):
    """
    Class that tests the route used to register telegram chat IDs
    """

    def test_registering(self):
        """
        Tests registering a telegram chat ID
        :return: None
        """
        user, password, _ = self.generate_sample_user()
        self.assertEqual(len(TelegramChatId.query.all()), 0)
        with self.client:
            self.login_user(user, password)
            self.client.post("/register_telegram",
                             data={"telegram_chat_id": 12345})
            self.assertEqual(len(TelegramChatId.query.all()), 1)
            self.client.post("/register_telegram",
                             data={"telegram_chat_id": 67890})
            self.assertEqual(len(TelegramChatId.query.all()), 1)
