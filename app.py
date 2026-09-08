import os
from flask import Flask, redirect, render_template, jsonify, session, request
import sqlite3
from wikipedia_api import (
    get_wikipedia_page_title,
    get_airlines_from_wikipedia,
    get_top_destinations_from_wikipedia
)
from airport_weather_api import (
    get_airport_current_weather
)
from urllib.parse import quote
import builtins, math, requests
from datetime import datetime
import random
from openai import OpenAI
import openai
import json

import sys

from dotenv import load_dotenv

load_dotenv()

print("APP PYTHON:", sys.executable)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.secret_key = "airport-app-secret-key-2026"

# Configure your OpenAI API key
openai.api_key = os.environ.get("OPENAI_API_KEY")


def get_db_connection():

    conn = sqlite3.connect(
        os.path.join(BASE_DIR, "airports.db")
    )
    # conn = sqlite3.connect("airports.db")
    conn.row_factory = sqlite3.Row

    return conn



# for AI city summary in city info page
@app.route("/api/city-summary/<int:city_id>")
def ai_city_summary(city_id):

# @app.route("/api/ai_city_summary")
# def ai_city_summary():
    """
    Route that unpacks url arguments, looks up coordinate data,
    verifies via Wikipedia, and passes context directly to OpenAI.
    """
    # Expecting parameters: /city_info?city=Naples&state=Florida
    # selected_city_id = request.args.get("city")

    selected_city_id = city_id
    
    if not selected_city_id:
        return "Error: Missing city parameter", 400

    # 1. Fetch exact geographic coordinates from your database
    conn = get_db_connection()
    city_data = conn.execute("""
        SELECT 
            id,
            city,
            state,
            country,
            location,
            demographics,
            history,
            culture,
            climate,
            interesting_facts
        FROM cities 
        WHERE id = ? 
    """, (selected_city_id, )).fetchone()
    conn.close()
    
    if not city_data:
        return f"Error: City ID '{selected_city_id}' not found in the database", 404

    # Safeguard against raw sqlite3.Row parsing TypeErrors by explicitly matching keys
    city = city_data["city"]
    state = city_data["state"]
    country = city_data["country"]
    location = city_data["location"]
    demographics = city_data["demographics"]
    history = city_data["history"]
    culture = city_data["culture"]
    climate = city_data["climate"]
    facts = city_data["interesting_facts"]

    # check if ai summary data exists for city. If exists, then get summary data and return to template.

    if location is not None:

        return jsonify({
            "location": location,
            "demographics": demographics,
            "history": history,
            "culture": culture,
            "climate": climate,
            "facts": facts
        })
    
    else:

    # If ai data does not exist, then get summary data from AI and return to template.

        CITY_SUMMARY_SCHEMA = {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string"
                },
                "demographics": {
                    "type": "string"
                },
                "history": {
                    "type": "string"
                },
                "culture": {
                    "type": "string"
                },
                "climate": {
                    "type": "string"
                },
                "interesting_facts": {
                    "type": "string"
                }
            },
            "required": [
                "location",
                "demographics",
                "history",
                "culture",
                "climate",
                "interesting_facts"
            ],
            "additionalProperties": False
        }



        # 4. Prompt GPT-5.4-mini with zero-temperature and explicit constraint definitions
        try:

            response = openai.chat.completions.create(
                model="gpt-5.4-mini",
                temperature=0.0,

                messages=[
                    {
                        "role": "system",
                        "content": """
                            You create concise, interesting city summaries for people
                            who have never heard of the city.

                            Follow these rules:

                            - Aim for 100-150 words per category when reliable
                            information genuinely supports that length.
                            - Categories may be substantially shorter when information is limited.
                            - Do not invent or guess specific facts.
                            - Use information you are reasonably confident is true.
                            - Distinguish city-specific facts from facts about the surrounding region.
                            - Do not attribute regional characteristics to the city without saying
                            that they are regional.
                            - Do not claim that a city is known for something without a reasonable
                            basis.
                            - For small or obscure settlements, be especially conservative.
                            - If reliable information for a category is limited, say so briefly.
                            - Never fabricate population figures, landmarks, historical events,
                            festivals, restaurants, ethnic composition, or other specific details.
                            - Write for someone who has never heard of the city.
                            """
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Create a summary of {city}, {state}, {country}."
                        )
                    }
                ],

                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "city_summary",
                        "strict": True,
                        "schema": CITY_SUMMARY_SCHEMA
                    }
                }
            )

        except Exception as e:
            print("=== OPENAI ERROR ===")
            print(type(e).__name__)
            print(str(e))
            print(repr(e))

            return jsonify({
                "error": str(e)
            }), 500

        ai_summary = response.choices[0].message.content

        try:
            summary = json.loads(ai_summary)
        except json.JSONDecodeError as e:
            print("JSON ERROR:", e)
            return jsonify({
                "error": "AI returned invalid JSON"
            }), 500


        location = summary["location"]
        demographics = summary["demographics"]
        history = summary["history"]
        culture = summary["culture"]
        climate = summary["climate"]
        facts = summary["interesting_facts"]

        # add ai summary data to database
        conn = get_db_connection()
        conn.execute("""
            UPDATE cities
            SET
                location = ?,
                demographics = ?,
                history = ?,
                culture = ?,
                climate = ?,
                interesting_facts = ?
            WHERE id = ?
        """,(location,demographics,history,culture,climate,facts,selected_city_id))

        conn.commit()
        conn.close()
    

        return jsonify({
            "location": location,
            "demographics": demographics,
            "history": history,
            "culture": culture,
            "climate": climate,
            "facts": facts
        })

     


