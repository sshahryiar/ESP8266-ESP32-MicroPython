from micropython import const
from machine import Pin, I2C, RTC
from utime import sleep_ms
from SSD1306_I2C import OLED1306
from unix_time import unix
from unixtime import unixtime
from open_weather_map import open_weather_map
import Open_Weather_Map_Credentials
import network
import gc
import framebuf
import WiFi_Credentials


sync_hour = const(1)


image_0 = framebuf.FrameBuffer(bytearray(
    b'\x00\x00\x00\x00\x3e\x22\x3a\x80\xbe\x8a\x8e\x80\x2e\x2a\x3a\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x3e\x41\x80\x0c\x12\x0c\x80'
    b'\x41\x3e\x00\x00\x00\x00\x00\x00\x00\x00\x40\xc0\x40\x00\x40\xc0\x41\x0e\xc1\x80\xc0\x00\xc0\x40\x40\x00\x00\x00\x00\x00\x00\x87'
    b'\x40\x20\x24\x17\x14\xd0\x17\x10\x27\x20\x47\x85\x04\x00\x00\x00\x00\x00\x3e\xc1\x00\x00\x00\x00\x00\x0f\x08\x08\x08\x00\x00\xc1'
    b'\x3e\x00\x00\x00\x00\x00\x00\x00\x01\x02\x02\x04\x04\x04\x04\x04\x02\x02\x01\x00\x00\x00\x00\x00'),
    20, 48, framebuf.MONO_VLSB)


image_1 = framebuf.FrameBuffer(bytearray(
    b'\x00\x00\x00\x00\xfe\x01\x01\x01\xfe\x00\x00\xaa\xaa\xaa\x22\x22\x00\x00\x00\x00\x00\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\xaa'
    b'\xaa\xaa\x22\x22\x00\x00\x00\x00\x00\x00\x00\x00\xff\x00\xf0\x00\xff\x00\x00\xaa\xaa\xaa\x22\x22\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\xff\x00\xff\x00\xff\x00\x00\xaa\xaa\xaa\x22\x22\x00\x00\x00\x00\x00\xf0\xf8\xfc\xff\xfe\xff\xfe\xff\xfc\xf8\xf2\x02\x42\xa2\x42'
    b'\x00\xe0\x20\x20\x00\x01\x03\x07\x0f\x0f\x0f\x0f\x0f\x07\x03\x01\x00\x00\x00\x00\x00\x03\x02\x02'),
    20, 48, framebuf.MONO_VLSB)


image_2 = framebuf.FrameBuffer(bytearray(
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x80\x60\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xf8\x04\x02\x11\x80\x40\x20\x11'
    b'\x02\x04\xf8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x02\x04\x09\x08\x08\x08\x09\x04\x02\x01\x00\x00\x00\x00\x00\x00\x00\x00\xc8'
    b'\x04\x02\x04\x08\x04\xc2\x04\x08\x04\x02\x04\xc8\x00\x00\x00\x00\x00\x10\x20\x7f\x20\x10\x00\x10\x20\x7f\x20\x10\x00\x10\x20\x7f'
    b'\x20\x10\x00\x00\x00\x00\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x00\x00\x00'),
    20, 48, framebuf.MONO_VLSB)


image_3 = framebuf.FrameBuffer(bytearray(
    b'\x00\x00\x50\x50\x50\x50\x50\x56\x51\x49\x46\x40\x40\x46\x49\x21\x11\x0e\x00\x00\x00\x00\x01\x01\x01\x01\x01\x01\x01\x01\x01\x09'
    b'\x11\x12\x0c\x00\x00\x00\x00\x00\x18\x24\x22\x41\x41\x41\x41\x62\x24\x28\x1c\x22\x61\x41\x41\x62\x24\x28\x18\x00\x00\x00\x00\xc8'
    b'\xf8\xf8\xc8\x00\x00\x00\x00\x00\x00\xc8\xf8\xf8\xc8\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\x66\x66\x66\x66\xff\xff\xff\xff'
    b'\xff\xff\x00\x00\x00\x04\x07\x0f\x0f\x0f\x0f\x07\x04\x00\x00\x04\x07\x0f\x0f\x0f\x0f\x07\x04\x00'),
    20, 48, framebuf.MONO_VLSB)


image_4 = framebuf.FrameBuffer(bytearray(
    b'\x00\x00\x00\x00\x00\x00\x00\x04\x06\x7f\x06\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10\x20\x04\x88\xc0\xe0\xe0\xee\xe0\xe0'
    b'\xc0\x88\x04\x20\x10\x00\x00\x00\x08\x09\x09\x08\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x08\x09\x09\x08\x08\x00\x00\x00\x00'
    b'\x00\x00\x00\x10\x30\x7f\x30\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\xc0\xe0\xe0\xe0\xe0\xe0\xc0\x80\x00\x00'
    b'\x00\x00\x00\x00\x08\x08\x08\x08\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x08\x08\x08\x08\x08'),
    20, 48, framebuf.MONO_VLSB)


ip = 0
LED_state = True
connection_status = False
data_pull_flag = False
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
disp_counter = 0
unix_time_stamp = 0
weather_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


gc.collect()
LED = Pin(2, Pin.OUT)
i2c = I2C(0, sda = Pin(21), scl = Pin(22), freq = 250000)
oled = OLED1306(i2c)
wifi_station = network.WLAN(network.STA_IF)
rtcc = RTC()
rtcc.datetime((1970, 1, 1, 0, 0, 0, 0, 0))
ts = unixtime()
unx = unix(+6)
owm = open_weather_map(Open_Weather_Map_Credentials.country, Open_Weather_Map_Credentials.city, Open_Weather_Map_Credentials.api_key)


