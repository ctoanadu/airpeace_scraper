from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AirPeace:
    def __init__(
        self,
        fly_from,
        fly_to,
        dep_date,
        return_date=None,
        adult=1,
        child=0,
        infant=0,
        return_trip=True
    ):

        self.fly_from = fly_from
        self.fly_to = fly_to
        self.dep_date = dep_date
        self.return_date = return_date if return_trip else None
        self.adult = adult
        self.child = child
        self.infant = infant
        self.return_trip=return_trip
        

    def get_url(self):
        if self.return_trip:
            trip='ROUND_TRIP'
        else:
            trip='ONE_WAY'

        url1 = f"https://book-airpeace.crane.aero/ibe/availability?tripType={trip}&depPort={self.fly_from}&arrPort={self.fly_to}&departureDate={self.dep_date}%20%20%20%20%20%20%20%20&adult={self.adult}&child={self.child}&infant={self.infant}&returnDate={self.return_date}&lang=en"
        return url1
        
        
            

    def capture_html_page(self, get_url):
        driver = webdriver.Chrome()

        driver.get(get_url)
        html_content = driver.page_source

        driver.quit()
        return html_content

    def parse_html(self):
        html_page_source = self.capture_html_page
        data = {
            "Departure": {
                "time": [],
                "economy_price": "",
                "premium_economy_price": "",
                "business_price": "",
            },
            "Return": {
                "time": [],
                "economy_price": "",
                "premium_economy_price": "",
                "business_price": "",
            },
        }

        return data


if __name__ == "__main__":
    pass
    