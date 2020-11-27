from datetime import datetime
from unittest import mock

import pytest

from core import CourseCache
from core.udemy import UdemyStatus


@pytest.mark.parametrize(
    "cache_file_name,data_to_cache,expected_cached_data,urls_should_exist,urls_shouldnt_exist",
    [
        (
            ".course_cache_1",
            (
                (
                    "https://www.udemy.com/course/python/?couponCode=25A92E01C0CB3718497B",
                    UdemyStatus.EXPIRED.value,
                ),
                (
                    "https://www.udemy.com/course/short-sell/?couponCode=1NOV20",
                    UdemyStatus.ENROLLED.value,
                ),
                (
                    "https://www.udemy.com/course/financial-accounting/?couponCode=1EEE181F6BB09A83190D",
                    UdemyStatus.ENROLLED.value,
                ),
                (
                    "https://www.udemy.com/course/cycle/?couponCode=1EEE181F6BB09A83190D",
                    UdemyStatus.UNWANTED_LANGUAGE.value,
                ),
                (
                    "https://www.udemy.com/course/art/?couponCode=1EEE181F6BB09A83190D",
                    UdemyStatus.UNWANTED_CATEGORY.value,
                ),
            ),
            [
                {
                    "url": "https://www.udemy.com/course/python/?couponCode=25A92E01C0CB3718497B",
                    "status": UdemyStatus.EXPIRED.value,
                    "date": "2020-10-10T00:00:00",
                },
                {
                    "url": "https://www.udemy.com/course/short-sell/?couponCode=1NOV20",
                    "status": UdemyStatus.ENROLLED.value,
                    "date": "2020-10-10T00:00:00",
                },
                {
                    "url": "https://www.udemy.com/course/financial-accounting/?couponCode=1EEE181F6BB09A83190D",
                    "status": UdemyStatus.ENROLLED.value,
                    "date": "2020-10-10T00:00:00",
                },
                {
                    "url": "https://www.udemy.com/course/cycle/?couponCode=1EEE181F6BB09A83190D",
                    "status": UdemyStatus.UNWANTED_LANGUAGE.value,
                    "date": "2020-10-10T00:00:00",
                },
                {
                    "url": "https://www.udemy.com/course/art/?couponCode=1EEE181F6BB09A83190D",
                    "status": UdemyStatus.UNWANTED_CATEGORY.value,
                    "date": "2020-10-10T00:00:00",
                },
            ],
            [
                "https://www.udemy.com/course/python/?couponCode=25A92E01C0CB3718497B",
                "https://www.udemy.com/course/short-sell/?couponCode=1NOV20",
                "https://www.udemy.com/course/financial-accounting/?couponCode=1EEE181F6BB09A83190D",
                "https://www.udemy.com/course/cycle/?couponCode=1EEE181F6BB09A83190D",
                "https://www.udemy.com/course/art/?couponCode=1EEE181F6BB09A83190D",
            ],
            [
                "https://www.udemy.com/course/python1/?couponCode=25A92E01C0CB3718497B",
                "https://www.udemy.com/course/new-course-1/?couponCode=19NOV20",
                "https://www.udemy.com/course/new-course-2/?couponCode=25A92E01C0CB3718497B",
                "https://www.udemy.com/course/new-course-3/?couponCode=10NOV20",
            ],
        ),
    ],
    ids=("Initialize cache and add data",),
)
@mock.patch("core.cache.datetime")
def test_cache(
    mock_dt,
    cache_file_name,
    data_to_cache,
    expected_cached_data,
    urls_should_exist,
    urls_shouldnt_exist,
):
    mock_dt.datetime.utcnow = mock.Mock(return_value=datetime(2020, 10, 10))
    cc = CourseCache(f"test_tmp/{cache_file_name}")
    for url, status in data_to_cache:
        cc.add(url, status)

    assert cc._cache == expected_cached_data
    for url in urls_should_exist:
        assert url in cc

    for url in urls_shouldnt_exist:
        assert url not in cc


