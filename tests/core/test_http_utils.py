"""Tests for http_utils."""

import logging
from unittest import mock

import pytest

from udemy_enroller.http_utils import http_get, http_get_no_redirect, close_session


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


class MockSession:
    def __init__(self, response=None):
        self._response = response or MockResponse()
        self.closed = False

    def get(self, url, headers=None, allow_redirects=None):
        self._get_url = url
        self._get_headers = headers
        self._get_allow_redirects = allow_redirects
        return self._response

    async def close(self):
        self.closed = True


@pytest.fixture(autouse=True)
def mock_sleep():
    """Mock asyncio.sleep to avoid real delays in retry logic."""
    with mock.patch("udemy_enroller.http_utils.asyncio.sleep", return_value=None):
        yield


class TestHttpGet:
    @pytest.mark.asyncio
    async def test_http_get_success(self):
        mock_response = MockResponse(data=b"hello world")
        mock_session = MockSession(response=mock_response)

        with mock.patch("udemy_enroller.http_utils._get_session", return_value=mock_session):
            result = await http_get("https://example.com")
            assert result == b"hello world"

    @pytest.mark.asyncio
    async def test_http_get_with_headers(self):
        mock_response = MockResponse(data=b"ok")
        mock_session = MockSession(response=mock_response)

        with mock.patch("udemy_enroller.http_utils._get_session", return_value=mock_session):
            result = await http_get("https://example.com", headers={"X-Test": "1"})
            assert result == b"ok"

    @pytest.mark.asyncio
    async def test_http_get_exception(self, caplog):
        caplog.set_level(logging.ERROR)

        class FailingSession:
            closed = False

            def get(self, url, headers=None):
                raise RuntimeError("connection failed")

            async def close(self):
                self.closed = True

        with mock.patch("udemy_enroller.http_utils._get_session", return_value=FailingSession()):
            result = await http_get("https://example.com")
            assert result is None
            assert "Request to https://example.com failed" in caplog.text


class TestHttpGetNoRedirect:
    @pytest.mark.asyncio
    async def test_http_get_no_redirect_success(self):
        mock_response = MockResponse(data=b"redirect", headers={"Location": "https://other.com"})
        mock_session = MockSession(response=mock_response)

        with mock.patch("udemy_enroller.http_utils._get_session", return_value=mock_session):
            result = await http_get_no_redirect("https://example.com")
            assert result == {"Location": "https://other.com"}

    @pytest.mark.asyncio
    async def test_http_get_no_redirect_with_headers(self):
        headers = {"X-Custom": "value"}
        mock_response = MockResponse(data=b"ok", headers={"Content-Type": "text/plain"})
        mock_session = MockSession(response=mock_response)

        with mock.patch("udemy_enroller.http_utils._get_session", return_value=mock_session):
            result = await http_get_no_redirect("https://example.com", headers=headers)
            assert result == {"Content-Type": "text/plain"}

    @pytest.mark.asyncio
    async def test_http_get_no_redirect_exception(self, caplog):
        caplog.set_level(logging.ERROR)

        class FailingSession:
            closed = False

            def get(self, url, headers=None, allow_redirects=None):
                raise RuntimeError("connection failed")

            async def close(self):
                self.closed = True

        with mock.patch("udemy_enroller.http_utils._get_session", return_value=FailingSession()):
            result = await http_get_no_redirect("https://example.com")
            assert result is None
            assert "Request to https://example.com failed" in caplog.text


class TestCloseSession:
    @pytest.mark.asyncio
    async def test_close_session(self):
        import udemy_enroller.http_utils as http_utils
        mock_session = MockSession()
        mock_connector = mock.AsyncMock()
        mock_connector.closed = False

        http_utils._SESSION = mock_session
        http_utils._CONNECTOR = mock_connector
        await close_session()
        assert mock_session.closed
        assert http_utils._SESSION is None

    @pytest.mark.asyncio
    async def test_close_session_no_session(self):
        import udemy_enroller.http_utils as http_utils
        http_utils._SESSION = None
        http_utils._CONNECTOR = None
        await close_session()
        # Should not raise
