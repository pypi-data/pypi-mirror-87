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

from unittest.mock import patch
from jerrycan.test.mocks import send_email_mock, verify_recaptcha_mock, \
    negative_verify_recaptcha_mock, generate_random_mock
from otaku_info.test.TestFramework import _TestFramework


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

            self.assertTrue(b"Password was reset successfully" in resp.data)
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

            self.assertTrue(b"Password was reset successfully" in resp.data)
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

            self.assertTrue(b"ReCaptcha not solved correctly" in resp.data)
            self.assertTrue(b"<!--user_management/forgot.html-->" in resp.data)
            self.assertTrue(user.verify_password(password))
            self.assertFalse(user.verify_password("testpass"))
