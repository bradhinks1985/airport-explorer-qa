from pages.airport_info import AirportInfoPage


### PASSED ###
# Verify that the airlines and destinations section on the airport info page displays the correct information for a selected airport.
def test_airlines_destinations(page):

    airport_page = AirportInfoPage(page)

    airport_page.go_to_airport_info_page("United States")

    airport_page.select_airport("Detroit - Detroit Metropolitan Airport", "DTW")

    airport_page.select_airport_button.click()
 

    ### airlines and destinations
    airport_page.open_airlines_destinations()

    # first airline
    # assert airport_page.get_airline_air_dest.is_visible()
    assert (
        airport_page.get_airline_air_dest()
        == "Aeroméxico Connect"
    )

    # first destination
    # assert airport_page.get_destination_air_dest.is_visible()
    assert (
        airport_page.get_destination_air_dest()
        == "Monterrey"
    )

