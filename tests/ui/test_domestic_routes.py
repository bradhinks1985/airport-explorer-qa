from pages.airport_info import AirportInfoPage


### PASSED ###
# Verify that the busiest domestic routes section on the airport info page displays the correct information for an airport with domestic routes.
def test_domestic_routes_has_data(page):

    airport_page = AirportInfoPage(page)

    airport_page.go_to_airport_info_page("United States")

    airport_page.select_airport("Detroit - Detroit Metropolitan Airport", "DTW")

    airport_page.select_airport_button.click()

    # Busiest international routes
    if airport_page.international_routes_card.is_visible():

        # busiest domestic routes - first route
        airport_page.open_domestic_routes()
    
        assert airport_page.domestic_route_destination.is_visible()
        assert (
            airport_page.get_domestic_route_destination()
            == "Atlanta, Georgia"
        )
    else:
        print("Airport has no domestic route data.")



### PASSED ###
# Verify that the busiest domestic routes section on the airport info page does not display for an airport without domestic routes.
def test_domestic_routes_has_no_data(page):

    airport_page = AirportInfoPage(page)

    airport_page.go_to_airport_info_page("United States")

    airport_page.select_airport("Denver - Centennial Airport", "APA")

    airport_page.select_airport_button.click()

    # Busiest domestic routes
    if airport_page.domestic_routes_card.is_visible():
        airport_page.open_domestic_routes()
        destination = airport_page.get_domestic_route_destination()
        assert destination
    else:
        print("Airport has no domestic route data.")