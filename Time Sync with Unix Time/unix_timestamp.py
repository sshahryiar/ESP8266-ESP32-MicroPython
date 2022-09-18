import urequests as requests
import ujson as json


class unix_timestamp():
    def __init__(self, _continent, _city):
        self.continent = _continent
        self.city = _city
    
    
    def connect_url(self):
        url = 'http://api.aladhan.com/v1/currentTimestamp?zone=' + self.continent + "/" + self.city
        return url
    
    
    def fetch_data(self):
        return_data = 0
        requested_data = requests.get(self.connect_url())
        return_data = requested_data.json().get('data')
        return int(return_data)

        
        