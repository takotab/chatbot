# from pyowm import OWM
# from pyowm import timeutils
from datetime import datetime, timedelta
import random


def weather(city, time, language_):
    if random.random() > 0.5:
        return "rainy", "8"
    else:
        return "sunny", "21"
        """
    print(language_)
    owm = OWM(API_key='93cb27adec624ac85b40c7779e0b0fe3', language='nl')
    print(owm)
    if time.lower() in ['today', 'now']:
        temp = owm.weather_at_place(city).get_weather(
        ).get_temperature("celsius")["temp_min"]
        status = owm.weather_at_place(city).get_weather()._detailed_status

    else:
        if time.lower().__contains__("tom"):
            time = timeutils.tomorrow()
        else:
            try:
                hrs = int(time.lower().split('day')[0]) * 24
            except:
                print("error while reading date")

            time = datetime.now()+timedelta(hours=hrs)

        status = owm.three_hours_forecast(
            city).get_weather_at(time)._status  # status
        temp = owm.three_hours_forecast(city).get_weather_at(
            time).get_temperature(unit="celsius")["temp_min"]
    print(status)
    print(temp)

    return status, str(temp)
"""
