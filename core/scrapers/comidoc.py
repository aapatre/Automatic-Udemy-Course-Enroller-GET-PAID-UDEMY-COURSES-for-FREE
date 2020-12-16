import datetime
import json
import logging
import re
from typing import Dict, List

import aiohttp
from bs4 import BeautifulSoup

from core.scrapers.base_scraper import BaseScraper

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

    def __init__(self, enabled, days_offset=5):
        super().__init__()
        self.scraper_name = "comidoc"
        if not enabled:
            self.set_state_disabled()
        self.days_offset = days_offset  # Query the past months coupons

    @BaseScraper.time_run
    async def run(self) -> List:
        """
        Called to gather the udemy links

        :return: List of udemy course links
        """
        await self.set_api_key()
        return await self.get_links()

    async def get_links(self) -> List:
        links = []
        # TODO: Add try/except block to handle connection issues
        data = await self.get_data()
        if data:
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

        url = f"{self.DOMAIN}/beta"
        payload = {
            "query": "query DAILY_COURSES_QUERY($myDate: DateTime) { coupons: "
            'coupons( where: { isValid: true createdAt_gte: $myDate discountValue_starts_with: "100%" } '
            "orderBy: createdAt_DESC) { code isValid createdAt discountValue discountPrice maxUses "
            "remainingUses endTime course { udemyId cleanUrl createdAt updatedAt detail(last: 1) { title "
            "isPaid lenghtTxt rating updated subscribers locale { locale } } } } }",
            "variables": {
                "myDate": (
                    datetime.datetime.utcnow()
                    - datetime.timedelta(days=self.days_offset)
                ).strftime("%Y-%m-%dT%H")
            },
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                url, headers=self.HEADERS, data=json.dumps(payload)
            ) as response:
                data = await response.json()

        return data["data"]["coupons"] if data else {}

    async def set_api_key(self) -> None:
        """
        Retrieves the api key from comidoc and updates our Headers with that value

        :return: None
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self.DOMAIN,
                headers=self.HEADERS,
            ) as response:
                text = await response.read()
        js_links = []
        soup = BeautifulSoup(text.decode("utf-8"), "html.parser")

        # There is no way to identify which js file has the api key
        # so we gather all js files imported at top of the page
        for i in soup.find_all("script"):
            src = i.get("src", "")
            if (
                src.startswith("https://cdn.comidoc.net/_next/static/chunks/")
                and src.endswith(".js")
                and "-" not in src
            ):
                js_links.append(src)

        # Loop through js files until we get the X-API-KEY
        for js_url in reversed(js_links):
            async with aiohttp.ClientSession() as session:
                async with session.get(js_url) as response:
                    text = await response.read()
                    if "X-API-KEY" in str(text):
                        match = re.search('(?<=X-API-KEY":")(.*?)(?=")', str(text))
                        self.HEADERS["x-api-key"] = match.group()
                        break
