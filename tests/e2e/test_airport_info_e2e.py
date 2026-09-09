from pages.airport_info import AirportInfoPage
from tests.conftest import page


### PASSED ###
# As an end-to-end test, verify that the airport info page displays the correct information for a selected airport, including airport information, domestic and international routes, and airlines and destinations.
def test_airport_info_complete_user_journey(page):

    airport_page = AirportInfoPage(page)

    airport_page.go_to_airport_info_page("United States")

    airport_page.select_airport("Detroit - Detroit Metropolitan Airport", "DTW")

    airport_page.select_airport_button.click()

    page.wait_for_timeout(1000)

    # Wait for loading overlay to disappear before checking visibility
    page.locator("#loadingOverlay").wait_for(state="hidden", timeout=60000)
    
    # Add explicit waits for cards to be visible before assertions
    airport_page.airport_info.wait_for(state="visible", timeout=60000)
    airport_page.domestic_routes_card.wait_for(state="visible", timeout=60000)
    airport_page.international_routes_card.wait_for(state="visible", timeout=60000)
    airport_page.airlines_destinations_card.wait_for(state="visible", timeout=60000)

    # Verify the major sections of the page are available
    assert airport_page.airport_info.is_visible()
    assert airport_page.domestic_routes_card.is_visible()
    assert airport_page.international_routes_card.is_visible()
    assert airport_page.airlines_destinations_card.is_visible()