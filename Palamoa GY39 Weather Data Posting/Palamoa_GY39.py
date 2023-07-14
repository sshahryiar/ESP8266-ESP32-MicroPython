from urequests import post, request
import Palamoa_Credential
import gc


class Palamoa_GY39():
        
    def post_data(self, l, t, p, rh):
        gc.collect()
        main_dict = {}
        P = {}
        T = {}
        RH = {}
        L = {}
        
        link = "https://palamoa.de/json/" + Palamoa_Credential.key
        
        request_headers = {'Content-Type': 'application/json'}
        
        P["color"] = "#32D08E"
        P["label"] = "Pressure"
        P["value"] = str("%3.1f" %p)
        
        RH["color"] = "#5F8AFF"
        RH["label"] = "Humidity"
        RH["value"] = str("%3.1f" %rh)
        
        T["color"] = "#E86161"
        T["label"] = "Temperature"
        T["value"] = str("%3.1f" %t)
        
        L["color"] = "#6300FF"
        L["label"] = "Light"
        L["value"] = str("%3.1f" %l)
        
        main_dict["device_name"] = "microarena"
        main_dict["P"] = P
        main_dict["T"] = T
        main_dict["L"] = L
        main_dict["RH"] = RH
                        
        try:
            req = post(url = link, json = main_dict, headers = request_headers)
            print("\r\n" + req.text + "\r\n")
            req.close()
            
        except:
            print("Failed to post last data!")   
                