from pages.airport_info import AirportInfoPage


### PASSED ###
# Verify that the airport information card on the airport info page displays the correct information for a selected airport.
def test_airport_information(page):

    airport_page = AirportInfoPage(page)

    airport_page.go_to_airport_info_page("United States")

    airport_page.select_airport("Detroit - Detroit Metropolitan Airport", "DTW")

    airport_page.select_airport_button.click()
    
    # airport info card
    actual = airport_page.get_airport_info()

    assert actual["airport_name"] == "Airport: Detroit Metropolitan Wayne County Airport"

    assert actual["city_country"] == "City-Country: Detroit - United States"

    assert actual["latitude"] == "Latitude: 42.21°"

    assert actual["longitude"] == "Longitude: -83.35°"

    assert (
        "N/A" in actual["temperature"]
        or "°" in actual["temperature"]
    )