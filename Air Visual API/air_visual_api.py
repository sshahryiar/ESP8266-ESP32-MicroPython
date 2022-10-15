import urequests as requests
import ujson as json


class air_visual():
    def __init__(self, _lat, _lon, _key):
        self.lat = _lat
        self.lon = _lon
        self.api_key = _key


    def connect_url(self):
        url = "https://api.airvisual.com/v2/nearest_city?lat=" + self.lat + "&lon=" + self.lon + "&key=" + self.api_key
        return url


    def fetch_data(self):
        return_data = []
        
        fetched_data = requests.get(self.connect_url())

        return_data.append(fetched_data.json().get('status'))
        return_data.append(fetched_data.json().get('data').get('city'))
        return_data.append(fetched_data.json().get('data').get('state'))
        return_data.append(fetched_data.json().get('data').get('country'))

        return_data.append(fetched_data.json().get('data').get('location').get('coordinates'))

        return_data.append(fetched_data.json().get('data').get('current').get('pollution').get('ts'))
        return_data.append(fetched_data.json().get('data').get('current').get('pollution').get('aqius'))
        return_data.append(fetched_data.json().get('data').get('current').get('pollution').get('mainus'))
        return_data.append(fetched_data.json().get('data').get('current').get('pollution').get('aqicn'))
        return_data.append(fetched_data.json().get('data').get('current').get('pollution').get('maincn'))

        return_data.append(fetched_data.json().get('data').get('current').get('weather').get('ts'))
        return_data.append(fetched_data.json().get('data').get('current').get('weather').get('tp'))
        return_data.append(fetched_data.json().get('data').get('current').get('weather').get('pr'))
        return_data.append(fetched_data.json().get('data').get('current').get('weather').get('hu'))
        return_data.append(fetched_data.json().get('data').get('current').get('weather').get('ws'))
        return_data.append(fetched_data.json().get('data').get('current').get('weather').get('wd'))
        return_data.append(fetched_data.json().get('data').get('current').get('weather').get('ic'))

        return return_data
