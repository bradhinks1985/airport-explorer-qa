from pages.airport_info import AirportInfoPage


### PASSED ###
# For airport with ai summary in db, verify that the ai summary history on the airport info page matches the history in the database.
def test_airport_ai_summary_database(page):

    airport_page = AirportInfoPage(page)
    
    airport_page.go_to_airport_info_page("United States")

    #go to airport info page and select airport
    airport_page.select_airport("Detroit - Detroit Metropolitan Airport", "DTW")

    #click select airport button
    airport_page.select_airport_button.click()

    # click ai summary link
    airport_page.view_ai_summary()

    # wait for loading icon to be hidden
    page.locator("#loadingOverlay").wait_for(state="hidden")

    # get ai history from page
    airport_page.airport_ai_history_page = airport_page.get_airport_ai_history()

    # get db ai history 
    airport_ai_history_db = airport_page.get_airport_ai_history_db("DTW")
    airport_ai_history_db = airport_ai_history_db["history"]

    
    assert airport_page.airport_ai_history_page == airport_ai_history_db