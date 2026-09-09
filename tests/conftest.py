import pytest



@pytest.fixture
def page(browser):
    page = browser.new_page()
    page.set_default_timeout(60000)  # Set 60 second timeout
    page.goto("http://127.0.0.1:5000")
    
    return page


