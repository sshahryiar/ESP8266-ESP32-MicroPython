import urequests as requests
import ujson as json


class iss_location():
    
    def fetch_data(self):
        try:
            fetched_data = requests.get("http://api.open-notify.org/iss-now.json")
        except:
            print("Error!")
        
        utc = (fetched_data.json().get('timestamp'))                      
        lat = (fetched_data.json().get('iss_position').get('latitude'))   
        lon = (fetched_data.json().get('iss_position').get('longitude'))  
        
        return utc, lat, lon
