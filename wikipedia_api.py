import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import unquote
import pandas as pd 


HEADERS = {
    "User-Agent": "AirportDistancePortfolio/1.0"
}


def get_wikipedia_page_title(iata):

    # do not try to fetch wiki page if airport does not have an iata code
    if not iata or iata == r"\N":
        return None


    query = f"""
    SELECT ?article WHERE {{
      ?airport wdt:P238 "{iata}".

      ?article schema:about ?airport ;
               schema:isPartOf <https://en.wikipedia.org/> .
    }}
    """


    response = requests.get(
        "https://query.wikidata.org/sparql",
        params={
            "query": query,
            "format": "json"
        },
        headers=HEADERS
    )


    if response.status_code != 200:
        print("Wikidata error:", response.status_code)
        print(response.text[:200])
        return None


    try:
        data = response.json()

    except ValueError:
        print("Wikidata did not return JSON")
        print(response.text[:200])
        return None


    bindings = data.get("results", {}).get("bindings", [])


    if not bindings:
        print("No Wikipedia page found for:", iata)
        return None


    url = bindings[0]["article"]["value"]

    page_title = url.split("/")[-1]

    page_title = unquote(page_title)

    return page_title



def get_airlines_from_wikipedia(page_title):

    url = "https://en.wikipedia.org/w/api.php"

    headers = {
        "User-Agent": "AirportDistancePortfolio/1.0"
    }

    params = {
        "action": "parse",
        "page": page_title,
        "prop": "sections",
        "format": "json"
    }

    response = requests.get(
        url,
        params=params,
        headers=headers,
        timeout=10
    )

    try:
        data = response.json()
        print(data)
    except ValueError:
        print(f"{page_title}: Invalid response from Wikipedia")
        return {}

    # data = response.json()

    # Safety check: did Wikipedia return a valid page?
    if "parse" not in data:
        print("Wikipedia page not found.")
        return {}
            
      
    # Find Airlines and destinations section
    section_number = None

    for section in data["parse"]["sections"]:
        if "airlines and destinations" in section["line"].lower() or "airline and destinations" in section["line"].lower() or "airlines and destination" in section["line"].lower() or "airline and destination" in section["line"].lower():
            section_number = section["index"]
            break

    # Safety check: no Airlines and destinations section found
    if section_number is None:
        print("No Airlines and destinations section found")
        return {}

    # Get that section's HTML
    params = {
        "action": "parse",
        "page": page_title,
        "prop": "text",
        "section": section_number,
        "format": "json"
    }

    response = requests.get(
        url,
        params=params,
        headers=headers
    )

    html = response.json()["parse"]["text"]["*"]

    soup = BeautifulSoup(html, "html.parser")

    airlines = {}

    for table in soup.find_all("table"):

        for row in table.find_all("tr")[1:]:

            cells = row.find_all(["th", "td"])

            if len(cells) >= 2:

                airline = cells[0].get_text(" ", strip=True)

                # Remove citation references
                for sup in cells[1].find_all("sup"):
                    sup.decompose()

                destinations = []

                for item in cells[1].contents:

                    text = item.get_text(" ", strip=True) if hasattr(item, "get_text") else str(item).strip()

                    # ignore commas and empty values
                    if text and text != ",":
                        destinations.append(text)

                # clean whitespace
                destinations = [
                    d.strip()
                    for d in destinations
                ]

                airlines[airline] = destinations

    return airlines



def get_top_destinations_from_wikipedia(page_title):

    url = f"https://en.wikipedia.org/wiki/{page_title}"

    html = requests.get(url, headers=HEADERS).text

    soup = BeautifulSoup(html, "html.parser")

    domestic_routes = []
    international_routes = []

    for table in soup.find_all("table", class_="wikitable"):

        caption = table.find("caption")

        if not caption:
            continue

        if caption and "Busiest domestic routes" in caption.get_text(strip=True):

            domestic_routes = []

            for tr in table.find_all("tr")[1:]:

                cells = tr.find_all(["td","th"])

                if len(cells) == 3:
                
                    domestic_routes.append({
                        "rank": cells[0].get_text(" ", strip=True),
                        "destination": cells[1].get_text(" ", strip=True),
                        "passengers": cells[2].get_text(" ", strip=True),
                    })   

                if len(cells) > 3:

                    domestic_routes.append({
                        "rank": cells[0].get_text(" ", strip=True),
                        "destination": cells[1].get_text(" ", strip=True),
                        "passengers": cells[2].get_text(" ", strip=True),
                        "airline": cells[3].get_text(" ", strip=True)
                    })  

                else:

                    continue
                
                    
        elif caption and "Busiest international routes" in caption.get_text(strip=True):

            international_routes = []

            for tr in table.find_all("tr")[1:]:

                cells = tr.find_all(["td","th"])

                if len(cells) == 3:
                
                    international_routes.append({
                        "rank": cells[0].get_text(" ", strip=True),
                        "destination": cells[1].get_text(" ", strip=True),
                        "passengers": cells[2].get_text(" ", strip=True),
                    })

                elif len(cells) > 3:

                    international_routes.append({
                        "rank": cells[0].get_text(" ", strip=True),
                        "destination": cells[1].get_text(" ", strip=True),
                        "passengers": cells[2].get_text(" ", strip=True),
                        "airline": cells[3].get_text(" ", strip=True)
                    })  

                else:

                    continue

    if not domestic_routes:
        domestic_routes = 'No domestic routes found'
    if not international_routes:
        international_routes = 'No international routes found'

    return {
        "domestic": domestic_routes,
        "international": international_routes
    }




# page_title = get_wikipedia_page_title('DTW')
# get_top_destinations_from_wikipedia(page_title)