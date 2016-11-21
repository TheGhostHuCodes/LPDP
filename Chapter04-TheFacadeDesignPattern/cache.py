from datetime import datetime, timedelta
import pickle


class Cache():
    def __init__(self, filename):
        self.filename = filename

    def save(self, obj):
        with open(self.filename, 'wb') as file_:
            dct = {
                'obj': obj,
                'expired': datetime.utcnow() + timedelta(hours=3)
            }
            pickle.dump(dct, file_)

    def load(self):
        try:
            with open(self.filename, 'rb') as file_:
                result = pickle.load(file_)
                if result['expired'] > datetime.utcnow():
                    return result['obj']
        except IOError:
            pass
