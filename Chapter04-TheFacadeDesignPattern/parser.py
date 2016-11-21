from datetime import datetime
import json


class Parser():
    def parse_weather_data(self, weather_data):
        parsed = json.loads(weather_data)
        start_date = None
        result = []

        for data in parsed['list']:
            date = datetime.fromtimestamp(data['dt'])
            start_date = start_date or date
            if start_date.day != date.day:
                return result
            result.append(data['temp']['day'])
