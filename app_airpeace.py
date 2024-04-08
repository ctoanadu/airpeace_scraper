import json
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC



class AirPeace:
    def __init__(
        self,
        fly_from,
        fly_to,
        dep_date,
        trip_type,
        return_date=None,
    ):

        self.fly_from = fly_from
        self.fly_to = fly_to
        self.dep_date = dep_date
        self.trip_type = trip_type
        self.return_date = return_date if trip_type == "ROUND_TRIP" else None

    def get_url(self):
        url1 = f"https://book-airpeace.crane.aero/ibe/availability?tripType={self.trip_type}&depPort={self.fly_from}&arrPort={self.fly_to}&departureDate={self.dep_date}%20%20%20%20%20%20%20%20&adult=1&child=0&infant=0&returnDate={self.return_date}&lang=en"
        return url1

    def capture_html_page(self):
        driver = webdriver.Chrome()
        url = self.get_url()
        driver.get(url)
        time.sleep(7)
        html_content = driver.page_source
        driver.quit()
        return html_content

    def tranaform(self, stringss):

        left = stringss.find("div", class_="info-block left-info-block text-left")
        list_of_left = left.text.strip().split()
        departure_time = list_of_left[0]
        departure_location = list_of_left[2]
        departure_date = f"{list_of_left[4]}:{list_of_left[5]}:{list_of_left[6]}"

        middle = stringss.find("div", class_="middle-block")
        list_of_middle = middle.text.strip().split()
        flight_no = list_of_middle[0]
        flight_stop = list_of_middle[3]
        flight_duration = f"{list_of_middle[1]} {list_of_middle[2]}"

        right = stringss.find("div", class_="info-block right-info-block text-right")
        list_of_right = right.text.strip().split()
        arrival_time = list_of_right[0]
        arrival_location = list_of_right[1]
        arrival_date = f"{list_of_right[3]}:{list_of_right[4]}:{list_of_right[5]}"

        price_list = []
        for i in stringss.find_all("div", class_="flight-table__flight-type"):
            price = i.text.strip().split()
            price_list.append(price)

        for i in price_list:
            economy_price = f"{price_list[0][-2]}{price_list[0][-1]}"
            premium_economy = f"{price_list[1][-2]}{price_list[1][-1]}"
            business_price = f"{price_list[2][-2]}{price_list[2][-1]}"

        dictt = {
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

        return dictt

    def get_flight_info(self):
        html_content = self.capture_html_page()
        soup = BeautifulSoup(html_content, "html.parser")
        final_dict = []
        departure_list = soup.find(id="availability-flight-table-0").find_all(
            "div", class_="row w-100 no-gutters"
        )
        departure = list(map(self.tranaform, departure_list))

        try:
            return_list = soup.find(id="availability-flight-table-1").find_all(
                "div", class_="row w-100 no-gutters"
            )
            returns = list(map(self.tranaform, return_list))
        except Exception as e:
            print("This is oneway")

        if self.trip_type == "ROUND_TRIP":
            data = {"Departure": departure, "Return": returns}
            final_dict.append(data)

        elif self.trip_type == "ONE_WAY":
            data = data = {"Departure": departure}
            final_dict.append(data)

        json_data = json.dumps(data, indent=4, ensure_ascii=False)

        return json_data


if __name__ == "__main__":
    airpeace = AirPeace("ABV", "LOS", "16.04.2024", "ONE_WAY")
    print(airpeace.get_flight_info())
