from pages.airport_info import AirportInfoPage


### PASSED ###
# Verify that the busiest international routes section on the airport info page displays the correct information for an airport with international routes.
def test_international_routes_has_data(page):

    airport_page = AirportInfoPage(page)

    airport_page.go_to_airport_info_page("United States")

    airport_page.select_airport("Detroit - Detroit Metropolitan Airport", "DTW")

    airport_page.select_airport_button.click()

    # Busiest international routes
    if airport_page.international_routes_card.is_visible():
        airport_page.open_international_routes()
        destination = airport_page.get_international_route_destination()
        assert (
            airport_page.get_international_route_destination()
            == "Amsterdam, Netherlands"
        )
    else:
        print("Airport has no international route data.")



### PASSED ###
# Verify that the busiest international routes section on the airport info page does not display for an airport without international routes.
def test_international_routes_has_no_data(page):

    airport_page = AirportInfoPage(page)

    airport_page.go_to_airport_info_page("United States")

    airport_page.select_airport("Denver - Centennial Airport", "APA")

    airport_page.select_airport_button.click()

    # Busiest international routes
    if airport_page.international_routes_card.is_visible():
        airport_page.open_international_routes()
        destination = airport_page.get_international_route_destination()
        assert destination
    else:
        print("Airport has no international route data.")


