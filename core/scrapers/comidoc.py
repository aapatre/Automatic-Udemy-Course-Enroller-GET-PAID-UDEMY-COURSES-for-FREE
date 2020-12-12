import datetime
import json
import logging

import aiohttp

from core.scrapers.base_scraper import BaseScraper

logger = logging.getLogger("udemy_enroller")


class ComidocScraper(BaseScraper):
    """
    Contains any logic related to scraping of data from comidoc.net
    """

    DOMAIN = "https://comidoc.net"
    HEADERS = {
        "authority": "comidoc.net",
        "accept-language": "en-US",
        "content-type": "application/json",
        "accept": "*/*",
        "origin": DOMAIN,
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": f"{DOMAIN}/daily",
    }

    def __init__(self, days_offset=10, enabled=True):
        super().__init__()
        self.scraper_name = "comidoc"
        if not enabled:
            self.set_state_disabled()
        self.days_offset = days_offset  # Query the past months coupons

    @BaseScraper.time_run
    async def run(self):
        return await self.get_links()

    async def get_links(self):
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

    async def get_data(self):
        """

        :return:
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

        return data["data"]["coupons"]