@app.route("/city-summary/<int:city_id>")
def city_summary(city_id):

    return render_template(
        "city_summary.html",
        city_id=city_id
    )



# for AI airport summary in airport info page
@app.route("/api/airport-summary/<iata>")
def ai_airport_summary(iata):

   
    iata = iata
    
    if not iata:
        return "Error: Missing airport parameter", 400

    # 1. Fetch exact geographic coordinates from your database
    conn = get_db_connection()
    airport_data = conn.execute("""
        SELECT 
            airport_name,
            city,
            country,
            history,
            features,
            facts
        FROM airports 
        WHERE iata = ? 
    """, (iata, )).fetchone()
    conn.close()
    
    if not airport_data:
        return f"Error: Airport iata '{iata}' not found in the database", 404

    # Safeguard against raw sqlite3.Row parsing TypeErrors by explicitly matching keys
    airport_name = airport_data["airport_name"]
    city = airport_data["city"]
    country = airport_data["country"]
    history = airport_data["history"]
    features = airport_data["features"]
    facts = airport_data["facts"]


    # check if ai summary data exists for airport. If exists, then get summary data and return to template.

    if history is not None:

        return jsonify({
            "history": history,
            "features": features,
            "facts": facts
        })
    
    else:

    # If ai data does not exist, then get summary data from AI and return to template.

        AIRPORT_SUMMARY_SCHEMA = {
            "type": "object",
            "properties": {
                "history": {
                    "type": "string"
                },
                "features": {
                    "type": "string"
                },
                "interesting_facts": {
                    "type": "string"
                }
            },
            "required": [
                "history",
                "features",
                "interesting_facts"
            ],
            "additionalProperties": False
        }


        # 4. Prompt GPT-5.4-mini with zero-temperature and explicit constraint definitions
        try:

            response = openai.chat.completions.create(
                model="gpt-5.4-mini",
                temperature=0.0,

                messages=[
                    {
                        "role": "system",
                        "content": """
                            You create concise, interesting airport summaries for people
                            who have never heard of the airport.

                            Follow these rules:

                            - Aim for 100-150 words per category when reliable
                            information genuinely supports that length.
                            - Categories may be substantially shorter when information is limited.
                            - Do not invent or guess specific facts.
                            - Use information you are reasonably confident is true.
                            - For small or obscure airports, be especially conservative.
                            - If reliable information for a category is limited, say so briefly.
                            - Write for someone who has never heard of the airport.
                            """
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Create a summary of {airport_name} with iata = {iata} in {city}, {country}."
                        )
                    }
                ],

                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "airport_summary",
                        "strict": True,
                        "schema": AIRPORT_SUMMARY_SCHEMA
                    }
                }
            )

        except Exception as e:
            print("=== OPENAI ERROR ===")
            print(type(e).__name__)
            print(str(e))
            print(repr(e))

            return jsonify({
                "error": str(e)
            }), 500

        ai_summary = response.choices[0].message.content

        try:
            summary = json.loads(ai_summary)
        except json.JSONDecodeError as e:
            print("JSON ERROR:", e)
            return jsonify({
                "error": "AI returned invalid JSON"
            }), 500


        history = summary["history"]
        features = summary["features"]
        facts = summary["interesting_facts"]

        # add ai summary data to database
        conn = get_db_connection()
        conn.execute("""
            UPDATE airports
            SET
                history = ?,
                features = ?,
                facts = ?
            WHERE iata = ?
        """,(history,features,facts,iata))

        conn.commit()
        conn.close()
    

        return jsonify({
            "history": history,
            "features": features,
            "facts": facts
        })

     

