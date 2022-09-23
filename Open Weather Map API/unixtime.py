import urequests
import ujson


class unixtime():
    def get_time(self):
        url = "https://showcase.api.linx.twenty57.net/UnixTime/tounixtimestamp?datetime=now"
        url_data = urequests.get(url)
        json_data = ujson.loads(url_data.text)
        return int(json_data['UnixTimeStamp']) 