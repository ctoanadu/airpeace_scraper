from src.app_airpeace import AirPeaceFlightCheck

airpeace= AirPeaceFlightCheck("LOS", "LGW", "16.04.2024", "ROUND_TRIP", "20.04.2024")

print (airpeace.get_flight_info())