@app.route("/airport-summary/<iata>")
def airport_summary(iata):

    return render_template(
        "airport_summary.html",
        iata=iata
    )



# returns airports for a given country, used to populate airport select list in airport info page
@app.route("/api/airports")
def api_airports():

    country = request.args.get("country")
    conn = get_db_connection()

    airports = conn.execute("""
    SELECT 
        iata,
        city,
        airport_name
    FROM airports
    WHERE country = ?
    AND iata IS NOT NULL
    AND iata <> ?
    ORDER BY city, airport_name
    """, (country, r"\N")).fetchall()

    conn.close()


    return jsonify([
        dict(row) for row in airports
    ])



@app.route("/")
def home():


    return render_template(
        "index.html"
    )




@app.route("/airport_info")
def airport_info():

    selected_airport_lat_long = None
    airlines = None
    top_destinations = None
    wiki_url = None
    selected_iata = None
    airport_current_temp = None

    conn = get_db_connection()

    #query for countries to display in country filter
    countries = conn.execute("""
                SELECT
                    DISTINCT country
                FROM airports
                ORDER BY country 
                """).fetchall()

    #get selected country from country filter
    selected_country = request.args.get("country")    
    
    if selected_country:
    
            #query for airports for selected country, if country selected
            airports = conn.execute("""
                SELECT
                    iata,
                    city,
                    country,
                    airport_name
                FROM airports
                WHERE country = ?
                ORDER BY country, city, airport_name
            """,(selected_country,)).fetchall()    

    else:
        #query for airports for all countries, if not country selected 
        airports = conn.execute("""
            SELECT
                iata,
                city,
                country,
                airport_name
            FROM airports
            WHERE iata IS NOT NULL
            AND iata <> ?
            ORDER BY country, city, airport_name
        """, (r"\N",)).fetchall()

    # get selected airport IATA from airport list
    selected_iata = request.args.get("iata")

    if selected_iata:

        # get airport lat/long
        selected_airport_lat_long = conn.execute("""
            SELECT
                airport_name,
                city,
                country,
                ROUND(latitude,2) AS latitude,
                ROUND(longitude,2) AS longitude,
                icao
            FROM airports
            WHERE iata = ?
        """, (selected_iata,)).fetchone()

        # get wikipedia page title using IATA
        page_title = get_wikipedia_page_title(selected_iata)

        if page_title:
            # get airlines and destinations for airport from airport wikipedia page, using wiki page title
            airlines = get_airlines_from_wikipedia(page_title)
            # get busiest routes for selected airport from wikipedia
            top_destinations = get_top_destinations_from_wikipedia(page_title)

        else:
            airlines = {}


        # for wikipedia airport page link
        wiki_url = None
        if page_title:
            wiki_url = (
                "https://en.wikipedia.org/wiki/"
                + quote(page_title.replace(" ", "_"))
            )


    #Google search link for selected city
    google_url = None
    if selected_airport_lat_long:

        airport_name = selected_airport_lat_long["airport_name"]

        if airport_name:
            google_url = (
                "https://www.google.com/search?q="
                + airport_name.replace(" ", "+")
            )
            
    # airport_name = selected_airport_lat_long[0]
    # if airport_name:
    #     google_url = f"https://www.google.com/search?q={airport_name}"
    # else:
    #     google_url = None


        page_title = get_wikipedia_page_title(selected_iata)

        if selected_airport_lat_long:
            selected_airport_icao = selected_airport_lat_long["icao"]   
            airport_current_weather = get_airport_current_weather(selected_airport_icao)

            if airport_current_weather is not None:
                airport_current_temp = round(airport_current_weather, 2)
            else:
                print("No weather data found or request failed.")
                airport_current_temp = None

            if not airport_current_weather:
                    
                    airport_current_temp = "N/A" # Clear fallback value for your HTML page
                              
        else:
            print(f"No airport found for IATA {selected_iata}")

 

    conn.close()

    return render_template(
        "airport_info.html",
        airports=airports,
        selected_airport_lat_long=selected_airport_lat_long,
        airlines=airlines,
        wiki_url=wiki_url,
        google_url=google_url,
        countries=countries,
        selected_country=selected_country,
        selected_iata=selected_iata,
        top_destinations=top_destinations,
        airport_current_temp=airport_current_temp
    )



