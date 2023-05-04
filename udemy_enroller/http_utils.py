"""HTTP helpers."""
import aiohttp

from udemy_enroller.logger import get_logger

logger = get_logger()


async def http_get(url, headers=None):
    """
    Send REST get request to the url passed in.

    :param url: The Url to get call get request on
    :param headers: The headers to pass with the get request
    :return: data if any exists
    """
    if headers is None:
        headers = {}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                text = await response.read()
                return text
    except Exception as e:
        logger.error(f"Error in get request: {e}")


async def http_get_no_redirect(url, headers=None):
    """
    Send REST get request to the url passed in but doesn't follow redirect.

    :param url: The Url to get call get request on
    :param headers: The headers to pass with the get request
    :return: data if any exists
    """
    if headers is None:
        headers = {}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, allow_redirects=False) as response:
                return response
    except Exception as e:
        logger.error(f"Error in get request: {e}")