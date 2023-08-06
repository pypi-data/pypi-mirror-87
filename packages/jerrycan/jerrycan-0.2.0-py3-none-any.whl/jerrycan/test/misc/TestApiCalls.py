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

import json
from unittest.mock import patch
from flask.blueprints import Blueprint
from jerrycan.routes.decorators import api
from jerrycan.test.TestFramework import _TestFramework


class TestApiCalls(_TestFramework):
    """
    Class that tests various API calls
    """

    def test_unauthorized_call(self):
        """
        Tests and unauthorized API call
        :return: None
        """
        api_headers = self.generate_api_key_headers("1:100")
        resp = self.client.get(
            "/api/v1/authorize", headers=api_headers, json={}
        )
        self.assertEqual(resp.status_code, 401)
        data = json.loads(resp.data.decode("utf-8"))
        self.assertEqual(data["status"], "error")
        self.assertEqual(data["reason"], "unauthorized")

    def test_non_base64_header(self):
        """
        Tests using a header that's not base64 encoded
        :return: None
        """
        user, _, _ = self.generate_sample_user()
        _, api_key, _ = self.generate_api_key(user)
        resp = self.client.get(
            "/api/v1/authorize",
            headers={"Authorization": "Basic " + api_key},
            json={}
        )
        self.assertEqual(resp.status_code, 401)
        data = json.loads(resp.data.decode("utf-8"))
        self.assertEqual(data["status"], "error")
        self.assertEqual(data["reason"], "unauthorized")

    def test_expired_api_key(self):
        """
        Tests using an expired API key
        :return: None
        """
        user, _, _ = self.generate_sample_user()
        api_key_obj, api_key, _ = self.generate_api_key(user)

        api_key_obj.creation_time = 0
        self.db.session.commit()

        api_headers = self.generate_api_key_headers(api_key)
        resp = self.client.get(
            "/api/v1/authorize", headers=api_headers, json={}
        )
        self.assertEqual(resp.status_code, 401)
        data = json.loads(resp.data.decode("utf-8"))
        self.assertEqual(data["status"], "error")
        self.assertEqual(data["reason"], "unauthorized")

    def test_using_non_json_data(self):
        """
        Tests sending the data as something that's not JSON
        :return: None
        """
        user, password, _ = self.generate_sample_user()
        resp = self.client.post("/api/v1/key", data={
            "username": user.username,
            "password": password
        })
        self.assertEqual(resp.status_code, 400)
        data = json.loads(resp.data.decode("utf-8"))
        self.assertEqual(data["status"], "error")
        self.assertEqual(data["reason"], "not in json format")

    def test_random_exception(self):
        """
        Tests that the API routes catch any Exceptions without issue
        :return: None
        """
        class Mocker:
            @staticmethod
            def get_json():
                print({}["test"])

        with patch("jerrycan.routes.api.user_management.request",
                   Mocker):
            user, password, _ = self.generate_sample_user()
            resp = self.client.post("/api/v1/key", json={
                "username": user.username,
                "password": password
            })
            self.assertEqual(resp.status_code, 400)
            data = json.loads(resp.data.decode("utf-8"))
            self.assertEqual(data["status"], "error")
            self.assertEqual(data["reason"], "bad request: KeyError")

    def test_exception_in_api_route(self):
        """
        Tests if an exeption on an API route is correctly wrapped
        in a JSON response
        :return: None
        """
        bp = Blueprint("exceptiontest", __name__)

        @bp.route("/api/exception", methods=["GET"])
        @api
        def exception_route():
            return f"{1/0}"

        self.app.register_blueprint(bp)
        resp = self.client.get("/api/exception")
        self.assertEqual(resp.status_code, 500)