# returns cities for a given country, used to populate city select list in city info page
@app.route("/api/cities")
def api_cities():

    country = request.args.get("country")
    conn = get_db_connection()

    cities = conn.execute("""
        SELECT 
            id, 
            city, 
            state, 
            ROUND(latitude, 2) AS latitude
        FROM cities
        WHERE country = ?
        ORDER BY state, city
    """, (country,)).fetchall()

    conn.close()

    return jsonify([
        dict(row) for row in cities
    ])
    
 



# page for cities with similar latitudes to selected city
@app.route("/cities_similar_latitude", methods=["GET", "POST"])
def cities():

    conn = get_db_connection()

    #query for countries to display in country filter
    countries = conn.execute("""
                SELECT
                    DISTINCT country
                FROM cities
                ORDER BY country 
                """).fetchall()

    #get selected country from country filter
    selected_country = request.args.get("country")  

    if selected_country:
        #get all cities from database to populate "select city " list, if country was selected
        cities = conn.execute("""
            SELECT
                city,
                state,
                country,
                ROUND(latitude, 2) AS latitude
            FROM cities
            WHERE country = ?
            ORDER BY state, city
        """,(selected_country,)).fetchall() 

    else:
        #get all cities from database to populate "select city " list, if country was not selected
        cities = conn.execute("""
            SELECT
                city,
                state,
                country,
                ROUND(latitude, 2) AS latitude
            FROM cities
            WHERE population > 100000
            ORDER BY country, state, city
        """).fetchall() 

    # 1. Grab the combined string from the HTML form submission
    raw_city_input = request.args.get("city")  # e.g., "Naples|40.85"
    
    # Initialize default values
    selected_city = None
    selected_latitude = None  
    selected_city_latitude = 0.0

    if raw_city_input:
        # 2. Split the string into two separate variables
        selected_city, latitude_str = raw_city_input.split("|")
        
        # 3. Convert the text latitude to a decimal number
        selected_latitude = float(latitude_str)      

    #get selected degrees from degree selector
    selected_degrees = request.args.get("degrees") 

    # convert to float/int, providing a default fallback if they are None or empty
    selected_degrees = float(selected_degrees) if selected_degrees else 0.0

    # 3. Use both fields in your SQL query to find the exact unique row
    row = conn.execute("""
        SELECT ROUND(latitude, 2) AS latitude 
        FROM cities 
        WHERE city = ? AND country = ?
    """, (selected_city, selected_country)).fetchone()
    
    if row:
        # Avoid row object errors by pulling index 0
        selected_city_latitude = float(row[0]) 

    # Calculate bounds 
    lat_max = round(selected_city_latitude + selected_degrees/2,2)
    lat_min = round(selected_city_latitude - selected_degrees/2,2)
    
    similar_latitude_cities = conn.execute("""
        SELECT
            city,
            state,
            country,
            ROUND(latitude, 2) AS latitude,
            ROUND(longitude, 2) AS longitude,
            population
        FROM cities
        WHERE latitude BETWEEN ? AND ?
        AND population > 100000
        ORDER BY country DESC, population DESC
        """,
        (
            lat_min,
            lat_max
        )
        ).fetchall()   

    #used for cities_same_latitude_map page
    session["selected_latitude"] = selected_city_latitude
    session["latitude_range"] = selected_degrees
    
    conn.close()

    return render_template(
        "cities_similar_latitude.html",
        cities=cities,
        countries=countries,
        selected_city=selected_city,
        selected_country=selected_country,
        selected_latitude=selected_latitude,
        similar_latitude_cities=similar_latitude_cities,
        lat_max=lat_max,
        lat_min=lat_min,
        selected_degrees=selected_degrees
    )



