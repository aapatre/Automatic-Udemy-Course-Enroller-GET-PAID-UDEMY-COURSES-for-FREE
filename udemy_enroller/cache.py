import datetime
import json
import os

from udemy_enroller.utils import get_app_dir


class CourseCache:
    """
    Basic cache to keep details on courses already scraped
    """

    def __init__(self, file_name=".course_cache"):
        self._file_name = os.path.join(get_app_dir(), file_name)
        self._cache = []
        self._load_cache()

    def __contains__(self, url: str) -> bool:
        """
        Simply check if the url is already in the cache

        :param str url: URL to check the cache for
        :return:
        """
        return url in [c["url"] for c in self._cache]

    def _load_cache(self) -> None:
        """
        Load the cache into memory when we initialize

        :return:
        """
        file_mode = "r" if os.path.isfile(self._file_name) else "w+"
        with open(self._file_name, file_mode) as f:
            cached_data = f.read().splitlines()
            if cached_data:
                self._cache = list(map(json.loads, cached_data))

    def _append_cache(self, data: str) -> None:
        """
        Append the new data to the cache

        :param str data: Data to append to the cache
        :return:
        """
        with open(self._file_name, "a") as f:
            f.write(f"{data}\n")

    def add(self, url: str, status: str) -> None:
        """
        Add a result our cache

        :param str url: URL of the udemy course to cache
        :param str status: The status of the course determined by the script
        :return:
        """
        _data_to_cache = {
            "url": url,
            "status": status,
            "date": datetime.datetime.utcnow().isoformat(),
        }
        self._cache.append(_data_to_cache)
        self._append_cache(json.dumps(_data_to_cache))
