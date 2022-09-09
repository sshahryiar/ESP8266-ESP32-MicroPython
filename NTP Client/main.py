from micropython import const
from machine import Pin, I2C, WDT
from utime import sleep_ms
from SSD1306_I2C import OLED1306
import WiFi_Credentials
import time
import network
import ntptime


time_zone = const(+6)
sync_hour = const(3)

ip = 0
LED_state = True
second_previous = 0
sync_success = False
connection_successful = False


LED = Pin(2, Pin.OUT)
wdt = WDT()
i2c = I2C(sda = Pin(4), scl = Pin(5), freq = 250000)
oled = OLED1306(i2c)
wifi_sta = network.WLAN(network.STA_IF)


def connect_and_check_wifi_status():
    global ip, connection_successful, LED_state
    
    if(wifi_sta.isconnected()):
        if(connection_successful == False):
            print("Connected to WiFi Network with SSID: " + WiFi_Credentials.SSID + " and with IP address: " + wifi_sta.ifconfig()[0] + "\r\n")
            ip = wifi_sta.ifconfig()[0]
            connection_successful = True
            
    else:
        wifi_sta.active(True)
        wifi_sta.connect(WiFi_Credentials.SSID, WiFi_Credentials.password)
        sleep_ms(400)
        print("Network Unavailable!" + "\r\n")
        LED_state ^= 0x01
        LED.value(LED_state)
        sleep_ms(90)
        connection_successful = False
        
    wdt.feed()
    
    return connection_successful

    
def sync_ntp():
    try:
        ntptime.settime()
        print("\r\n" + "RTC Synchronized." + "\r\n")
        oled.text("Sync", 90, 46, oled.WHITE)
        return True
    except OSError:
        print("\r\n" + 'NTP server: connection timeout...' + "\r\n")
        oled.text("Error", 80, 46, oled.WHITE)
        return False


while(True):
    try:     
        oled.fill(oled.BLACK)
        
        network_status = connect_and_check_wifi_status()
            
        UTC_OFFSET = (time_zone * 3600)
        rtc_value = time.localtime(time.time() + UTC_OFFSET)
        
        year = rtc_value[0]
        month = rtc_value[1]
        date = rtc_value[2]
        hour = rtc_value[3]
        minute = rtc_value[4]
        second = rtc_value[5]
        
        if(network_status == True):
            if(sync_success == False):
                if(second == 0):
                    sync_success = sync_ntp()
                    
            else:
                if(((hour % sync_hour) == 0) and (minute == 0) and (second == 0)):
                    sync_success = sync_ntp()
        
        wdt.feed()
        
        if(second != second_previous):
                        
            oled.text("ESP RTC NTP Time", 0, 0, oled.WHITE)
        
            if(network_status == False):
                oled.text("Network Error!", 0, 14, oled.WHITE)
                oled.text("000.000.000.000", 0, 28, oled.WHITE)
                
            else:
                oled.text(("WiFi: " + WiFi_Credentials.SSID), 0, 14, oled.WHITE)
                oled.text(ip, 0, 28, oled.WHITE)
            
            oled.text(("Time: " + str("%02u:" %hour) + str("%02u:" %minute) + str("%02u" %second)), 0, 42, oled.WHITE)
            oled.text(("Date: " + str("%02u/" %date) + str("%02u/" %month) + str("%4u" %year)), 0, 56, oled.WHITE)
            
            print("Time: " + str("%02u:" %hour) + str("%02u:" %minute) + str("%02u" %second)
                  + "   Date: " + str("%02u/" %date) + str("%02u/" %month) + str("%4u" %year))
            
            LED_state ^= 0x01
            oled.show()
            LED.value(LED_state)
        
        second_previous = second
        
    except OSError:
        print('Error! Rebooting....' + "\r\n")
        oled.text("Error", 80, 46, oled.WHITE)
        oled.show()
