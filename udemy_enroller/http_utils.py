"""HTTP helpers."""
import aiohttp
from udemy_enroller.types import HttpRequestFailed, Result

from udemy_enroller.logger import get_logger

logger = get_logger()


async def http_get(url, headers=None, timeout: int = 15) -> Result[bytes, HttpRequestFailed]:
    """
    Send REST get request to the url passed in.

    :param url: The Url to get call get request on
    :param headers: The headers to pass with the get request
    :return: data if any exists
    """
    if headers is None:
        headers = {}
    try:
        client_timeout = aiohttp.ClientTimeout(total=timeout)
        async with aiohttp.ClientSession(timeout=client_timeout) as session:
            async with session.get(url, headers=headers) as response:
                if response.status >= 400:
                    retryable = 500 <= response.status < 600
                    if response.status in (403, 404):
                        retryable = False
                    err = HttpRequestFailed(url=url, status=response.status, reason=response.reason, retryable=retryable)
                    logger.error(f"GET {url} failed with status {response.status}")
                    return Result(ok=False, error=err)
                text = await response.read()
                return Result(ok=True, value=text)
    except Exception as e:
        err = HttpRequestFailed(url=url, status=None, reason=str(e), retryable=True)
        logger.error(f"Error in get request: {e}")
        return Result(ok=False, error=err)
