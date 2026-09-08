import sqlite3


### PASSED ###
# Verify that airport record exists in the database and has the correct information.
def test_airport_database_record():

    conn = sqlite3.connect("airports.db")
    conn.row_factory = sqlite3.Row

    row = conn.execute(
        """
        SELECT *
        FROM airports
        WHERE iata = ?
        """,
        ("DTW",)
    ).fetchone()

    conn.close()

    assert row is not None
    assert row["iata"] == "DTW"
    assert row["airport_name"] == "Detroit Metropolitan Wayne County Airport"
    assert row["city"] == "Detroit"
    assert row["country"] == "United States"


