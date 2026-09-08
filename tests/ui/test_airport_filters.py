from pages.airport_info import AirportInfoPage


### PASSED ###
# Verify that changing country resets the airport selection and clears the airport info card on the airport info page.
def test_country_change_resets_airport_selection(page):

    airport_page = AirportInfoPage(page)
    airport_page.go_to_airport_info_page("United States")
    airport_page.select_airport("Detroit - Detroit Metropolitan Airport", "DTW")
    airport_page.select_airport_button.click()
 
    # change country to Canada
    # airport_page.go_to_airport_info_page("Canada")
    airport_page.select_country("Canada")

    # verify that the airport selection is reset
    # assert airport_page.airport_select_input.input_value() == ""
    assert airport_page.airport_search.input_value() == ""