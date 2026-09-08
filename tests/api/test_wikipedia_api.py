import pytest
from wikipedia_api import (
    get_wikipedia_page_title,
    get_airlines_from_wikipedia,
    get_top_destinations_from_wikipedia
)


### PASSED ###
# Verify that the airlines from Wikipedia are returned for a valid airport.
@pytest.mark.parametrize(
    "iata",
    [
        "DTW",
        "ORD"
    ]
)
def test_valid_wikipedia_airlines(iata):

    page_title = get_wikipedia_page_title(iata)
    airlines = get_airlines_from_wikipedia(page_title)
    assert airlines is not None


### PASSED ###
# Verify that the airlines from Wikipedia are not returned for an invalid airport.
def test_invalid_wikipedia_airlines():

    page_title = get_wikipedia_page_title("bad_iata")
    airlines = get_airlines_from_wikipedia(page_title)
    assert airlines == {}


### PASSED ###
# Verify handling of missing wikipedia page for airlines.
def test_missing_page_wikipedia_airlines():

    airlines = get_airlines_from_wikipedia("bad_page_title")
    assert airlines == {}


### PASSED ###
# Verify that the top destinations from Wikipedia are returned for a given airport.
def test_valid_airport_wikipedia_routes():

    page_title = get_wikipedia_page_title("DTW")
    destinations = get_top_destinations_from_wikipedia(page_title)
    assert destinations


### PASSED ###
# Verify that the top destinations from Wikipedia are not returned for an invalid airport.
def test_invalid_airport_wikipedia_routes():

    page_title = get_wikipedia_page_title("bad_iata")
    destinations = get_top_destinations_from_wikipedia(page_title)
    assert destinations == {
        'domestic': 'No domestic routes found',
        'international': 'No international routes found',
    }