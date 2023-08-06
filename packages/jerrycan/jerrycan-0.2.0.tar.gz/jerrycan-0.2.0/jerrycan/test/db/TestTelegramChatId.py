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
from bokkichat.entities.Address import Address
from bokkichat.entities.message.TextMessage import TextMessage
from jerrycan.test.TestFramework import _TestFramework


class TestTelegramChatId(_TestFramework):
    """
    Class that tests the TelegramChatId database model
    """

    def test_json_representation(self):
        """
        Tests the JSON representation of the model
        :return: None
        """
        user = self.generate_sample_user()[0]
        chat_id = self.generate_telegram_chat_id(user)
        self.assertEqual(
            chat_id.__json__(False),
            {
                "id": chat_id.id,
                "user_id": user.id,
                "chat_id": chat_id.chat_id
            }
        )
        user_json = user.__json__(True)
        user_json.pop("telegram_chat_id")
        self.assertEqual(
            chat_id.__json__(True),
            {
                "id": chat_id.id,
                "user_id": user.id,
                "user": user_json,
                "chat_id": chat_id.chat_id
            }
        )

    def test_string_representation(self):
        """
        Tests the string representation of the model
        :return: None
        """
        user = self.generate_sample_user()[0]
        chat_id = self.generate_telegram_chat_id(user)
        data = chat_id.__json__()
        data.pop("id")
        self.assertEqual(
            str(chat_id),
            "TelegramChatId:{} <{}>".format(chat_id.id, data)
        )

    def test_repr(self):
        """
        Tests the __repr__ method of the model class
        :return: None
        """
        user = self.generate_sample_user()[0]
        chat_id = self.generate_telegram_chat_id(user)
        generated = {"value": chat_id}
        code = repr(chat_id)

        # noinspection PyUnresolvedReferences
        from jerrycan.db.TelegramChatId import TelegramChatId
        exec("generated['value'] = " + code)
        self.assertEqual(generated["value"], chat_id)
        self.assertFalse(generated["value"] is chat_id)

    def test_hashing(self):
        """
        Tests using the model objects as keys in a dictionary
        :return: None
        """
        user = self.generate_sample_user()[0]
        user2 = self.generate_sample_user()[0]
        chat_id = self.generate_telegram_chat_id(user)
        chat_id2 = self.generate_telegram_chat_id(user2)
        mapping = {
            chat_id: 100,
            chat_id2: 200
        }
        self.assertEqual(mapping[chat_id], 100)
        self.assertEqual(mapping[chat_id2], 200)

    def test_equality(self):
        """
        Tests checking equality for model objects
        :return: None
        """
        user = self.generate_sample_user()[0]
        user2 = self.generate_sample_user()[0]
        chat_id = self.generate_telegram_chat_id(user)
        chat_id2 = self.generate_telegram_chat_id(user2)
        self.assertEqual(chat_id, chat_id)
        self.assertNotEqual(chat_id, chat_id2)
        self.assertNotEqual(chat_id, 100)

    def test_sending_message(self):
        """
        Tests sending a message
        :return: None
        """
        user = self.generate_sample_user()[0]
        chat_id = self.generate_telegram_chat_id(user)

        class DummyConnection:
            address = Address("ABC")
            parent: _TestFramework = self

            def send(self, message: TextMessage):
                self.parent.assertEqual(message.sender.address,
                                        self.address.address)
                self.parent.assertEqual(message.receiver.address,
                                        chat_id.chat_id)
                self.parent.assertEqual(message.body, "XYZ")

        class DummyConfig:
            TELEGRAM_BOT_CONNECTION = DummyConnection()

        with patch("jerrycan.db.TelegramChatId.Config", DummyConfig):
            chat_id.send_message("XYZ")
