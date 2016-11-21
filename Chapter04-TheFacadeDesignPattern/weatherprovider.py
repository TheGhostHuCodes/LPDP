import urllib.parse
import urllib.request
import configparser


class WeatherProvider():
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.api_key = config['DEFAULT']['APPID']
        self.api_url = 'http://api.openweathermap.org/data/2.5/forecast/daily?q={},{}&APPID={}'

    def get_weather_data(self, city, country):
        city = urllib.parse.quote(city)
        url = self.api_url.format(city, country, self.api_key)
        return urllib.request.urlopen(url).read().decode('utf-8')
