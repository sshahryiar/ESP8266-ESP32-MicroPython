import urequests as requests
import ujson as json


class unix_timestamp():
    def connect_url(self):
        url = 'http://api.aladhan.com/v1/currentTimestamp?zone=Europe/London'
        return url
    
    
    def fetch_data(self):
        return_data = 0
        requested_data = requests.get(self.connect_url())
        return_data = requested_data.json().get('data')
        return int(return_data)