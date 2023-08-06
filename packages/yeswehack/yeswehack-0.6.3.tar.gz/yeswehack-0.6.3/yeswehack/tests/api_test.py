#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import sys
import os

# add yeswehack lib to sys path
import unittest
from unittest import mock
from yeswehack import api
import inspect
import json

from yeswehack.exceptions import (
    APIError,
    InvalidResponse,
    BadCredentials,
    JWTNotFound,
    JWTInvalid,
)


class TestApi(unittest.TestCase):

    ywh = None
    current_dir = os.path.dirname(os.path.realpath(__file__))

    def setUp(self):
        self.ywh = api.YesWeHack(
            username="hunter"
        )

    def get_mock_data(self, func_name):
        mock_data_filename = (
            self.current_dir + "/mock/" + func_name + ".content"
        )
        with open(mock_data_filename, "r") as json_file:
            mock_json = json.load(json_file)
        return mock_json

    def test_bad_login(self):
        func_name = inspect.stack()[0][3]
        with mock.patch("yeswehack.api.requests.sessions.Session.request") as mock_request:
            mock_request.return_value.status_code = 401
            mock_request.return_value.json.return_value = self.get_mock_data(
                func_name
            )
            self.assertRaises(BadCredentials, self.ywh.login)

    def test_login(self):
        func_name = inspect.stack()[0][3]
        with mock.patch("yeswehack.api.requests.sessions.Session.request") as mock_request:
            mock_request.return_value.status_code = 200
            mock_request.return_value.json.return_value = self.get_mock_data(
                func_name
            )
            res = self.ywh.login()
        self.assertEqual(self.ywh.token, "test_token")

    def test_get_bu(self):
        func_name = inspect.stack()[0][3]
        with mock.patch("yeswehack.api.requests.sessions.Session.request") as mock_request:
            mock_request.return_value.status_code = 200
            mock_request.return_value.json.return_value = self.get_mock_data(
                func_name
            )
            res = self.ywh.get_business_units()
        self.assertEqual(res[0]["currency"], "EUR")

    def test_get_pgm(self):
        func_name = inspect.stack()[0][3]
        with mock.patch("yeswehack.api.requests.sessions.Session.request") as mock_request:
            mock_request.return_value.status_code = 200
            mock_request.return_value.json.return_value = self.get_mock_data(
                func_name
            )
            res = self.ywh.get_programs("bu")
        self.assertEqual(res[0].slug, "test-pgm")

    def test_get_report(self):
        func_name = inspect.stack()[0][3]
        mock_data = self.get_mock_data(func_name)

        def session_mock(_, method, url, **kwargs):
            if method == "GET":
                if url == "https://api.yeswehack.com/reports/2":
                    request_mock = mock.MagicMock(name="request")
                    request_mock.return_value.status_code = 200
                    request_mock.return_value.json.return_value = mock_data
                    return request_mock()
                if url == "https://api.yeswehack.com/reports/2/logs":
                    request_mock = mock.MagicMock(name="request")
                    request_mock.return_value.status_code = 200
                    request_mock.return_value.json.return_value = {"items": []}
                    return request_mock()
                if url.startswith("https://files.ywh.docker.local"):
                    request_mock = mock.MagicMock(name="request")
                    request_mock.return_value.status_code = 200
                    request_mock.return_value.content = bytes("Binary content for " + url, encoding="utf-8")
                    return request_mock()
            raise Exception(f"Unexpected test case for session request {method} {url}")

        with mock.patch("yeswehack.api.requests.sessions.Session.request", side_effect=session_mock, autospec=True):
            res = self.ywh.get_report(2)
        self.assertEqual(res.title, "test report")


if __name__ == "__main__":
    unittest.main(module="api_test")
