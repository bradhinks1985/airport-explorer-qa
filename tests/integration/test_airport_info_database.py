from pages.airport_info import AirportInfoPage
import sqlite3


### PASSED ###
# Verify that the airport information displayed on the airport info page matches the database for a selected airport.
def test_airport_info_matches_database(page):

    airport_page = AirportInfoPage(page)
    airport_page.go_to_airport_info_page("United States")
    airport_page.select_airport("Detroit - Detroit Metropolitan Airport", "DTW")
    airport_page.select_airport_button.click()

    # get airport data from database
    db_conn = sqlite3.connect("airports.db")
    db_conn.row_factory = sqlite3.Row

    row = db_conn.execute(
        """
        SELECT airport_name, city, country, latitude, longitude
        FROM airports
        WHERE iata = ?
        """,
        ("DTW",)
    ).fetchone()

    db_conn.close()

    # verify that the airport info on the page matches the database 
    assert airport_page.get_airport_info()["airport_name"] == f"Airport: {row['airport_name']}"
    assert airport_page.get_airport_info()["city_country"] == f"City-Country: {row['city']} - {row['country']}"
    assert airport_page.get_airport_info()["latitude"] == f"Latitude: {round(row['latitude'], 2)}°"
    assert airport_page.get_airport_info()["longitude"] == f"Longitude: {round(row['longitude'], 2)}°"