# page for cities sorted by latitude
@app.route("/cities_by_latitude", methods=["GET"])
def city_latitude():

    conn = get_db_connection()

    #query for countries to display in country filter
    countries = conn.execute("""
                SELECT
                    DISTINCT country
                FROM cities
                ORDER BY country 
                """).fetchall()

    #get selected country from country filter
    selected_country = request.args.get("country")    

    if selected_country:
    
        #get all cities from database to populate "select city " list, if country selected
        cities = conn.execute("""
            SELECT
                city,
                state,
                country,
                ROUND(latitude,2) AS latitude,
                population
            FROM cities
            WHERE country = ?
            AND population > 100000
            ORDER BY country, latitude DESC
        """,(selected_country,)).fetchall()    

    else:
        #query for cities for all countries, if not country selected
        cities = conn.execute("""
            SELECT
                city,
                state,
                country,
                ROUND(latitude,2) AS latitude,
                population
            FROM cities
            ORDER BY country, latitude DESC
        """).fetchall()

    conn.close()

    return render_template(
        "cities_by_latitude.html",
        cities=cities,
        countries=countries,
        selected_country=selected_country
    )



# page for finding cities within specified degrees of selected latitude
@app.route("/latitude_city_finder", methods=["GET"])
def latitude_city_finder():

    conn = get_db_connection()

    # Generates integers from 90 down to -90 inclusive
    latitudes = list(range(70, -56, -1))

    #get selected latitude from latitude selector
    selected_latitude = request.args.get("latitudes")   

    #get selected degrees from degree selector
    selected_degrees = request.args.get("degrees")   

    # convert to float/int, providing a default fallback if they are None or empty
    selected_latitude = float(selected_latitude) if selected_latitude else 0.0
    selected_degrees = float(selected_degrees) if selected_degrees else 0.0

    # Calculate bounds 
    lat_max = selected_latitude + selected_degrees/2
    lat_min = selected_latitude - selected_degrees/2

    #query for cities within specified degrees of latitude
    cities = conn.execute("""
        SELECT
            city,
            state,
            country,
            ROUND(latitude,2) AS latitude,
            population
        FROM cities
        WHERE population > 10000
        AND latitude BETWEEN ? AND ?
        ORDER BY country, population desc 
        """,
        (
            lat_min,
            lat_max
        )
        ).fetchall()

    conn.close()

    return render_template(
        "latitude_city_finder.html",
        cities=cities,
        latitudes=latitudes,
        selected_latitude=selected_latitude,
        selected_degrees=selected_degrees,
        lat_max=lat_max,
        lat_min=lat_min
    )



# airport map page
@app.route("/airport_map")
def map_page():

    selected_iata = request.args.get("iata")

    return render_template(
        "airport_map.html",
        selected_iata=selected_iata
        )



