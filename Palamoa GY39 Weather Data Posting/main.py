from machine import UART
from GY39 import GY39
from ST7789 import IPS15
from Palamoa_GY39 import Palamoa_GY39
from utime import sleep_ms
import WiFi_Credentials
import network
import gc
import os


gc.collect()

l = 0
t = 0
p = 0
rh = 0
ip = 0
alt = 0
connection_status = False
network_check_counter = -6


uart = UART(2, baudrate = 9600, bits = 8, parity = None, stop = 1, tx = 17, rx = 16)

gy = GY39(uart)

wifi_station = network.WLAN(network.STA_IF)

display = IPS15()
display.fill(display.BLACK)
display.print_str(9, 10, 2, display.WHITE, display.BLACK, "ESP32 GY39 Palamoa")

palamoa = Palamoa_GY39()


def connect_and_check_wifi_status():
    global ip, connection_status, network_check_counter
    
    if(wifi_station.isconnected()):
        if(connection_status == False):
            print("Connected to WiFi Network with SSID: " + WiFi_Credentials.SSID + " and with IP address: " + wifi_station.ifconfig()[0] + "\r\n")
            display.print_str(6, 220, 2, display.WHITE, display.BLACK, "SSID: " + str(WiFi_Credentials.SSID))
            ip = wifi_station.ifconfig()[0]
            network_check_counter = -10
            connection_status = True
            
    else:
        if(wifi_station.isconnected() == True):
            if(wifi_station.active() == True):
                wifi_station.active(False)
                sleep_ms(1000)
            
            wifi_station.disconnect()    
            sleep_ms(1000)
           
        print("Network Error!\r\n")
        display.print_str(6, 220, 2, display.WHITE, display.BLACK, "SSID: None        ")
        try:
            wifi_station.active(True)
        except:
            print("Unexpected Error!\r\n")
        sleep_ms(300)
        try:
            wifi_station.connect(WiFi_Credentials.SSID, WiFi_Credentials.password)
        except:
            print("Unable to connect!\r\n")
            network_check_counter = -10
        sleep_ms(300)
        connection_status = False


while(True):
    l, t, p, rh, alt = gy.get_data()
    
    string_1 = "Lm/Lux: " + str("%3.1f" %l)
    string_2 = "Tmp/'C: " + str("%3.1f" %t)
    string_3 = "P/mbar: " + str("%3.1f" %p)
    string_4 = "R.H./%: " + str("%3.1f" %rh)
    string_5 = "Alt./m: " + str("%3.1f" %alt)
    
    display.print_str(6, 40, 2, display.WHITE, display.BLACK, string_1)
    display.print_str(6, 70, 2, display.WHITE, display.BLACK, string_2)
    display.print_str(6, 100, 2, display.WHITE, display.BLACK, string_3)
    display.print_str(6, 130, 2, display.WHITE, display.BLACK, string_4)
    display.print_str(6, 160, 2, display.WHITE, display.BLACK, string_5)
    display.print_str(6, 190, 2, display.WHITE, display.BLACK, "Last Update/s: " + str(5 * network_check_counter) + " ")
   
    print(string_1)
    print(string_2)
    print(string_3)
    print(string_4)
    print(string_5)
    print("\r")
    
    network_check_counter -= 1
    if(network_check_counter < 0):
        connect_and_check_wifi_status()
        if(wifi_station.isconnected() == True):
            palamoa.post_data(l, t, p, rh)
        
        gc.collect()
            
        network_check_counter = 6
    