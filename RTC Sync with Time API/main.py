from machine import Pin, I2C, WDT, RTC
from SSD1306_I2C import OLED1306
import WiFi_Credentials
from time import sleep_ms
from timeapi import timeapi
import network
import esp
import socket
import gc


sync_hour = const(3)


ip = 0
time_zone = "...."
LED_state = True
time_fetch_flag = False
time_sync_status = False
connection_status = False


gc.collect()
LED = Pin(2, Pin.OUT)
wdt = WDT(timeout = 9000)
i2c = I2C(0, sda = Pin(21), scl = Pin(22), freq = 400000)
oled = OLED1306(i2c)
wifi_station = network.WLAN(network.STA_IF)
tapi = timeapi(23.81, 90.41)
rtcc = RTC()

rtcc.datetime((2000, 1, 1, 1, 0, 0, 0, 0))

#web_weather = open_weather_map(Open_Weather_Map_Credentials.country, Open_Weather_Map_Credentials.city, Open_Weather_Map_Credentials.api)


def connect_and_check_wifi_status():
    global ip, connection_status, LED_state
    
    if(wifi_station.isconnected()):
        if(connection_status == False):
            print("Connected to WiFi Network with SSID: " + WiFi_Credentials.SSID + " and with IP address: " + wifi_station.ifconfig()[0] + "\r\n")
            ip = wifi_station.ifconfig()[0]
            connection_status = True
            
    else:
        wifi_station.active(True)
        wifi_station.disconnect()
        sleep_ms(300)
        wifi_station.connect(WiFi_Credentials.SSID, WiFi_Credentials.password)
        wdt.feed()
        sleep_ms(600)
        print("Network Unavailable!" + "\r\n")
        LED_state ^= 0x01
        LED.value(LED_state)
        wdt.feed()
        sleep_ms(90)
        connection_status = False
        
        
def day_counter(string):
    if(string == "Tuesday"):
        return 1
    elif(string == "Wednesday"):
        return 2
    elif(string == "Thursday"):
        return 3
    elif(string == "Friday"):
        return 4
    elif(string == "Saturday"):
        return 5
    elif(string == "Sunday"):
        return 6
    else:
        return 0
        
        
while(True):
    oled.fill(oled.BLACK)
    
    connect_and_check_wifi_status()
    year, month, date, day, hour, minute, second, tz = rtcc.datetime()
    
    LED_state ^= 0x01
    LED.value(LED_state)
        
    oled.text("ESP RTC Time API", 0, 0, oled.WHITE)
    
    if(connection_status == False):
        oled.text("Network Error!", 0, 14, oled.WHITE)
        oled.text("....", 0, 28, oled.WHITE)
        time_sync_status = False
        oled.show()
        wdt.feed()
    
    else:
        if(time_sync_status == False):            
            if(second == 30):
                time_fetch_flag = True
                time_sync_status = True
        
        if(time_sync_status == True):
            if(((hour % sync_hour) == 0) and (minute == 0) and (second == 0)):
                time_fetch_flag = True
                
        if(time_fetch_flag == True):
            oled.text("*", 120, 46, oled.WHITE)
            value = tapi.fetch_data()
            year = value[0]
            month = value[1]
            date = value[2]
            day = day_counter(value[3])
            hour = value[4]
            minute = value[5]
            second = value[6]
            time_zone = value[8]
            wdt.feed()
            rtcc.datetime((year, month, date, day, hour, minute, second, tz))
            time_fetch_flag = False
        
        oled.text(("WiFi: " + WiFi_Credentials.SSID), 0, 14, oled.WHITE)
        oled.text(str(time_zone), 0, 28, oled.WHITE)
        
        wdt.feed()
        sleep_ms(990)

        
    oled.text(("Time: " + str("%02u:" %hour) + str("%02u:" %minute) + str("%02u" %second)), 0, 42, oled.WHITE)
    oled.text(("Date: " + str("%02u/" %date) + str("%02u/" %month) + str("%4u" %year)), 0, 56, oled.WHITE)
    oled.show()
        
    print("Time: " + str("%02u:" %hour) + str("%02u:" %minute) + str("%02u" %second)
            + "   Date: " + str("%02u/" %date) + str("%02u/" %month) + str("%4u" %year))
