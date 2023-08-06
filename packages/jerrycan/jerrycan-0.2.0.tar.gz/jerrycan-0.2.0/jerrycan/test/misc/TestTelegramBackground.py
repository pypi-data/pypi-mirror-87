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
# noinspection PyPackageRequirements
from telegram.error import Conflict
from bokkichat.entities.Address import Address
from bokkichat.entities.message.MediaMessage import MediaMessage, MediaType
from bokkichat.entities.message.TextMessage import TextMessage
from jerrycan.test.TestFramework import _TestFramework
from jerrycan.background.telegram import telegram_whoami


class TestTelegramBackground(_TestFramework):
    """
    Tests the telegram background functions
    """

    def test_whoami(self):
        """
        Tests the whoami functionality
        :return: None
        """
        class DummyConnection:
            address = Address("ABC")
            parent: _TestFramework = self
            create_errors = False
            counter = 0

            def send(self, message: TextMessage):

                if self.create_errors:
                    raise Conflict("Error")

                self.counter += 1

                self.parent.assertEqual(message.sender.address,
                                        self.address.address)
                self.parent.assertEqual(message.body, message.receiver.address)

            def loop(self, handler):
                handler(None, TextMessage(
                    Address("XYZ"),
                    self.address,
                    "/whoami"
                ))
                handler(None, TextMessage(
                    Address("XYZ"),
                    self.address,
                    "Hello"
                ))
                handler(None, MediaMessage(
                    Address("XYZ"),
                    self.address,
                    MediaType.AUDIO,
                    b""
                ))

        connection = DummyConnection()

        class DummyConfig:
            TELEGRAM_BOT_CONNECTION = connection

        with patch("jerrycan.background.telegram.Config", DummyConfig):
            self.assertEqual(connection.counter, 0)
            telegram_whoami()
            self.assertEqual(connection.counter, 1)
            DummyConfig.TELEGRAM_BOT_CONNECTION.create_errors = True
            telegram_whoami()
            self.assertEqual(connection.counter, 1)
