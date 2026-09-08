from pages.airport_info import AirportInfoPage


### PASSED ###
# Verify that the busiest international routes section on the airport info page displays the correct information for a selected airport.
def test_international_routes(page):

    airport_page = AirportInfoPage(page)

    airport_page.go_to_airport_info_page("United States")

    airport_page.select_airport("Detroit - Detroit Metropolitan Airport", "DTW")

    airport_page.select_airport_button.click()

    # wait for routes section to be visible
    airport_page.international_routes_card.wait_for(state="visible", timeout=10000)

    # busiest international routes - first route
    airport_page.open_international_routes()

    assert airport_page.international_route_destination.is_visible()
    assert (
        airport_page.get_international_route_destination()
        == "Amsterdam, Netherlands"
    )
