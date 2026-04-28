"""HTTP helpers with session reuse and retry/backoff."""

import asyncio
import random
from typing import Any

import aiohttp

from udemy_enroller.logger import get_logger

logger = get_logger()

_SESSION: aiohttp.ClientSession | None = None
_CONNECTOR: aiohttp.TCPConnector | None = None

MAX_RETRIES = 3
BASE_DELAY = 1.0


def _get_connector() -> aiohttp.TCPConnector:
    """Get or create the shared TCP connector."""
    global _CONNECTOR
    if _CONNECTOR is None or _CONNECTOR.closed:
        _CONNECTOR = aiohttp.TCPConnector(limit=10, force_close=False)
    return _CONNECTOR


def _get_session() -> aiohttp.ClientSession:
    """Get or create the shared aiohttp session."""
    global _SESSION
    if _SESSION is None or _SESSION.closed:
        _SESSION = aiohttp.ClientSession(connector=_get_connector())
    return _SESSION


async def close_session() -> None:
    """Close the shared session and connector."""
    global _SESSION, _CONNECTOR
    if _SESSION is not None and not _SESSION.closed:
        await _SESSION.close()
        _SESSION = None
    if _CONNECTOR is not None and not _CONNECTOR.closed:
        await _CONNECTOR.close()
        _CONNECTOR = None


async def http_get(url: str, headers: dict[str, Any] | None = None) -> bytes | None:
    """
    Send GET request with retry/backoff and session reuse.

    :param url: The URL to send GET request to
    :param headers: Optional headers to pass with the request
    :return: Response bytes or None on failure
    """
    if headers is None:
        headers = {}
    session = _get_session()
    for attempt in range(MAX_RETRIES):
        try:
            async with session.get(url, headers=headers) as response:
                return await response.read()
        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                delay = BASE_DELAY * (2 ** attempt) + random.uniform(0, 0.5)
                logger.warning(
                    f"Request to {url} failed (attempt {attempt + 1}/{MAX_RETRIES}): {e}. "
                    f"Retrying in {delay:.1f}s..."
                )
                await asyncio.sleep(delay)
            else:
                logger.error(f"Request to {url} failed after {MAX_RETRIES} attempts: {e}")
    return None


async def http_get_no_redirect(
    url: str, headers: dict[str, Any] | None = None
) -> Any | None:
    """
    Send GET request without following redirects.

    :param url: The URL to send GET request to
    :param headers: Optional headers to pass with the request
    :return: Response object or None on failure
    """
    if headers is None:
        headers = {}
    session = _get_session()
    for attempt in range(MAX_RETRIES):
        try:
            async with session.get(
                url, headers=headers, allow_redirects=False
            ) as response:
                return response
        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                delay = BASE_DELAY * (2 ** attempt) + random.uniform(0, 0.5)
                logger.warning(
                    f"Request to {url} failed (attempt {attempt + 1}/{MAX_RETRIES}): {e}. "
                    f"Retrying in {delay:.1f}s..."
                )
                await asyncio.sleep(delay)
            else:
                logger.error(f"Request to {url} failed after {MAX_RETRIES} attempts: {e}")
    return None