# API for getting data for airport map page
@app.route("/api/airports-for-map")
def get_airports():

    
    conn = sqlite3.connect(
        os.path.join(BASE_DIR, "airports.db")
    )
    # conn = sqlite3.connect("airports.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    airports = cursor.execute("""
        SELECT iata, airport_name, latitude, longitude
        FROM airports
    """).fetchall()

    conn.close()

    return jsonify([
        {
            "iata": airport["iata"],
            "name": airport["airport_name"],
            "lat": airport["latitude"],
            "lon": airport["longitude"]
        }
        for airport in airports
    ])



# API for getting data for city map page
@app.route("/api/cities-for-map")
def cities_for_map():
    
    conn = sqlite3.connect(
        os.path.join(BASE_DIR, "airports.db")
    )
    # conn = sqlite3.connect("airports.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cities = cursor.execute("""
        SELECT id, city, state, country, latitude, longitude
        FROM cities
    """).fetchall()

    conn.close()

    return jsonify([
        {
            "id": city["id"],
            "city": city["city"],
            "state": city["state"],
            "country": city["country"],
            "lat": city["latitude"],
            "lon": city["longitude"]
        }
        for city in cities
    ])



# city map page
@app.route("/city_map")
def city_map_page():

    selected_city_id = request.args.get("id", type=int)

    return render_template(
        "city_map.html",
        selected_city_id=selected_city_id
    )




@app.route("/cities_same_latitude_map")
def cities_same_latitude_map():

    selected_latitude = session.get("selected_latitude")
    latitude_range = session.get("latitude_range")

    if selected_latitude is None:
        return "No city selection found"

    lat_min = selected_latitude - latitude_range/2
    lat_max = selected_latitude + latitude_range/2

    conn = get_db_connection()

    cities = conn.execute("""
        SELECT
            city,
            state,
            country,
            latitude,
            longitude,
            population
        FROM cities
        WHERE latitude BETWEEN ? AND ?
            AND population > 100000
        ORDER BY country, latitude
    """,
    (
        lat_min,
        lat_max
    )).fetchall()


    # convert sqlite Row objects to dictionaries
    cities = [dict(row) for row in cities]

    conn.close()

    return render_template(
        "cities_same_latitude_map.html",
        cities=cities
    )



#page that lists airports by country 
@app.route("/airport_list")
def airport_list():

    conn = get_db_connection()

    #query for countries to display in country filter
    countries = conn.execute("""
                SELECT
                    DISTINCT country
                FROM airports
                ORDER BY country
                """).fetchall()

    #get selected country from country filter
    selected_country = request.args.get("country")  
    
    if selected_country:
    
        #query for airports for selected country, if country selected
        airports = conn.execute("""
            SELECT
                iata,
                city,
                country,
                airport_name,
                ROUND(latitude,2) AS latitude,
                ROUND(longitude,2) AS longitude
            FROM airports
            WHERE country = ?
            ORDER BY city, airport_name
        """,(selected_country,)).fetchall()    

    else:

        #query for airports for selected country, if country not selected
        airports = conn.execute("""
            SELECT
                iata,
                city,
                country,
                airport_name,
                ROUND(latitude,2) AS latitude,
                ROUND(longitude,2) AS longitude
            FROM airports
            ORDER BY city, airport_name
        """,).fetchall() 

    conn.close()

    return render_template(
        "airport_list.html",
        airports=airports,
        countries=countries,
        selected_country=selected_country
    )



def haversine_distance(lat1, lon1, lat2, lon2):
    # Earth's radius in kilometers. Use 3958.8 for miles.
    R = 6371.0
    
    # Convert degrees to radians
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    # Haversine formula core steps
    a = (math.sin(delta_phi / 2) ** 2 + 
         math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2)
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    # Calculate total distance in miles
    distance = int(round(R * c * 0.621371,0))  # Convert km to miles and round to nearest whole number

    return distance



#page that calculates straight-line distance between two USA cities over 100k population.
@app.route("/city_distance")
def city_distance():

    conn = get_db_connection()

    # get list of USA cities
    cities = conn.execute("""
        SELECT
            id,
            city,
            state,
            country,
            ROUND(latitude,2) AS latitude,
            ROUND(longitude,2) AS longitude
        FROM cities
        WHERE population > 100000
        ORDER BY country, state, city 
    """,).fetchall() 

    # get selected city 1
    selected_city_1_id = request.args.get("city_1")  
    
    # get selected city 2
    selected_city_2_id = request.args.get("city_2")  

    # Initialize distance variable
    distance = None

    # 3. ONLY run the calculation if the user has actually selected cities
    if selected_city_1_id and selected_city_2_id:

        # get lat and lon of city 1
        city_1_lat_lon = conn.execute("""
            SELECT
                ROUND(latitude,2) AS latitude,
                ROUND(longitude,2) AS longitude
            FROM cities
            WHERE id = ? 
        """,(selected_city_1_id,)).fetchall() 

        #get first row of city 1
        if city_1_lat_lon:
            city_1_lat_lon = city_1_lat_lon[0]
        else:
            # Handle the missing city error gracefully
            return "Error: City 1 not found in the database", 404

        # get lat and lon of city 2
        city_2_lat_lon = conn.execute("""
            SELECT
                ROUND(latitude,2) AS latitude,
                ROUND(longitude,2) AS longitude
            FROM cities
            WHERE id = ? 
        """,(selected_city_2_id, )).fetchall() 

        #get first row of city 2
        if city_2_lat_lon:
            city_2_lat_lon = city_2_lat_lon[0]
        else:
            # Handle the missing city error gracefully
            return "Error: City 2 not found in the database", 404

        # calculate distance
        distance = haversine_distance(city_1_lat_lon['latitude'], city_1_lat_lon['longitude'], city_2_lat_lon['latitude'], city_2_lat_lon['longitude'])
        
    conn.close()

    selected_city_1_id = int(selected_city_1_id) if selected_city_1_id and selected_city_1_id.isdigit() else None
    selected_city_2_id = int(selected_city_2_id) if selected_city_2_id and selected_city_2_id.isdigit() else None


    return render_template(
        "city_distance.html",
        cities=cities,
        distance=distance,
        selected_city_1_id=selected_city_1_id,
        selected_city_2_id=selected_city_2_id
    )



# returns all cities for a country to display in "info for all cities" of city info page
@app.route("/api/cities-for-google")
def api_cities_for_google():

    # Capture the ?country= value from the fetch URL request
    country = request.args.get("country")
    if not country:
        return jsonify([]), 400 # Return bad request error if empty

    conn = get_db_connection()

    cities = conn.execute("""     
       WITH country_sizes AS (
            SELECT country
            FROM cities 
            GROUP BY country 
            HAVING COUNT(*) > 50  -- Defines a "large" country by total city records
        )
        SELECT 
            id, city, state, latitude, longitude, population
        FROM cities 
        WHERE 
            ((country IN (SELECT country FROM country_sizes) AND population > 50000)
            OR 
            (country NOT IN (SELECT country FROM country_sizes)))
        AND country = ?
        ORDER BY population DESC
    """, (country,)).fetchall()

    conn.close()

    # Serialize results to pure dictionary
    data = []
    for city in cities:
        data.append({
            'id': city['id'],
            'city': city['city'],
            'state': city['state'],
            'latitude': city['latitude'],
            'longitude': city['longitude'],
            'population': city['population']
        })
        
    return jsonify(data)



# page that displays city information for selected city, including population, latitude, longitude, and sunrise/sunset times
@app.route("/city_info")
def city_info():

    conn = get_db_connection()

    selected_city_id = request.args.get("city", type=int)
    
    #query for countries to display in country filter
    countries = conn.execute("""
                SELECT
                    DISTINCT country
                FROM cities
                ORDER BY country
                """).fetchall()

    #get selected country from country filter
    selected_country = request.args.get("country")  

    if selected_country:
        #get all cities from database to populate "select city " list, if country was selected
        cities = conn.execute("""
            SELECT
                id,
                city,
                state,
                country,
                ROUND(latitude, 2) AS latitude,
                ROUND(longitude, 2) AS longitude,
                population
            FROM cities
            WHERE country = ?
            ORDER BY state, city
        """,(selected_country,)).fetchall() 

    elif selected_city_id:
    
        #get city data for randomly selected city feature
        cities = conn.execute("""
            SELECT
                id,
                city,
                state,
                country,
                ROUND(latitude, 2) AS latitude,
                ROUND(longitude, 2) AS longitude,
                population
            FROM cities
            WHERE id = ?
            ORDER BY country, state, city
        """,(selected_city_id,)).fetchall() 

    else: 
        cities = []

    # get country for random city selection
    if selected_country is None:
        selected_country = conn.execute("""
            SELECT country
            FROM cities
            WHERE id = ?
        """, (selected_city_id,)).fetchone()
        
        if selected_country:
            selected_country = selected_country["country"]
        else:
            selected_country = None

    # get selected city name, latitude, longitude, and population 
    city_data = conn.execute("""
            SELECT
                city,
                state,
                population,
                ROUND(latitude,2) AS latitude,
                ROUND(longitude,2) AS longitude
            FROM cities
            WHERE id = ? 
        """, (selected_city_id,)).fetchone()

    selected_city = city_data["city"] if city_data else None

    selected_state = city_data["state"] if city_data else None
    if selected_state == "":
            selected_state = "No State"

    latitude = city_data["latitude"] if city_data else None
    selected_latitude = city_data["latitude"] if city_data else None
    if selected_latitude is not None:
            selected_latitude = float(selected_latitude)    #convert from string to float

    longitude = city_data["longitude"] if city_data else None

    population = city_data["population"] if city_data else None


    # get sunrise/sunset times for selected city from API
    sunrise_sunset_times = None


    sunrise_sunset_times = requests.get(f"https://api.sunrise-sunset.org/v2?lat={latitude}&lng={longitude}")

    # check if the API request was successful
    if sunrise_sunset_times.status_code == 200:
        sunrise_sunset_times = sunrise_sunset_times.json()
        sunrise = sunrise_sunset_times["sunrise"]
        sunset = sunrise_sunset_times["sunset"]
    else:
        sunrise = None
        sunset = None

    conn.close()

    # convert sunrise and sunset times to preferred format (e.g., 12-hour format with AM/PM)
    if sunrise:
        # Parse the ISO 8601 string into a timezone-aware datetime object
        sunrise = datetime.fromisoformat(sunrise)
       
        # Extract and format the components
        date_part = sunrise.strftime("%m-%d-%Y")  # MM-DD-YYYY
        time_part = sunrise.strftime("%I:%M %p")     # 12HR:MIN

        # Extract the timezone offset hours and minutes (e.g., -04:00)
        tz_offset = sunrise.strftime("%z")
        offset_part = f"{tz_offset[:3]}:{tz_offset[3:]}"

        # Combine into the final format
        sunrise = f"{date_part} {time_part}{offset_part}"

    if sunset:
        # Parse the ISO 8601 string into a timezone-aware datetime object
        sunset = datetime.fromisoformat(sunset)
       
        # Extract and format the components
        date_part = sunset.strftime("%m-%d-%Y")  # MM-DD-YYYY
        time_part = sunset.strftime("%I:%M %p")     # 12HR:MIN

        # Extract the timezone offset hours and minutes (e.g., -04:00)
        tz_offset = sunset.strftime("%z")
        offset_part = f"{tz_offset[:3]}:{tz_offset[3:]}"

        # Combine into the final format
        sunset = f"{date_part} {time_part}{offset_part}"


    #wikipedia page link for selected city
    if selected_city and selected_state and selected_country == 'United States':
        wiki_url = f"https://en.wikipedia.org/wiki/{selected_city.replace(' ', '_')},_{selected_state.replace(' ', '_')}"
    else:
        wiki_url = None

    #Google search link for selected city
    if selected_city and selected_state:
        google_url = f"https://www.google.com/search?q={selected_city}+{selected_state}"
    else:
        google_url = None


    return render_template(
        "city_info.html",
        countries=countries,
        cities=cities,
        selected_city_id=selected_city_id,
        selected_country=selected_country,
        selected_city=selected_city,
        selected_state=selected_state,
        selected_latitude=selected_latitude,
        latitude=latitude,
        longitude=longitude,
        sunrise=sunrise,
        sunset=sunset,
        population=population,
        wiki_url=wiki_url,
        google_url=google_url
    )

    


@app.route("/random_airport")
def random_airport():

    conn = get_db_connection()

    airport = conn.execute("""
        SELECT iata
        FROM airports
        WHERE iata IS NOT NULL
        ORDER BY RANDOM()
        LIMIT 1
    """).fetchone()
    
    conn.close()

    if airport:
        return redirect(f"/airport_info?iata={airport['iata']}")

    return "No airports found"




@app.route("/random_city")
def random_city():

    conn = get_db_connection()

    city_id = conn.execute("""
        SELECT id
        FROM cities
        ORDER BY RANDOM()
        LIMIT 1
    """).fetchone()[0]

    conn.close()

    if city_id:
        return redirect(f"/city_info?city={city_id}")

    return "No cities found"


def openai_key():

    import os

    print("API key exists:", bool(os.getenv("OPENAI_API_KEY")))
    print("API key prefix:", os.getenv("OPENAI_API_KEY", "")[:10])



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)