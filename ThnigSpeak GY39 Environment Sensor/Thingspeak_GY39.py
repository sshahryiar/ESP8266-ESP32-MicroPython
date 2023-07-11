import urequests
import ujson as json


class Thingspeak_GY39():
    HTTP_HEADERS = {'Content-Type': 'application/json'} 
    
    def __init__(self, _api_write_key, _api_read_key):
        self._api_read_key = _api_read_key
        self.api_write_key = _api_write_key
        
        
    def push_data(self, l_field, t_field, p_field, rh_field, alt_field):
        urequests.post('http://api.thingspeak.com/update?api_key=' + self.api_write_key
                       + '&field1=' + str(l_field)
                       + '&field2=' + str(t_field)
                       + '&field3=' + str(p_field)
                       + '&field4=' + str(rh_field)
                       + '&field5=' + str(alt_field))
