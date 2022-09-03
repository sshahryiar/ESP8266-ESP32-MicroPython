from micropython import const
from machine import Pin, RTC, I2C, WDT
from utime import sleep_ms
from SSD1306_I2C import OLED1306
import WiFi_Credentials
import network
import ntptime


time_zone = const(+6)
sync_hour = const(6)

sync_success = False
ip = 0

LED = Pin(2, Pin.OUT)
rtc = RTC()
wdt = WDT(timeout = 4000)
i2c = I2C(0, sda = Pin(21), scl = Pin(22), freq = 250000)
oled = OLED1306(i2c)
wifi_sta = network.WLAN(network.STA_IF)


def connect_wifi():
    global ip
    if(wifi_sta.isconnected() == False):
        wifi_sta.active(True)
        wifi_sta.connect(WiFi_Credentials.SSID, WiFi_Credentials.password)
        while not wifi_sta.isconnected():
            print("Connecting WiFi...." + "\r\n")
            LED.on()
            sleep_ms(100)
            LED.off()
            sleep_ms(400)
            wdt.feed()
        print("IP address:" + wifi_sta.ifconfig()[0] + "\r\n")
        ip = wifi_sta.ifconfig()[0]
    
    
def sync_ntp():
    try:
        ntptime.settime()
        print("RTC Synchronized." + "\r\n")
        oled.text("Sync", 90, 46, oled.WHITE)
        return True
    except OSError:
        print('NTP server: connection timeout...' + "\r\n")
        oled.text("Error", 80, 46, oled.WHITE)
        return False


while(True):
    try:
        connect_wifi()
        
        oled.fill(oled.BLACK)
        
        rtc_value = rtc.datetime()
        
        year = rtc_value[0]
        month = rtc_value[1]
        date = rtc_value[2]
        hour = ((rtc_value[4] + time_zone) % 24)
        minute = rtc_value[5]
        second = rtc_value[6]

        
        oled.text("ESP32 NTP Client", 0, 0, oled.WHITE)
        oled.text(("WiFi: " + WiFi_Credentials.SSID), 0, 14, oled.WHITE)
        oled.text(ip, 0, 28, oled.WHITE)
        oled.text((str("%02u:" %hour) + str("%02u:" %minute) + str("%02u" %second)), 0, 42, oled.WHITE)
        oled.text((str("%02u/" %date) + str("%02u/" %month) + str("%4u" %year)), 0, 56, oled.WHITE)
        
        if(sync_success == False):
            if(second == 0):
                sync_success = sync_ntp()
                
        else:
            if(((hour % sync_hour) == 0) and (minute == 0) and (second == 0)):
                sync_success = sync_ntp()
        
        oled.show()
        
        print("Time: " + str("%02u:" %hour) + str("%02u:" %minute) + str("%02u" %second)
              + "   Date: " + str("%02u/" %date) + str("%02u/" %month) + str("%4u" %year) + "\r\n")
       
        wdt.feed()
        LED.on()
        sleep_ms(450)
        LED.off()
        sleep_ms(450)
        
    except OSError:
        print('Error! Rebooting....' + "\r\n")
        oled.text("Error", 80, 46, oled.WHITE)