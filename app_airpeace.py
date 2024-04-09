import json
import logging
import time

from bs4 import BeautifulSoup
from selenium import webdriver

logger = logging.getLogger(__name__)


class AirPeace:
    """
    Class to query flights on Airpeace
    """

    def __init__(
        self,
        fly_from,
        fly_to,
        dep_date,
        trip_type,
        return_date=None,
    ):
        """
        Initialize the class instance

        fly_from: Departure location
        fly_to: Arrival location
        dep_date: Departure date
        trip_type: Type of trip (One way or round trip)
        return_date: Date of return flight
        """
        self.fly_from = fly_from
        self.fly_to = fly_to
        self.dep_date = dep_date
        self.trip_type = trip_type
        self.logger = logger
        self.return_date = return_date if trip_type == "ROUND_TRIP" else None

        logging.basicConfig(level=logging.INFO)
        

    def get_url(self):
        """
        This method returns the url of airpeace

        Returns:
            str: Url of airpeace
        """
        url1 = f"https://book-airpeace.crane.aero/ibe/availability?tripType={self.trip_type}&depPort={self.fly_from}&arrPort={self.fly_to}&departureDate={self.dep_date}%20%20%20%20%20%20%20%20&adult=1&child=0&infant=0&returnDate={self.return_date}&lang=en"
        return url1


    def capture_page_source(self):
        """
        This method retrieves the page source of the AirPeace website utilizing the Selenium WebDriver.

        Returns:
            str: html apge source.
        """
        driver = webdriver.Chrome()
        url = self.get_url()
        driver.get(url)
        time.sleep(7)
        html_content = driver.page_source
        driver.quit()
        return html_content


    def transform(self, flight):
        """
        This method extracts pertinent flight details, processes them through parsing and transformation,
        and then returns a dictionary containing the resulting data for a single flight.

        Args:
            flight (str): HTML string for a single flight.

        Returns:
            Dict: Dictionary containing flight data
        """

        departure_html = flight.find(
            "div", class_="info-block left-info-block text-left"
        )
        departure_list = departure_html.text.strip().split()
        departure_time = departure_list[0]
        departure_location = departure_list[2]
        departure_date = f"{departure_list[4]}:{departure_list[5]}:{departure_list[6]}"

        flight_html = flight.find("div", class_="middle-block")
        flight_list = flight_html.text.strip().split()
        flight_no = flight_list[0]
        flight_stop = flight_list[3]
        flight_duration = f"{flight_list[1]} {flight_list[2]}"

        arrival_html = flight.find(
            "div", class_="info-block right-info-block text-right"
        )
        arrival_list = arrival_html.text.strip().split()
        arrival_time = arrival_list[0]
        arrival_location = arrival_list[1]
        arrival_date = f"{arrival_list[3]}:{arrival_list[4]}:{arrival_list[5]}"

        price_list = []
        for i in flight.find_all("div", class_="flight-table__flight-type"):
            price = i.text.strip().split()
            price_list.append(price)

        for i in price_list:
            economy_price = f"{price_list[0][-2]}{price_list[0][-1]}"
            premium_economy = f"{price_list[1][-2]}{price_list[1][-1]}"
            business_price = f"{price_list[2][-2]}{price_list[2][-1]}"

        flight_data = {
            "dep_time": departure_time,
            "dep_location": departure_location,
            "dep_date": departure_date,
            "flight_no": flight_no,
            "flight_stops": flight_stop,
            "flight_duration": flight_duration,
            "arrival_time": arrival_time,
            "arrival_location": arrival_location,
            "arrival_date": arrival_date,
            "economy_price": economy_price,
            "premium_economy": premium_economy,
            "business_price": business_price,
        }

        return flight_data



    def get_flight_info(self):
        """
        This function employs Beautiful Soup to parse HTML data,
        transforming it into JSON format before returning the flight data.

        Returns:
            dict: A dictionary containing multiple pieces of transformed flight data.
        """

        html_content = self.capture_page_source()
        soup = BeautifulSoup(html_content, "html.parser")
        final_dict = []
        departure_list = soup.find(id="availability-flight-table-0").find_all(
            "div", class_="row w-100 no-gutters"
        )
        departure = list(map(self.transform, departure_list))
        try:
            return_list = soup.find(id="availability-flight-table-1").find_all(
                "div", class_="row w-100 no-gutters"
            )
            logging.info("This is a round trip")
            returns = list(map(self.transform, return_list))

        except AttributeError:
            logging.info("This is a one way trip")

        if self.trip_type == "ROUND_TRIP":
            data = {"Departure": departure, "Return": returns}
            final_dict.append(data)

        elif self.trip_type == "ONE_WAY":
            data = data = {"Departure": departure}
            final_dict.append(data)

        json_data = json.dumps(data, indent=4, ensure_ascii=False)

        return json_data


if __name__ == "__main__":
    airpeace = AirPeace("ABV", "LOS", "16.04.2024", "ONE_WAY", "20.04.2024")
    print(airpeace.get_flight_info())
