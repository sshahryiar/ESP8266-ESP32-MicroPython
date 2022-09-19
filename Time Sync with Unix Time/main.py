from micropython import const
from machine import Pin, I2C, RTC
from utime import sleep_ms
from SSD1306_I2C import OLED1306
from unix_time import unix
from unix_timestamp import unix_timestamp
import network
import gc
import esp
import socket
import WiFi_Credentials


sync_hour = const(1)


ip = 0
LED_state = True
connection_status = False
time_fetch_flag = False
time_sync_status = False
unix_time_data = 0
year = 1970
month = 1
date = 1
hour = 0
minute = 0
second = 0
past_second = 0
day = 0
tz = 0
unix_time_stamp = 0


gc.collect()
LED = Pin(2, Pin.OUT)
i2c = I2C(sda = Pin(4), scl = Pin(5), freq = 250000)
oled = OLED1306(i2c)
wifi_sta = network.WLAN(network.STA_IF)
rtcc = RTC()
rtcc.datetime((1970, 1, 1, 0, 0, 0, 0, 0))
ts = unix_timestamp()
unx = unix(+6)


def connect_and_check_wifi_status():
    global ip, connection_status, LED_state

    sleep_ms(900)
    
    if(wifi_sta.isconnected()):
        if(connection_status == False):
            print("Connected to WiFi Network with SSID: " + WiFi_Credentials.SSID + " and with IP address: " + wifi_sta.ifconfig()[0] + "\r\n")
            ip = wifi_sta.ifconfig()[0]
            connection_status = True
            
    else:
        wifi_sta.active(True)
        wifi_sta.disconnect()
        sleep_ms(30)
        wifi_sta.connect(WiFi_Credentials.SSID, WiFi_Credentials.password)
        sleep_ms(60)
        print("Network Unavailable!" + "\r\n")
        LED_state ^= 0x01
        LED.value(LED_state)
        sleep_ms(9)
        connection_status = False


oled.fill(oled.BLACK)
oled.show()


while(True):
    connect_and_check_wifi_status()
    year, month, date, day, hour, minute, second, tz = rtcc.datetime()
    
    oled.fill(oled.BLACK)
    oled.text("Unix Time Sync ", 8, 0, oled.WHITE)
    
    if(second != past_second):
        LED_state ^= 0x01
        LED.value(LED_state)
        oled.text(("Time: " + str("%02u:" %hour) + str("%02u:" %minute) + str("%02u" %second)), 0, 42, oled.WHITE)
        oled.text(("Date: " + str("%02u/" %date) + str("%02u/" %month) + str("%4u" %year)), 0, 56, oled.WHITE)
           
        print("Time: " + str("%02u:" %hour) + str("%02u:" %minute) + str("%02u" %second)
                + "   Date: " + str("%02u/" %date) + str("%02u/" %month) + str("%4u" %year))
        
        past_second = second
    
    if(connection_status == False):
        oled.text("Network Error!", 0, 14, oled.WHITE)
        oled.text("....", 0, 28, oled.WHITE)
        time_sync_status = False

    else:
        if(time_sync_status == False):            
            if(second == 30):
                time_fetch_flag = True
                time_sync_status = True
        
        else:
            if(((hour % sync_hour) == 0) and (minute == 0) and (second == 0)):
                time_fetch_flag = True
                
        if(time_fetch_flag == True):
            oled.text("*", 120, 46, oled.WHITE)
            unix_time_stamp = ts.fetch_data()
            year, month, date, hour, minute, second = unx.unix_to_date_time(unix_time_stamp) 
            rtcc.datetime((year, month, date, day, hour, minute, second, tz))
            time_fetch_flag = False
        
        oled.text(("WiFi: " + WiFi_Credentials.SSID), 0, 14, oled.WHITE)
        oled.text(("UNIX: " + str("%u" %unix_time_stamp)), 0, 28, oled.WHITE)
    
    oled.show()

