import json
import logging
from typing import Dict, List

import aiohttp
from bs4 import BeautifulSoup

from core.scrapers.base_scraper import BaseScraper
from core.http import get

logger = logging.getLogger("udemy_enroller")


class ComidocScraper(BaseScraper):
    """
    Contains any logic related to scraping of data from comidoc.net
    """

    DOMAIN = "https://comidoc.net"
    HEADERS = {
        "authority": "comidoc.net",
        "sec-ch-ua": '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
        "accept-language": "en-US",
        "sec-ch-ua-mobile": "?0",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
        "content-type": "application/json",
        "accept": "*/*",
        "origin": DOMAIN,
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": f"{DOMAIN}/daily",
        "cookie": "consent=true",
    }

    def __init__(self, enabled):
        super().__init__()
        self.scraper_name = "comidoc"
        if not enabled:
            self.set_state_disabled()

    @BaseScraper.time_run
    async def run(self) -> List:
        """
        Called to gather the udemy links

        :return: List of udemy course links
        """
        return await self.get_links()

    async def get_links(self) -> List:
        # TODO: Add try/except block to handle connection issues
        data = await self.get_data()

        self.set_state_complete()
        links = [
            f"https://www.udemy.com/course{d['course']['cleanUrl']}?couponCode={d['code']}"
            for d in data
        ]

        return links

    async def get_data(self) -> Dict:
        """
        Fetch data from comidoc endpoint

        :return: dictionary containing data needed to build udemy free urls
        """

        text = await get(self.DOMAIN, headers=self.HEADERS)
        soup = BeautifulSoup(text.decode("utf-8"), "html.parser")

        # We get the url hash needed from the path of the _buildManifest.js file
        path_js = None
        for i in soup.find_all("script"):
            src = i.get("src", "")
            if src.startswith("https://cdn.comidoc.net/_next/static/") and src.endswith(
                "_buildManifest.js"
            ):
                path_js = src.split("/")[-2]
                break

        data = {}
        # Fetch the daily courses if the path has been correctly resolved
        if path_js is not None:
            daily_json_link = f"{self.DOMAIN}/_next/data/{path_js}/daily.json"
            data = await get(daily_json_link, headers=self.HEADERS)

            if data is not None:
                data = json.loads(data)["pageProps"]["coupons"]
            else:
                data = {}
                logger.warning(f"Empty response from comidoc. API may have changed!")
        return data
