import pytest


@pytest.fixture
def page(browser):
    page = browser.new_page()
    page.goto("http://127.0.0.1:5000")

    return page