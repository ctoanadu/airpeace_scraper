# AirPeace Flight Information Web Scraper
✈️ Python wrapper for https://flyairpeace.com/ ✈️

## Overview

This project is a Python-based web scraper built to extract flight information from the AirPeace website. It provides a convenient way to access flight details such as flight duration, flight fare, departure time, estimated time of arrival, flight code. The scraper is implemented using Python and utilizes BeautifulSoup and Selenium for web scraping tasks.

## Installation

To use this web scraper, follow these steps:

1. Clone or download the repository to your local machine:

```
pip install -e git+https://github.com/ctoanadu/airpeace_scraper.git
```

2. Install the required dependencies using pip:

```
pip install -r requirements.txt
```

3. Once dependencies are installed, you can import the `AirPeaceFlightCheck` class from `src.app_airpeace` module in your Python code.

## Usage

To use the scraper, create an instance of the `AirPeaceFlightCheck` class with the required parameters and call the `get_flight_info()` method to retrieve flight information. Here's an example:

```python
from src.app_airpeace import AirPeaceFlightCheck

airpeace = AirPeaceFlightCheck("LOS", "LGW", "16.04.2024", "ROUND_TRIP", "20.04.2024")

flight_info = airpeace.get_flight_info()
print(flight_info)
```

## Output

The `get_flight_info()` method returns flight information in a structured format. Here's an example of the return:

```json
{
    "Departure": [
        {
            "dep_time": "23:59",
            "dep_location": "Lagos",
            "dep_date": "16:Apr:2024",
            "flight_no": "P4-7578",
            "flight_stops": "Nonstop",
            "flight_duration": "6h 41m",
            "arrival_time": "06:40",
            "arrival_location": "London",
            "arrival_date": "17:Apr:2024",
            "economy_price": "£552.80",
            "premium_economy": "£604.70",
            "business_price": "NoSeat"
        }
    ],
    "Return": [
        {
            "dep_time": "11:10",
            "dep_location": "London",
            "dep_date": "20:Apr:2024",
            "flight_no": "P4-7579",
            "flight_stops": "Nonstop",
            "flight_duration": "6h 40m",
            "arrival_time": "17:50",
            "arrival_location": "Lagos",
            "arrival_date": "20:Apr:2024",
            "economy_price": "£461.20",
            "premium_economy": "NoSeat",
            "business_price": "£1,325.20"
        }
    ]
}
```
## Parameters

When creating an instance of `AirPeaceFlightCheck`, the following parameters are required:

- `departure_city`: The IATA code of the departure city.
- `arrival_city`: The IATA code of the arrival city.
- `departure_date`: The departure date in the format "dd.mm.yyyy".
- `trip_type`: The type of trip, either "ONE_WAY" or "ROUND_TRIP".
- `return_date` (optional): Required if `trip_type` is "ROUND_TRIP". The return date in the format "dd.mm.yyyy".


## Limitations

- The scraper relies on the structure of the AirPeace website, and any changes to the website layout or structure may cause the scraper to fail.
- Continuous usage of web scraping techniques might violate the terms of service of the website being scraped. Ensure compliance with website terms and conditions.

## Disclaimer

This project is for educational purposes only. The developers do not endorse or promote unauthorized access to websites or any illegal activities.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Authors

- [Chukwudi To-Anadu](https://github.com/ctoanadu) - Initial work

## Contribution

Contributions are welcome! Please open an issue or submit a pull request with any improvements or fixes.

