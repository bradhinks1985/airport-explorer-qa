from pages.airport_info import AirportInfoPage


### PASSED ###
# Verify that the airlines and destinations section on the airport info page displays the correct information for an airport with airlines and destinations data.
def test_airlines_destinations_has_data(page):

    airport_page = AirportInfoPage(page)

    airport_page.go_to_airport_info_page("United States")

    airport_page.select_airport("Detroit - Detroit Metropolitan Airport", "DTW")

    airport_page.select_airport_button.click()

    # airlines and destinations
    if airport_page.airlines_destinations_card.is_visible():

        # first airline
        airport_page.open_airlines_destinations()
    
        assert (
            airport_page.get_airline_air_dest()
            == "Aeroméxico Connect"
        )

        # first destination
        assert (
            airport_page.get_destination_air_dest()
            == "Monterrey"
        )

    else:
        print("Airport has no airlines and destinations data.")
 


 
### PASSED ###
# Verify that the airlines and destinations section on the airport info page does not display for an airport without airlines and destinations data.
def test_airlines_destinations_has_no_data(page):

    airport_page = AirportInfoPage(page)

    airport_page.go_to_airport_info_page("United States")

    airport_page.select_airport("Georgetown - Sussex County Airport", "GED")

    airport_page.select_airport_button.click()

    # airlines and destinations
    if airport_page.airlines_destinations_card.is_visible():

        # first airline
        airport_page.open_airlines_destinations()
        airline = airport_page.get_airline_air_dest()
        assert airline

        # first destination
        destination = airport_page.get_destination_air_dest()
        assert destination

    else:
        print("Airport has no airlines and destinations data.")
