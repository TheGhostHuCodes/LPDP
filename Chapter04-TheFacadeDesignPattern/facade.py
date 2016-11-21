#!/usr/bin/env python3
from cache import Cache
from weatherprovider import WeatherProvider
from parser import Parser
from weather import Weather
from converter import Converter


class Facade():
    def get_forcast(self, city, country):
        cache = Cache('weather_cache')

        cache_result = cache.load()

        if cache_result:
            return cache_result
        else:
            weather_provider = WeatherProvider()
            weather_data = weather_provider.get_weather_data(city, country)

            parser = Parser()
            parsed_data = parser.parse_weather_data(weather_data)

            weather = Weather(parsed_data)
            temperature_celcius = Converter.from_kelvin_to_celcius(
                weather.temperature)

            cache.save(temperature_celcius)
            return temperature_celcius


if __name__ == '__main__':
    facade = Facade()
    print(facade.get_forcast('Fremont', 'US'))
