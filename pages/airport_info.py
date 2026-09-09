from playwright.sync_api import Page
import sqlite3, os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_db_connection():
    conn = sqlite3.connect(
        os.path.join(BASE_DIR, "airports.db")
    )
    conn.row_factory = sqlite3.Row
    return conn



# Airport Info page object model
class AirportInfoPage:
    def __init__(self, page: Page):
        self.page = page

        # Airport information page navigation
        self.airport_info_link = page.get_by_role("link", name="Airport Info")

        # Form controls
        self.country_select = page.locator("#countrySelect")
        self.airport_select_wrapper = page.locator(
            "#airportSelectWrapper"
        )


        self.airport_select = page.locator("#airportSelect")
        self.airport_select_control = page.locator(
            "#airportSelect + .ts-wrapper .ts-control"
        )
        self.airport_search = page.locator("#airportSelect-ts-control")


        # self.airport_select = page.locator("#airportSelect-ts-control")
        # self.airport_select_control = page.locator(
        #     "#airportSelect + .ts-wrapper .ts-control"
        # )

        # self.airport_select = page.locator("#airportSelect")

        # self.airport_search = page.locator(
        #     "#airportSelect-ts-control"
        # )
        self.select_airport_button = page.get_by_role("button", name="Select Airport")
        # self.select_airport_button = page.get_by_text("Select Airport")

        self.generate_random_airport_button = page.locator("#random-airport-button")

        # ai summary
        self.ai_summary_link = page.get_by_role("link", name="View AI Summary")
        self.history_summary = page.locator("#history")

        # google search
        self.google_search_link = page.get_by_role("link", name="Search Google")

        # wiki page
        self.wiki_page_link = page.get_by_role("link", name="View Wikipedia page")

        # view on map
        self.view_map_link = page.get_by_role("link", name="View on Map")
        self.map_page_title = page.get_by_text(
            "Airport Map",
            exact=True
        )



        # Airport information section
        self.airport_info = page.locator(".card").filter(
            has_text="Airport Information"
        )

        self.airport_name = self.airport_info.locator("p").nth(0)
        self.city_country = self.airport_info.locator("p").nth(1)
        self.latitude = self.airport_info.locator("p").nth(2)
        self.longitude = self.airport_info.locator("p").nth(3)
        self.temperature = self.airport_info.locator("p").nth(4)


        ### busiest domestic routes section ###

        # busiest domestic routes card  
        self.domestic_routes_card = page.locator(".card").filter(
            has=page.get_by_text("Busiest Domestic Routes", exact=True))

        # first domestic route
        self.domestic_route_destination = (
            self.domestic_routes_card
            .locator("tbody tr")
            .nth(0)
            .locator("td")
            .nth(1)
        )


        ### busiest international routes section ###

        # busiest international routes card
        self.international_routes_card = page.locator(".card").filter(
            has=page.get_by_text("Busiest International Routes", exact=True)
        )

        # first international route
        self.international_route_destination = (
            self.international_routes_card
            .locator("tbody tr").nth(0)
            .locator("td").nth(1)
        )


        ### airlines and destinations section ###

        # airlines and destinations card
        self.airlines_destinations_card = page.locator(".card").filter(
            has=page.get_by_text("Airlines and Destinations", exact=True)
        )

        # A & L card title for opening in get_airline_air_dest(self)
        self.airline_air_dest_summary = self.airlines_destinations_card.get_by_text(
            "Airlines and Destinations",
            exact=True
        )

        # first airline in airlines and destinations card
        self.airline_air_dest = (
            self.airlines_destinations_card
            .locator("h3").nth(0)
        )

        # first destination of first airline
        self.destination_air_dest = (
            self.airlines_destinations_card
            .locator("ul").nth(0)
            .locator("li").nth(0)
        )


    ### Actions ###

    # navigate to airport info page
    def go_to_airport_info_page(self, country=None):
        self.airport_info_link.click()

        if country:
            self.page.goto(
                f"http://127.0.0.1:5000/airport_info?country={country}"
            )


    def select_country(self, country):
        self.country_select.select_option(label=country)
        self.airport_select_wrapper.wait_for(state="visible")
        
    def select_airport(self, airport_name, airport_iata):
        self.airport_select_wrapper.wait_for(state="visible")
        self.airport_select.select_option(airport_iata)
        
    # def select_airport(self, airport_name, airport_iata):
    #     self.airport_select_wrapper.wait_for(state="visible")
    #     self.airport_select_control.click()
    #     self.airport_search.fill(airport_name)
    #     airport_option = self.page.locator(
    #         f'[data-value="{airport_iata}"]'
    #     )
    #     airport_option.wait_for(state="visible")
    #     airport_option.click()        # self.page.locator(f'[data-value="{airport_iata}"]').click()

    #     # Verify Tom Select actually selected the airport
    #     selected_value = self.page.locator("#airportSelect").input_value()
    #     print("SELECTED AIRPORT VALUE:", selected_value)


    def generate_random_airport(self):
        self.generate_random_airport_button.click()

    
    ### ai summary
    def view_ai_summary(self):
        self.ai_summary_link.click()

    def get_airport_ai_history(self):
        return self.history_summary.inner_text().strip()

    # get history summary from db
    def get_airport_ai_history_db(self, airport_iata):
        conn = get_db_connection()
        
        #query for airport's history
        history = conn.execute("""
                    SELECT
                        history
                    FROM airports
                    WHERE iata = ?
                    """,(airport_iata,)).fetchone()
        return history


    def search_google(self):
        self.google_search_link.click()

    def view_wiki_page(self):
        self.wiki_page_link.click()

    def view_on_map(self):
        self.view_map_link.click()


    def get_airport_info(self):
            return {
                "airport_name": self.airport_name.inner_text().strip(),
                "city_country": self.city_country.inner_text().strip(),
                "latitude": self.latitude.inner_text().strip(),
                "longitude": self.longitude.inner_text().strip(),
                "temperature": self.temperature.inner_text().strip()
            }    


    # busiest domestic routes
    def open_domestic_routes(self):
        self.domestic_routes_card.click()        

    def get_domestic_route_destination(self):
        if not self.domestic_routes_card.is_visible():
            return None
        return self.domestic_route_destination.inner_text().strip()


    # busiest international routes
    def open_international_routes(self):
        self.international_routes_card.click()       

    def get_international_route_destination(self):
        if not self.international_routes_card.is_visible():
            return None
        return self.international_route_destination.inner_text().strip()


    # airlines and destinations
    def open_airlines_destinations(self):
            self.airlines_destinations_card.click()   

        # get first airline    
    def get_airline_air_dest(self):
            if not self.airlines_destinations_card.is_visible():
                return None
            return self.airline_air_dest.inner_text().strip()

        # get first destination of first airline    
    def get_destination_air_dest(self):
            if not self.airlines_destinations_card.is_visible():
                return None
            return self.destination_air_dest.inner_text().strip()




