from pages.airport_info import AirportInfoPage

### PASSED ###
# Verify that the link to the airport map page opens when map link is clicked on airport info page.
def test_airport_on_map(page):

    airport_page = AirportInfoPage(page)
    
    airport_page.go_to_airport_info_page("United States")
    
    airport_page.select_airport("Detroit - Detroit Metropolitan Airport", "DTW")
    
    airport_page.select_airport_button.click()

    # view on map 
    airport_page.view_on_map()

    assert airport_page.map_page_title.is_visible()