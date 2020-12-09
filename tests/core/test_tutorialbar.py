from unittest import mock

import pytest

from core import TutorialBarScraper


@pytest.mark.parametrize(
    "tutorialbar_course_page_link,tutorialbar_links,udemy_links",
    [
        (
            "https://www.tutorialbar.com/all-courses/page/1/",
            [
                "https://www.tutorialbar.com/course_1",
                "https://www.tutorialbar.com/course_2",
            ],
            [
                "https://www.udemy.com/1?FREECOURSE",
                "https://www.udemy.com/2?FREECOURSE",
            ],
        ),
        ("https://www.tutorialbar.com/all-courses/page/1/", [], []),
    ],
    ids=("List of courses", "Empty courses"),
)
@mock.patch.object(TutorialBarScraper, "gather_udemy_course_links")
@mock.patch.object(TutorialBarScraper, "get_course_links")
def test_run(
    mock_get_course_links,
    mock_gather_udemy_course_links,
    tutorialbar_course_page_link,
    tutorialbar_links,
    udemy_links,
):
    mock_get_course_links.return_value = tutorialbar_links
    mock_gather_udemy_course_links.return_value = udemy_links
    tbs = TutorialBarScraper()
    links = tbs.run()

    mock_get_course_links.assert_called_with(tutorialbar_course_page_link)
    mock_gather_udemy_course_links.assert_called_with(tutorialbar_links)
    for link in links:
        assert link in udemy_links


@pytest.mark.parametrize(
    "page_number,is_first_page",
    [(1, True), (2, False)],
    ids=(
        "First Page",
        "Not first page",
    ),
)
def test_check_page_number(page_number, is_first_page):
    tbs = TutorialBarScraper()
    tbs.current_page = page_number
    assert tbs.is_first_loop() == is_first_page


@mock.patch("core.tutorialbar.requests")
def test_get_course_links(mock_requests, tutorialbar_main_page):
    url = "https://www.tutorialbar.com/main"
    requests_response = mock.Mock()
    requests_response.content = tutorialbar_main_page
    mock_requests.get.return_value = requests_response
    tbs = TutorialBarScraper()
    tbs.current_page = 1
    links = tbs.get_course_links(url)

    assert tbs.last_page == "601"
    assert links == [
        "https://www.tutorialbar.com/mindfulness-meditation-for-pain-relief-stress-management/",
        "https://www.tutorialbar.com/become-a-crm-manager-overview-for-email-marketing-starters/",
        "https://www.tutorialbar.com/superminds-the-future-of-artificial-intelligence-ai/",
        "https://www.tutorialbar.com/invade-your-classroom-with-digital-robot-teachers-in-2020/",
        "https://www.tutorialbar.com/introduction-au-machine-learning-python/",
        "https://www.tutorialbar.com/comic-creation-for-entrepreneurs-2020-edition/",
        "https://www.tutorialbar.com/delicious-japanese-language-for-foodies-jlpt-n5-jlpt-n4/",
        "https://www.tutorialbar.com/sparring-tai-chi-chen-new-frame-routine-2-for-fitness/",
        "https://www.tutorialbar.com/active-learning-using-games-in-education/",
        "https://www.tutorialbar.com/eiq2-coaching-for-improved-performance-and-superior-results/",
        "https://www.tutorialbar.com/quickbooks-pro-desktop-bookkeeping-business-easy-way/",
        "https://www.tutorialbar.com/quickbooks-online-bank-feeds-credit-card-feeds-2020/",
    ]
