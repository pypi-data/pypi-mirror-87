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
from jerrycan.test.mocks import send_email_mock, verify_recaptcha_mock,\
    generate_random_mock, negative_verify_recaptcha_mock


class TestForgotRoute(_TestFramework):
    """
    Class that tests password reset features
    """

    def test_page_get(self):
        """
        Tests getting the page
        :return: None
        """
        resp = self.client.get("/forgot")
        self.assertTrue(b"<!--user_management/forgot.html-->" in resp.data)

    def test_resetting_password(self):
        """
        Tests successfully resetting a password
        :return: None
        """
        user, password, _ = self.generate_sample_user()

        with self.client:
            with send_email_mock as m:
                with generate_random_mock:
                    with verify_recaptcha_mock:
                        self.assertEqual(0, m.call_count)
                        resp = self.client.post(
                            "/forgot",
                            follow_redirects=True,
                            data={
                                "email": user.email,
                                "g-recaptcha-response": ""
                            }
                        )
                        self.assertEqual(1, m.call_count)

            expected = self.config.STRINGS["password_was_reset"]
            self.assertTrue(expected.encode("utf-8") in resp.data)
            self.assertTrue(b"<!--static/index.html-->" in resp.data)
            self.assertFalse(user.verify_password(password))
            self.assertTrue(user.verify_password("testpass"))

    def test_unsuccessfully_resetting_password(self):
        """
        Tests unsuccessfully resetting a password
        :return: None
        """
        user, password, _ = self.generate_sample_user()
        with self.client:
            with send_email_mock as m:
                with generate_random_mock:
                    with verify_recaptcha_mock:
                        self.assertEqual(0, m.call_count)
                        resp = self.client.post(
                            "/forgot",
                            follow_redirects=True,
                            data={
                                "email": user.email + "AAA",
                                "g-recaptcha-response": ""
                            }
                        )
                        self.assertEqual(0, m.call_count)

            expected = self.config.STRINGS["password_was_reset"]
            self.assertTrue(expected.encode("utf-8") in resp.data)
            self.assertTrue(b"<!--static/index.html-->" in resp.data)
            self.assertTrue(user.verify_password(password))
            self.assertFalse(user.verify_password("testpass"))

    def test_invalid_recaptcha(self):
        """
        Tests that invalid ReCaptcha responses are handled correctly
        :return: None
        """
        user, password, _ = self.generate_sample_user()
        with self.client:
            with send_email_mock as m:
                with generate_random_mock:
                    with negative_verify_recaptcha_mock:
                        self.assertEqual(0, m.call_count)
                        resp = self.client.post(
                            "/forgot",
                            follow_redirects=True,
                            data={
                                "email": user.email,
                                "g-recaptcha-response": ""
                            }
                        )
                        self.assertEqual(0, m.call_count)

            expected = self.config.STRINGS["recaptcha_incorrect"]\
                .encode("utf-8")
            self.assertTrue(expected in resp.data)
            self.assertTrue(b"<!--user_management/forgot.html-->" in resp.data)
            self.assertTrue(user.verify_password(password))
            self.assertFalse(user.verify_password("testpass"))
