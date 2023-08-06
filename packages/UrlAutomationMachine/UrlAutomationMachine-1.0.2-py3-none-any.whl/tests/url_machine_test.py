import pytest
from src.url_class import urlAutomationMachine


@pytest.fixture()
def example_urls():
    return [
        "https://www.google.ca",
        "http://rawkamatic.github.io/opensourcefeed",
        "http://www.danepstein.ca/category/open-source/feed",
    ]


def test_process_url_passed(example_urls):
    url = example_urls[0]

    test_url = urlAutomationMachine(url)
    test_url.processUrl()

    assert (test_url.getStatus()) == 200


def test_process_url_failed(example_urls):
    url = example_urls[1]
    test_url = urlAutomationMachine(url)

    test_url.processUrl()

    assert (test_url.getStatus()) == 404


def test_url_unknown(example_urls):
    url = example_urls[2]

    test_url = urlAutomationMachine(url)

    test_url.processUrl()

    assert (test_url.getStatus()) == 403


def test_url_is_correct():
    url = "https://www.google.ca"

    test_url = urlAutomationMachine(url)

    assert (test_url.checkUrl()) == url


def test_url_is_not_correct():
    url = "htt://www.google.ca"

    test_url = urlAutomationMachine(url)

    assert (test_url.checkUrl()) == None


def test_file_upload_empty():
    test_url = urlAutomationMachine()

    with pytest.raises(AttributeError) as error_value:
        test_url.processFile()

    assert "A parameter is required" in str(error_value)


def test_file_upload_is_not_file():
    test_url = urlAutomationMachine({})

    with pytest.raises(ValueError) as error_value:
        test_url.processFile()

    assert "Function requires a file to be inserted" in str(error_value)
