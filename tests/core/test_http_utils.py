"""Tests for http_utils."""

import logging
from unittest import mock

import pytest
from aiohttp import ClientSession

from udemy_enroller.http_utils import http_get, http_get_no_redirect


class MockResponse:
    def __init__(self, data=b"", status=200, headers=None):
        self._data = data
        self.status = status
        self.headers = headers or {}

    async def read(self):
        return self._data

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def __aenter__(self):
        return self


class MockClientSession:
    def __init__(self, response=None):
        self._response = response or MockResponse()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass

    def get(self, url, headers=None, allow_redirects=None):
        self._get_url = url
        self._get_headers = headers
        self._get_allow_redirects = allow_redirects
        return self._response


class TestHttpGet:
    @pytest.mark.asyncio
    async def test_http_get_success(self):
        mock_response = MockResponse(data=b"hello world")
        mock_session = MockClientSession(response=mock_response)

        with mock.patch("udemy_enroller.http_utils.aiohttp.ClientSession", return_value=mock_session):
            result = await http_get("https://example.com")
            assert result == b"hello world"

    @pytest.mark.asyncio
    async def test_http_get_with_headers(self):
        mock_response = MockResponse(data=b"ok")
        mock_session = MockClientSession(response=mock_response)

        with mock.patch("udemy_enroller.http_utils.aiohttp.ClientSession", return_value=mock_session):
            result = await http_get("https://example.com", headers={"X-Test": "1"})
            assert result == b"ok"

    @pytest.mark.asyncio
    async def test_http_get_exception(self, caplog):
        caplog.set_level(logging.ERROR)

        class FailingSession:
            async def __aenter__(self):
                return self

            async def __aexit__(self, exc_type, exc, tb):
                pass

            def get(self, url, headers=None):
                raise RuntimeError("connection failed")

        with mock.patch("udemy_enroller.http_utils.aiohttp.ClientSession", return_value=FailingSession()):
            result = await http_get("https://example.com")
            assert result is None
            assert "Error in get request" in caplog.text


class TestHttpGetNoRedirect:
    @pytest.mark.asyncio
    async def test_http_get_no_redirect_success(self):
        mock_response = MockResponse(data=b"redirect", headers={"Location": "https://other.com"})
        mock_session = MockClientSession(response=mock_response)

        with mock.patch("udemy_enroller.http_utils.aiohttp.ClientSession", return_value=mock_session):
            result = await http_get_no_redirect("https://example.com")
            assert result == mock_response

    @pytest.mark.asyncio
    async def test_http_get_no_redirect_with_headers(self):
        headers = {"X-Custom": "value"}
        mock_response = MockResponse(data=b"ok")
        mock_session = MockClientSession(response=mock_response)

        with mock.patch("udemy_enroller.http_utils.aiohttp.ClientSession", return_value=mock_session):
            result = await http_get_no_redirect("https://example.com", headers=headers)
            assert result == mock_response

    @pytest.mark.asyncio
    async def test_http_get_no_redirect_exception(self, caplog):
        caplog.set_level(logging.ERROR)

        class FailingSession:
            async def __aenter__(self):
                return self

            async def __aexit__(self, exc_type, exc, tb):
                pass

            def get(self, url, headers=None, allow_redirects=None):
                raise RuntimeError("connection failed")

        with mock.patch("udemy_enroller.http_utils.aiohttp.ClientSession", return_value=FailingSession()):
            result = await http_get_no_redirect("https://example.com")
            assert result is None
            assert "Error in get request" in caplog.text
