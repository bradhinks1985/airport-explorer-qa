import requests


# Function to get current temperature for a given airport using the Aviation Weather Center API. Used in airport_info.py to display current temperature on airport info page.
def get_airport_current_weather(icao_id):

    url = "https://aviationweather.gov/api/data/metar"

    # icao_id = 'KDTW'

    # Needed so I don't get blocked for calling API as bot.
    headers = {
        "User-Agent": "MyWeatherApp/1.0 (contact@example.com)"
    }

    params = {
        "ids": icao_id,
        "format": "json"
    }

    response = requests.get(url, params=params, headers=headers)
    
    try:
        # Returns empty list if status is 204 (No Content)
        if response.status_code == 200:
            data = response.json()  # This is a list: [ {...} ]
            
            # 1. Check if the list actually contains any data
            if len(data) > 0:
                # 2. Extract the first report dictionary from the list, then get 'temp'
                temp_c = data[0].get("temp") 
                temp_f = temp_c*9/5 + 32
                return temp_f
                
        return None  # Return None if no data found or server returned 204
    except Exception as e:
        print(f"Error: {e}")
        return None
    



