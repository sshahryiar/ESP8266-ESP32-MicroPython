from micropython import const
from machine import Pin, RTC
from utime import sleep_ms
from unix_time import unix
from unix_timestamp import unix_timestamp
from air_visual_api import air_visual
from ST7735 import TFT
import air_visual_credential
import WiFi_Credentials
import network
import random
import math
import gc
import os


scale_factor_1 = const(42)
scale_factor_2 = const(6)
sync_hour = const(1)
net_check_interval = const(10)
screen_change_interval = const(12)

conv_factor = 0.0174532925
pi_by_2 = 1.570796327

ip = 0
LED_state = True
connection_status = False
data_pull_flag = False
city_flag = False
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
counter = 0
unix_time_stamp = 0
screen_counter = 0
city_counter = 0
air_visual_data = [0 for _ in range(0, 19)]

lat = ["23.88", "39.90", "-34.60", "-33.92", "41.00", "34.05", "19.43", "19.07", "1.35", "48.85",
       "35.67", "52.52", "30.04", "23.32", "51.51", "55.75", "40.71", "-23.56", "-33.83", "43.65"]

lon = ["90.39", "116.40", "-58.38", "18.42", "28.98", "-118.24", "-99.13", "72.88", "103.82", "2.35",
       "139.65", "13.40", "31.23", "114.17", "-0.12", "37.62" "-74.00", "-46.64", "151.21", "-79.38"]

gc.collect()
LED = Pin(2, Pin.OUT)
tft = TFT()
wifi_station = network.WLAN(network.STA_IF)
rtcc = RTC()
rtcc.datetime((1970, 1, 1, 0, 0, 0, 0, 0))
ts = unix_timestamp()
unx = unix(+6)


def map_value(v, x_min, x_max, y_min, y_max):
    return (y_min + (((y_max - y_min)/(x_max - x_min)) * (v - x_min)))


def contrain(value, min_value, max_value):
    if(value > max_value):
        return max_value
    
    elif(value < min_value):
        return min_value
    
    else:
        return value


def circle(xc, yc, r, f, c):
    a = 0
    b = r
    p = (1 - b)

    while(a <= b):
       if(f == True):
           tft.line((xc - a), (yc + b), (xc + a), (yc + b), c)
           tft.line((xc - a), (yc - b), (xc + a), (yc - b), c)
           tft.line((xc - b), (yc + a), (xc + b), (yc + a), c)
           tft.line((xc - b), (yc - a), (xc + b), (yc - a), c)
           
       else:
           tft.pixel((xc + a), (yc + b), c)
           tft.pixel((xc + b), (yc + a), c)
           tft.pixel((xc - a), (yc + b), c)
           tft.pixel((xc - b), (yc + a), c)
           tft.pixel((xc + b), (yc - a), c)
           tft.pixel((xc + a), (yc - b), c)
           tft.pixel((xc - a), (yc - b), c)
           tft.pixel((xc - b), (yc - a), c)
        
       if(p < 0):
           p += (3 + (2 * a))
           a += 1
        
       else:
           p += (5 + (2 * (a  - b)))
           a += 1
           b -= 1



def sunny():
    circle(80, 40, 20, True, tft.YELLOW)
    
    for i in range(0, 360, 30):
        tft.line(80, 40, (80 + int(35 * math.sin((i * 2) * conv_factor))), int(40 - (35 * math.cos((i * 2) * conv_factor))), tft.YELLOW)
        tft.line(80, 40, (80 + int(30 * math.sin(i * conv_factor))), int(40 - (30 * math.cos(i * conv_factor))), tft.YELLOW)
        
        
def cloudy(den, col1, col2, col3):
    circle(80, 40, 10, True, tft.colour_generator(col1, col2, col3))
    circle(90, 35, 12, True, tft.colour_generator(col1, col2, col3))
    circle(95, 42, 11, True, tft.colour_generator(col1, col2, col3))
    
    circle(50, 40, 8, True, tft.colour_generator(col1, col2, col3))
    circle(60, 35, 10, True, tft.colour_generator(col1, col2, col3))
    circle(70, 42, 15, True, tft.colour_generator(col1, col2, col3))
    
    if(den == True):    
        col1 += 30
        col2 = col1
        col3 = col2
        
        circle(65, 20, 6, True, tft.colour_generator(col1, col2, col3))
        circle(75, 15, 9, True, tft.colour_generator(col1, col2, col3))
        circle(70, 12, 11, True, tft.colour_generator(col1, col2, col3))
    
    
def night():
    for i in range(0, 20):
        circle(random.randrange(40, 100), random.randrange(20, 60), random.randrange(1, 3), False, tft.CYAN)
        

def rain():
    for i in range(0, 10):
        x_pos = random.randrange(70, 90)
        y_pos = random.randrange(60, 70)
        tft.line(x_pos, y_pos, (x_pos - 5), (y_pos - 5), tft.CYAN)
        