def connect_and_check_wifi_status():
    global ip, connection_status
    
    if(wifi_station.isconnected() == True):
        if(connection_status == False):
            print("Connected to WiFi Network with SSID: " + WiFi_Credentials.SSID + " and with IP address: " + wifi_station.ifconfig()[0] + "\r\n")
            ip = wifi_station.ifconfig()[0]
            connection_status = True
            
    else:
        if(wifi_station.active() == True):
            if(wifi_station.isconnected()):
                wifi_station.disconnect()            
            wifi_station.active(False)
            sleep_ms(100)
        print("Network Error!")
        wifi_station.active(True)
        LED.value(True)
        sleep_ms(100)
        wifi_station.connect(WiFi_Credentials.SSID, WiFi_Credentials.password)
        LED.value(False)
        sleep_ms(400)
        connection_status = False


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
        
        print(weather_data)

        past_second = second
    
    if(connection_status == False):
        oled.text("Open Weather Map", 0, 0, oled.WHITE)
        oled.text("Network Error!", 0, 14, oled.WHITE)
        oled.text("....", 0, 28, oled.WHITE)
        time_sync_status = False

    else:
        disp_counter = (second // 10)
        
        if(disp_counter == 0):
            up_year, up_month, up_date, up_hour, up_minute, up_second = unx.unix_to_date_time(int(weather_data[4])) 
            oled.fill(oled.BLACK)
            oled.text("Open Weather Map", 0, 0, oled.WHITE)
            oled.text(("WiFi: " + WiFi_Credentials.SSID), 0, 12, oled.WHITE)
            oled.text(("Now : " + str(weather_data[7])), 0, 24, oled.WHITE)            
            oled.text(("Time: " + str("%02u:" %up_hour) + str("%02u" %up_minute)), 0, 36, oled.WHITE)
            oled.text(("Date: " + str("%02u/" %up_date) + str("%02u/" %up_month) + str("%4u" %up_year)), 0, 48, oled.WHITE)
        
        elif(disp_counter == 1):
            oled.fill(oled.BLACK)
            oled.text("Location & Time.", 0, 0, oled.WHITE)
            oled.blit(image_0, 0, 19)            
            oled.text(("Lat: " + str("%2.2f" %weather_data[2])), 30, 14, oled.WHITE)
            oled.text(("Lon: " + str("%2.2f" %weather_data[3])), 30, 26, oled.WHITE)            
            oled.text((str("%02u:" %hour) + str("%02u:" %minute) + str("%02u" %second)), 30, 40, oled.WHITE)
            oled.text((str("%02u/" %date) + str("%02u/" %month) + str("%4u" %year)), 30, 52, oled.WHITE)
            
        elif(disp_counter == 2):
            oled.fill(oled.BLACK)
            oled.text("Temperature/'C", 12, 0, oled.WHITE)
            oled.blit(image_1, 0, 19)
            oled.text(("Now.: " + str("%2.1f" %weather_data[9])), 30, 14, oled.WHITE)
            oled.text(("Feel: " + str("%2.1f" %weather_data[10])), 30, 26, oled.WHITE) 
            oled.text(("Max.: " + str("%2.1f" %weather_data[12])), 30, 40, oled.WHITE)
            oled.text(("Min.: " + str("%2.1f" %weather_data[11])), 30, 54, oled.WHITE)            
        
        elif(disp_counter == 3):
            oled.fill(oled.BLACK)
            oled.text("R.H & Pressure.", 6, 0, oled.WHITE)
            oled.blit(image_2, 0, 19)
            oled.text("R.H/%", 30, 14, oled.WHITE)
            oled.text(str("%3u" %weather_data[13]), 30, 26, oled.WHITE) 
            oled.text("P./mbar", 30, 40, oled.WHITE)
            oled.text(str("%4u" %weather_data[14]), 30, 54, oled.WHITE)     
            
        elif(disp_counter == 4):
            oled.fill(oled.BLACK)
            oled.text("Wind & Others.", 10, 0, oled.WHITE)
            oled.blit(image_3, 0, 19)
            oled.text(("W/m/s: " + str("%2.1f" %weather_data[15])), 30, 14, oled.WHITE)
            oled.text(("dir/': " + str("%3u" %weather_data[16])), 30, 26, oled.WHITE) 
            oled.text(("Cld/%: " + str("%3u" %weather_data[19])), 30, 40, oled.WHITE)
            oled.text(("Vis/m: " + str("%5u" %weather_data[18])), 30, 54, oled.WHITE)       
            
        elif(disp_counter == 5):
           sr_year, sr_month, sr_date, sr_hour, sr_minute, sr_second = unx.unix_to_date_time(int(weather_data[5]))
           ss_year, ss_month, ss_date, ss_hour, ss_minute, ss_second = unx.unix_to_date_time(int(weather_data[6])) 
           oled.fill(oled.BLACK)
           oled.text("Sunrise & Sunset.", 0, 0, oled.WHITE)
           oled.blit(image_4, 0, 19)
           oled.text("Sunrise", 30, 14, oled.WHITE)
           oled.text((str("%02u:" %sr_hour) + str("%02u:" %sr_minute) + str("%02u" %sr_second)), 30, 26, oled.WHITE)
           oled.text("Sunset", 30, 40, oled.WHITE)
           oled.text((str("%02u:" %ss_hour) + str("%02u:" %ss_minute) + str("%02u" %ss_second)), 30, 54, oled.WHITE)
        
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
            weather_data = owm.fetch_data()
            
            year, month, date, hour, minute, second = unx.unix_to_date_time(unix_time_stamp) 
            rtcc.datetime((year, month, date, day, hour, minute, second, tz))
            data_pull_flag = False
    
    oled.show()
   