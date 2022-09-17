import urequests as requests
import ujson as json


class timeapi():
    def __init__(self, lat, lon):
        self.latitude = lat
        self.longitude = lon
        
        
    def coonect_url(self):
        url = "https://timeapi.io/api/Time/current/coordinate?latitude=" + str("%3.2f" %self.latitude) + "&longitude=" + str("%3.2f" %self.longitude)
        return url
    
    
    def fetch_data(self):
        return_data = []
        
        fetched_data = requests.get(self.coonect_url())
             
        return_data.append(fetched_data.json().get('year'))              # 0
        return_data.append(fetched_data.json().get('month'))             # 1
        return_data.append(fetched_data.json().get('day'))               # 2
        return_data.append(fetched_data.json().get('dayOfWeek'))         # 3
        return_data.append(fetched_data.json().get('hour'))              # 4
        return_data.append(fetched_data.json().get('minute'))            # 5
        return_data.append(fetched_data.json().get('seconds'))           # 6
        return_data.append(fetched_data.json().get('milliSeconds'))      # 7
        return_data.append(fetched_data.json().get('timeZone'))          # 8
        
        return return_data
        