def snow():
    for i in range(0, 10):
        circle(random.randrange(60, 80), random.randrange(60, 70), random.randrange(1, 2), True, tft.CYAN)
        
        
def lightning():
    x_pos = random.randrange(60, 80)
    y_pos = random.randrange(50, 60)
    
    tft.line((x_pos + 5), y_pos, x_pos, (y_pos + 5), tft.YELLOW)
    tft.line(x_pos, (y_pos + 5), (x_pos + 5), (y_pos + 5), tft.YELLOW)
    tft.line((x_pos + 5), (y_pos + 5), x_pos, (y_pos + 10), tft.YELLOW)
    
    
def mist():
    for i in range(0, 15):
        tft.hline(random.randrange(40, 60), random.randrange(20, 60, 4), 45, tft.CYAN)
        
        
def aqi_graphics(value):
    value_l = [0, 51, 101, 201, 301, 401]
    value_h = [50, 100, 200, 300, 400, 500]
    col = [(0, 128, 64), (0, 255, 64), (0, 255, 0), (255, 255, 0), (255, 128, 0), (255, 0, 0)]
    
    tft.rect(10, 90, 140, 30, tft.WHITE)
    for i in range(12, 130, 23):
        j = (i // 22)
        tft.fill_rect(i, 92, 22, 26, tft.colour_generator(col[j][0], col[j][1], col[j][2]))
        tft.text(str(value_l[j]), (i - 2), 94, tft.BLACK)
        tft.text(str(value_h[j]), (i - 2), 108, tft.BLACK)
        
    temp = contrain(value, 0, 500)
    temp = int(map_value(temp, 0, 500, 12, 148))
    tft.line(temp, 85, (temp - 4), 81, tft.WHITE)
    tft.line(temp, 85, (temp + 4), 81, tft.WHITE)
    tft.line((temp - 4), 81, (temp + 4), 81, tft.WHITE)
    
    
def compass(value):
    tft.text("N", 80, 18, tft.RED)
    circle(80, 80, 42, False, tft.BLUE)
    circle(80, 80, 4, True, tft.BLUE)
    heading_in_radians = (value * conv_factor) 
    v1 = int(scale_factor_1 * math.cos(heading_in_radians))
    h1 = int(scale_factor_1 * math.sin(heading_in_radians))
    tft.line(80, 80, (80 + h1), (80 - v1), tft.GREEN)
    
    v2 = int(scale_factor_2 * math.cos((heading_in_radians - pi_by_2)))
    h2 = int(scale_factor_2 * math.sin((heading_in_radians - pi_by_2)))
    tft.line(80, 80, (80 - h2), (80 + v2), tft.CYAN)
    tft.line(80, 80, (80 + h2), (80 - v2), tft.CYAN)
     
    tft.line((80 + h1), (80 - v1), (80 + h2), (80 - v2),  tft.CYAN)
    tft.line((80 - h1), (80 + v1), (80 + h2), (80 - v2),  tft.CYAN)
    tft.line((80 + h1), (80 - v1), (80 - h2), (80 + v2),  tft.CYAN)
    tft.line((80 - h1), (80 + v1), (80 - h2), (80 + v2),  tft.CYAN)


def connect_and_check_wifi_status():
    global ip, connection_status
    
    if(wifi_station.isconnected()):
        if(connection_status == False):
            print("Connected to WiFi Network with SSID: " + WiFi_Credentials.SSID + " and with IP address: " + wifi_station.ifconfig()[0] + "\r\n")
            ip = wifi_station.ifconfig()[0]
            connection_status = True
            
    else:
        if(wifi_station.isconnected() == True):
            if(wifi_station.active() == True):
                wifi_station.active(False)
                sleep_ms(1000)
            
            wifi_station.disconnect()    
            sleep_ms(1000)
           
        print("Network Error!")
        try:
            wifi_station.active(True)
        except:
            print("Error!")
        LED.value(True)
        sleep_ms(300)
        try:
            wifi_station.connect(WiFi_Credentials.SSID, WiFi_Credentials.password)
            LED.value(False)
        except:
            print("Unable to connect!")
        sleep_ms(300)
        connection_status = False


tft.fill(tft.BLACK)
tft.show()


while(True):
    tft.fill(tft.BLACK)
    year, month, date, day, hour, minute, second, tz = rtcc.datetime()
    
    if((second % net_check_interval) == 0):
        connect_and_check_wifi_status()
    
    if(second != past_second):        
        LED_state ^= 0x01
        counter += 1
        if(counter > 59):
            counter = 0
            city_flag = False
        LED.value(LED_state)
        
        print("Time: " + str("%02u:" %hour) + str("%02u:" %minute) + str("%02u" %second)
                + "   Date: " + str("%02u/" %date) + str("%02u/" %month) + str("%4u" %year))
        past_second = second
    
    if(screen_counter == 1):
        tft.text("ESP32 Air Visual API", 0, 4, tft.WHITE)
        tft.text("Local Time and Date", 0, 40, tft.YELLOW)
        tft.text(("Time: " + str("%02u:" %hour) + str("%02u:" %minute) + str("%02u" %second)), 0, 50, tft.YELLOW)
        tft.text(("Date: " + str("%02u/" %date) + str("%02u/" %month) + str("%4u" %year)), 0, 60, tft.YELLOW)
        tft.text(("City:" + str(air_visual_data[1])), 0, 75, tft.CYAN)
        tft.text(("State:" + str(air_visual_data[2])), 0, 85, tft.CYAN)
        tft.text(("Country:" + str(air_visual_data[3])), 0, 95, tft.CYAN)
        tft.text(str(air_visual_data[10]), 0, 115, tft.CYAN)    
        
    elif(screen_counter == 2):
        
        if(air_visual_data[16] == "01d"):
            sunny()
            
        elif(air_visual_data[16] == "01n"):
            night()
            
        elif(air_visual_data[16] == "02d"):
            sunny()
            cloudy(False, 90, 90, 90)
            
        elif(air_visual_data[16] == "02n"):
            night()
            cloudy(False, 128, 128, 128)
            
        elif(air_visual_data[16] == "03d"):
            cloudy(False, 160, 160, 160)
            
        elif(air_visual_data[16] == "03n"):
            cloudy(False, 60, 60, 50)
            
        elif(air_visual_data[16] == "04d"):
            cloudy(True, 75, 75, 75)
        
        elif(air_visual_data[16] == "09d"):
            cloudy(False, 90, 90, 90)
            rain()
            
        elif(air_visual_data[16] == "10d"):
            sunny()
            cloudy(True, 120, 120, 120)
            rain()
        
        elif(air_visual_data[16] == "10n"):
            night()
            cloudy(True, 80, 80, 80)
            rain()
            
        elif(air_visual_data[16] == "11d"):
            cloudy(False, 110, 110, 110)
            lightning()
            
        elif(air_visual_data[16] == "13d"):
            cloudy(False, 140, 140, 140)
            snow()
        
        else:
            mist()        
        
        tft.text("Weather Data", 40, 95, tft.WHITE)
        tft.text((str("%04u" %air_visual_data[12]) + " kPa"), 0, 120, tft.CYAN)
        tft.text((str("%02u" %air_visual_data[11]) + "'C"), 75, 120, tft.CYAN)
        tft.text((str("%02u" %air_visual_data[13]) + "%"), 130, 120, tft.CYAN)
        
    elif(screen_counter == 3):
        compass(air_visual_data[15])
        tft.text("Wind Data", 52, 4, tft.WHITE)
        tft.text((str("%02u" %air_visual_data[14]) + " m/s"), 0, 120, tft.CYAN)
        tft.text((str("%02u" %air_visual_data[15]) + "'N"), 115, 120, tft.CYAN)
        
    elif(screen_counter == 4):
        aqi_graphics(air_visual_data[6])
        tft.text("AQI", 71, 4, tft.WHITE)
        tft.text("PM2.5", 64, 20, tft.BLUE)
        tft.text((str("%02u" %air_visual_data[6]) + " ug/m3"), 46, 40, tft.CYAN)
        
    elif(screen_counter == 0):
        tft.fill(tft.BLACK)
        tft.text("Updating", 50, 40, tft.WHITE)        
        
    if(connection_status == True):
        screen_counter = (counter // screen_change_interval)
        
        if(screen_counter == 1):
            tft.text(("WiFi: " + WiFi_Credentials.SSID), 0, 20, tft.GREEN)
            tft.text(("IP: " + str(ip)), 0, 30, tft.GREEN)
                        
            if(city_flag == False):
                try:
                    air_visual_data = av.fetch_data()
                except:
                    print("Unable to download data!")
                
                av = air_visual(lat[city_counter], lon[city_counter], air_visual_credential.api_key)
                screen_counter = 1
                print(air_visual_data)
                city_counter = city_counter + 1
                counter = 0 
                if(city_counter > 19):
                    city_counter = 0
                city_flag = True

        if(time_sync_status == False):            
            if(second == 0):
                data_pull_flag = True
                time_sync_status = True
        
        else:
            if(((hour % sync_hour) == 0) and (minute == 0) and (second == 0)):
                data_pull_flag = True
                
        if(data_pull_flag == True):
            
            try:
                unix_time_stamp = ts.fetch_data()
                air_visual_data = av.fetch_data()
                tft.text("*", 150, 40, tft.GREEN)
            except:
                print("Unable to download data!")
            
            year, month, date, hour, minute, second = unx.unix_to_date_time(unix_time_stamp) 
            rtcc.datetime((year, month, date, day, hour, minute, second, tz))
            data_pull_flag = False
            
    else:
        tft.text("WiFi: No Network!", 0, 20, tft.RED)
        tft.text("IP: 0.0.0.0", 0, 30, tft.RED)
        time_sync_status = False
        screen_counter = 1
    
    tft.show()
