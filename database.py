import csv
import sqlite3
from wikipedia_api import get_airlines_from_wikipedia, get_wikipedia_page_title
import time
import traceback

import os

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))




# conn = sqlite3.connect("airports.db")

# with open("data/spain_data.csv", newline="", encoding="utf-8") as f:
#     reader = csv.DictReader(f)

#     rows = [
#         (
#             row["city"],
#             row["state"],
#             row["country"],
#             float(row["latitude"]),
#             float(row["longitude"]),
#             int(row["population"])
#         )
#         for row in reader
#     ]

# conn.executemany("""
#     INSERT INTO cities
#         (city, state, country, latitude, longitude, population)
#     VALUES (?, ?, ?, ?, ?, ?)
# """, rows)

# conn.commit()
# conn.close()

# print(f"Inserted {len(rows)} cities")


# conn = sqlite3.connect(
#     os.path.join(BASE_DIR, "airports.db")
# )
# # conn = sqlite3.connect("airports.db")
# conn.row_factory = sqlite3.Row
# cur = conn.cursor()


# # insert data into airlines and destinations table
# us_airports = conn.execute("""
#     SELECT iata
#     FROM airports
#     WHERE country = 'United States'
#       AND iata IS NOT NULL
#       AND iata != ''
# """).fetchall()

# # print(type(us_airports[0]))
# # print(us_airports[0])

# for airport in us_airports:

#     iata = airport["iata"]

#     try:
#         page_title = get_wikipedia_page_title(iata)

#         if not page_title:
#             print(f"{iata}: No Wikipedia page")
#             continue

#         routes = get_airlines_from_wikipedia(page_title)

#         if not routes:
#             print(f"{iata}: No routes found")
#             continue

#         for airline, destinations in routes.items():

#             for destination in destinations:

#                 conn.execute("""
#                     INSERT OR REPLACE INTO airport_destinations
#                     (
#                         airport_iata,
#                         airline,
#                         destination_city,
#                         wikipedia_page,
#                         last_updated
#                     )
#                     VALUES (?, ?, ?, ?, DATE('now'))
#                 """,
#                 (
#                     iata,
#                     airline,
#                     destination,
#                     page_title
#                 ))

#         print(f"{iata}: imported")

#     except Exception as e:
#         print(f"{iata}: ERROR - {e}")

#     time.sleep(1)

# conn.commit()

# conn.close()




# # import of airport_list.csv into airports table
# cur.execute("""
#     CREATE TABLE IF NOT EXISTS airports (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         iata TEXT,
#         icao TEXT,
#         airport_name TEXT,
#         city TEXT,
#         country TEXT,
#         latitude REAL,
#         longitude REAL
#     )
# """)

# with open("data/airport_list.csv", newline="", encoding="utf-8-sig") as f:
#     lines = f.readlines()

# cleaned_lines = []
# for line in lines:
#     line = line.strip("\r\n")
#     if line.startswith('"') and line.endswith('"'):
#         line = line[1:-1]              # remove outer wrapping quotes
#     line = line.replace('""', '"')     # unescape doubled quotes
#     cleaned_lines.append(line)

# reader = csv.reader(cleaned_lines)

# inserted = 0
# skipped = 0
# for row in reader:
#     if len(row) <= 4 or row[4].strip() == "":
#         skipped += 1
#         continue
#     cur.execute(
#         """
#         INSERT INTO airports
#         (iata, icao, airport_name, city, country, latitude, longitude)
#         VALUES (?, ?, ?, ?, ?, ?, ?)
#         """,
#         (
#             row[4],   # IATA
#             row[5],   # ICAO
#             row[1],   # Airport name
#             row[2],   # City
#             row[3],   # Country
#             row[6],   # Latitude
#             row[7],   # Longitude
#         )
#     )
#     inserted += 1

# print(f"Inserted: {inserted}, Skipped: {skipped}")

# conn.commit()

# cur.execute("SELECT COUNT(*) FROM airports")
# print("Total rows:", cur.fetchone()[0])

# #delete old table data
# cur.execute("DROP TABLE cities")

# # import of world cities data csv into cities table
# cur.execute("""
#     CREATE TABLE IF NOT EXISTS cities (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         city TEXT,
#         state TEXT,
#         country TEXT,
#         latitude REAL,
#         longitude REAL,
#         population INTEGER
#     )
# """)


# with open("data/world_cities.csv", newline="", encoding="utf-8-sig") as f:

#     reader = csv.reader(f)
#     next(reader)  # Skip header if present

#     inserted = 0
#     try:
#         for row in reader:
#             cur.execute(
#                 """
#                 INSERT INTO cities
#                 (city, state, country, latitude, longitude, population)
#                 VALUES (?, ?, ?, ?, ?, ?)
#                 """,
#                 (
#                     row[0],   # City
#                     row[1],   # State
#                     row[2],   # Country
#                     float(row[3]),   # Latitude
#                     float(row[4]),   # Longitude
#                     int(row[5]),  # Population
#                 )
#             )
#             inserted += 1

#     except Exception as e:
#         print("Skipping row:", row)
#         print(e)

#     print(f"Inserted: {inserted}")

# conn.commit()

# cur.execute("SELECT COUNT(*) FROM cities")
# print("Total rows:", cur.fetchone()[0])




