from app import app


#### PASSED ###
# Verify that the /api/airports endpoint returns a list of airports for a valid country.
def test_valid_country():
    client = app.test_client()

    response = client.get("/api/airports?country=United States")

    assert response.status_code == 200

    airports = response.get_json()

    assert len(airports) > 0



#### PASSED ###
# Verify that the /api/airports endpoint returns an empty list for an invalid country.
def test_invalid_country():
    client = app.test_client()

    response = client.get("/api/airports?country=NotARealCountry")

    assert response.status_code == 200

    airports = response.get_json()

    assert airports == []



#### PASSED ###
# Verify that the /api/airports endpoint returns required fields.
def test_airport_response_contains_required_fields():
    client = app.test_client()

    response = client.get("/api/airports?country=United States")

    assert response.status_code == 200

    airports = response.get_json()

    required_fields = {"iata", "city", "airport_name"}

    for airport in airports:
        assert required_fields.issubset(airport.keys())