@pytest.mark.parametrize(
    "cache_file_name,data_to_cache,expected_cached_data,urls_should_exist,urls_shouldnt_exist",
    [
        (
            ".course_cache_2",
            (
                (
                    "https://www.udemy.com/course/python/?couponCode=25A92E01C0CB3718497B",
                    UdemyStatus.EXPIRED.value,
                ),
                (
                    "https://www.udemy.com/course/short-sell/?couponCode=1NOV20",
                    UdemyStatus.ENROLLED.value,
                ),
                (
                    "https://www.udemy.com/course/financial-accounting/?couponCode=1EEE181F6BB09A83190D",
                    UdemyStatus.ENROLLED.value,
                ),
                (
                    "https://www.udemy.com/course/cycle/?couponCode=1EEE181F6BB09A83190D",
                    UdemyStatus.UNWANTED_LANGUAGE.value,
                ),
                (
                    "https://www.udemy.com/course/art/?couponCode=1EEE181F6BB09A83190D",
                    UdemyStatus.UNWANTED_CATEGORY.value,
                ),
            ),
            [
                {
                    "url": "https://www.udemy.com/course/python/?couponCode=25A92E01C0CB3718497B",
                    "status": UdemyStatus.EXPIRED.value,
                    "date": "2020-11-10T00:00:00",
                },
                {
                    "url": "https://www.udemy.com/course/short-sell/?couponCode=1NOV20",
                    "status": UdemyStatus.ENROLLED.value,
                    "date": "2020-11-10T00:00:00",
                },
                {
                    "url": "https://www.udemy.com/course/financial-accounting/?couponCode=1EEE181F6BB09A83190D",
                    "status": UdemyStatus.ENROLLED.value,
                    "date": "2020-11-10T00:00:00",
                },
                {
                    "url": "https://www.udemy.com/course/cycle/?couponCode=1EEE181F6BB09A83190D",
                    "status": UdemyStatus.UNWANTED_LANGUAGE.value,
                    "date": "2020-11-10T00:00:00",
                },
                {
                    "url": "https://www.udemy.com/course/art/?couponCode=1EEE181F6BB09A83190D",
                    "status": UdemyStatus.UNWANTED_CATEGORY.value,
                    "date": "2020-11-10T00:00:00",
                },
            ],
            [
                "https://www.udemy.com/course/python/?couponCode=25A92E01C0CB3718497B",
                "https://www.udemy.com/course/short-sell/?couponCode=1NOV20",
                "https://www.udemy.com/course/financial-accounting/?couponCode=1EEE181F6BB09A83190D",
                "https://www.udemy.com/course/cycle/?couponCode=1EEE181F6BB09A83190D",
                "https://www.udemy.com/course/art/?couponCode=1EEE181F6BB09A83190D",
            ],
            [
                "https://www.udemy.com/course/python1/?couponCode=25A92E01C0CB3718497B",
                "https://www.udemy.com/course/new-course-1/?couponCode=19NOV20",
                "https://www.udemy.com/course/new-course-2/?couponCode=25A92E01C0CB3718497B",
                "https://www.udemy.com/course/new-course-3/?couponCode=10NOV20",
            ],
        ),
    ],
    ids=("Initialize cache and add data",),
)
@mock.patch("core.cache.datetime")
def test_cache_load(
    mock_dt,
    cache_file_name,
    data_to_cache,
    expected_cached_data,
    urls_should_exist,
    urls_shouldnt_exist,
):
    mock_dt.datetime.utcnow = mock.Mock(return_value=datetime(2020, 11, 10))
    # Create original cache and write some data to it
    cc = CourseCache(f"test_tmp/{cache_file_name}")
    for url, status in data_to_cache:
        cc.add(url, status)

    assert cc._cache == expected_cached_data

    # Load from file when new instance created
    next_run = CourseCache(f"test_tmp/{cache_file_name}")
    assert next_run._cache == expected_cached_data
