from micropython import const
from machine import Pin, I2C, RTC
from utime import sleep_ms
from SSD1306_I2C import OLED1306
from unix_time import unix
from unixtime import unixtime
from Thingspeak_DHT import Thingspeak_DHT
import Thingspeak_Credentials
import dht
import network
import WiFi_Credentials
import gc


sync_hour = const(1)
update_time = const(15)


ip = 0
LED_state = True
connection_status = False
time_sync_status = False
time_sync_success = False
data_pull_flag = False

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
t = 0
rh = 0
update_counter = 0


gc.collect()
LED = Pin(2, Pin.OUT)
i2c = I2C(0, sda = Pin(21), scl = Pin(22), freq = 250000)
oled = OLED1306(i2c)
wifi_station = network.WLAN(network.STA_IF)
dht_sensor = dht.DHT11(Pin(4))
rtcc = RTC()
rtcc.datetime((1970, 1, 1, 0, 0, 0, 0, 0))
ts = unixtime()
unx = unix(+6)
thingspeak = Thingspeak_DHT(Thingspeak_Credentials.API_write_key, Thingspeak_Credentials.API_read_key)


def connect_and_check_wifi_status():
    global ip, connection_status
    
    if(wifi_station.isconnected() == True):
        if(connection_status == False):
            print("Connected to WiFi Network with SSID: " + WiFi_Credentials.SSID + " and with IP address: " + wifi_station.ifconfig()[0] + "\r\n")
            ip = wifi_station.ifconfig()[0]
            oled.fill(oled.BLACK)
            oled.text("ESP Thingspeak", 12, 0, oled.WHITE)
            oled.text("Network Details", 8, 16, oled.WHITE)
            oled.text(("WiFi: " + WiFi_Credentials.SSID), 0, 36, oled.WHITE)
            oled.text(("IP: " + ip), 0, 48, oled.WHITE)
            oled.show()
            sleep_ms(2000)
            connection_status = True
            
    else:
        print("Network Error!")
        wifi_station.active(True)
        LED.value(True)
        sleep_ms(100)
        wifi_station.connect(WiFi_Credentials.SSID, WiFi_Credentials.password)
        LED.value(False)
        sleep_ms(400)
        connection_status = False


connect_and_check_wifi_status()
oled.fill(oled.BLACK)
oled.show()


while(True):
    year, month, date, day, hour, minute, second, tz = rtcc.datetime()
    
    if(second != past_second):
        connect_and_check_wifi_status()
        oled.fill(oled.BLACK)
        LED_state ^= 0x01
        LED.value(LED_state)
        
        print("Time: " + str("%02u:" %hour) + str("%02u:" %minute) + str("%02u" %second)
                + "   Date: " + str("%02u/" %date) + str("%02u/" %month) + str("%4u" %year))
        
        print("T/'C: " + str("%2u" %t) + "  RH/%: " + str("%2u" %rh) + "\r\n")
        update_counter += 1
        past_second = second
        
        try:
            dht_sensor.measure()
            t = dht_sensor.temperature()
            rh = dht_sensor.humidity()
        except:
            continue
    
    if(connection_status == False):
        oled.text("ESP Thingspeak", 12, 0, oled.WHITE)
        oled.text("Network Error!", 0, 14, oled.WHITE)
        oled.text("....", 0, 28, oled.WHITE)
        time_sync_status = False
        time_sync_success = False

    else:
        oled.text("ESP Thingspeak", 12, 0, oled.WHITE)
        
        oled.text(("T/'C:         " + str("%02u" %t)), 0, 14, oled.WHITE)
        oled.text(("RH/%:         " + str("%02u" %rh)), 0, 28, oled.WHITE)
        
        oled.text(("Time: " + str("%02u:" %hour) + str("%02u:" %minute) + str("%02u" %second)), 0, 42, oled.WHITE)
        oled.text(("Date: " + str("%02u/" %date) + str("%02u/" %month) + str("%4u" %year)), 0, 56, oled.WHITE)
        
        
        if(time_sync_success == True):
            if(update_counter >= update_time):
                thingspeak.push_data(t, rh)
                update_counter = 0
        
        if(time_sync_status == False):            
            if(second == 0):
                data_pull_flag = True
                time_sync_status = True
        
        else:
            if(((hour % sync_hour) == 0) and (minute == 0) and (second == 0)):
                data_pull_flag = True
                
        if(data_pull_flag == True):
            oled.text("*", 120, 46, oled.WHITE)
            unix_time_stamp = ts.get_time()            
            year, month, date, hour, minute, second = unx.unix_to_date_time(unix_time_stamp) 
            rtcc.datetime((year, month, date, day, hour, minute, second, tz))
            time_sync_success = True
            data_pull_flag = False
    
    oled.show()
   