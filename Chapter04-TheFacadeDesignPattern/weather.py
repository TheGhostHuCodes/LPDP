class Weather():
    def __init__(self, data):
        result = 0

        for r in data:
            result += r

        self.temperature = result / len(data)
