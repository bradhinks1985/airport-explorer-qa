from pages.airport_info import AirportInfoPage

### PASSED ###
# for airport without ai summary in db, verify that the ai summary history displays on the airport info page.
def test_airport_ai_summary(page):

    airport_page = AirportInfoPage(page)

    # go to airport info page
    airport_page.go_to_airport_info_page("United States")

    #click generate random airport button
    airport_page.generate_random_airport()

    # click ai summary link
    airport_page.view_ai_summary()

    # wait for history section to be visible
    page.locator("#history").wait_for(state="visible", timeout=10000)


    # get ai history from page and assert that it is not empty
    assert airport_page.get_airport_ai_history()

    
      