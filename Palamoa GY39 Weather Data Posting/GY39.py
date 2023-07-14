from micropython import const
from utime import sleep_ms
import gc


GY39_TX_buffer_size = const(3)
GY39_RX_buffer_size_1 = const(9)
GY39_RX_buffer_size_2 = const(15)

GY39_header_frame = const(0x5A)

GY39_packet_identifier_1 = const(0x15)
GY39_packet_identifier_2 = const(0x45)

GY39_packet_size_1 = const(0x04)
GY39_packet_size_2 = const(0x0A)

GY39_I2C_address_change_CMD = const(0xAA)
GY39_data_mode_CMD = const(0xA5)

GY39_light_output_CMD = const(0x51)
GY39_environment_output_CMD = const(0x52)

GY39_baud_9600_CMD = const(0xAE)
GY39_baud_115200_CMD = const(0xAF)

GY39_data_header_1_frame_positon = const(0)
GY39_data_header_2_frame_positon = const(1)
GY39_packet_identifier_frame_positon = const(2)
GY39_packet_size_frame_positon = const(3)
GY39_temperture_MSB_frame_positon = const(4)
GY39_temperture_LSB_frame_positon = const(5)
GY39_light_byte_1_frame_positon = const(4)
GY39_light_byte_2_frame_positon = const(5)
GY39_light_byte_3_frame_positon = const(6)
GY39_light_byte_4_frame_positon = const(7)
GY39_air_pressure_byte_1_frame_positon = const(6)
GY39_air_pressure_byte_2_frame_positon = const(7)
GY39_air_pressure_byte_3_frame_positon = const(8)
GY39_air_pressure_byte_4_frame_positon = const(9)
GY39_humidity_MSB_frame_positon = const(10)
GY39_humidity_LSB_frame_positon = const(11)
GY39_altitude_MSB_frame_positon = const(12)
GY39_altitude_LSB_frame_positon = const(13)
GY39_CRC_1_frame_positon = const(8)
GY39_CRC_2_frame_positon = const(14)


class GY39():
    def __init__(self, _uart):
        self.rx_data_frame_2 = bytearray(GY39_RX_buffer_size_2)
               
        self.t = 0
        self.p = 0
        self.rh = 0
        self.alt = 0
        self.lux = 0
        
        self.t_min = -40
        self.t_max = 85
        self.rh_min = 0
        self.rh_max = 100
        self.p_min = 300
        self.p_max = 1100
        self.alt_min = 0
        self.alt_max = 20000
        self.lux_min = 0
        self.lux_max = 150000
        
        self.uart = _uart
        
        
    def send_data(self, cmd1, cmd2):
        tx_data_frame = bytearray(GY39_TX_buffer_size)
        
        tx_data_frame[0x00] = cmd1
        tx_data_frame[0x01] = cmd2
        tx_data_frame[0x02] = ((cmd1 + cmd2) & 0xFF)
        try:
            self.uart.write(tx_data_frame)
        except:
            print("Unable to request sensor for data!")
        gc.collect()
        sleep_ms(600)
        
        
    def set_output_type(self, mode):
        self.send_data(GY39_data_mode_CMD, mode)
        
        
    def set_baud_rate(self, baud):
        self.send_data(GY39_data_mode_CMD, baud)
        
        
    def set_I2C_address(self, addr):
        self.send_data(GY39_I2C_address_change_CMD, addr)
        
        
    def get_light_output(self):
        i = 0
        crc = 0
        lux_current = 0
        rx_data_frame = bytearray(GY39_RX_buffer_size_1)
        
        for i in range (GY39_data_header_1_frame_positon, (GY39_CRC_1_frame_positon + 1)):
            rx_data_frame[i] = 0x00
        
        self.set_output_type(GY39_light_output_CMD)
        try:
            if(self.uart.any() > 0x00):
                try:
                    rx_data_frame = self.uart.read(GY39_RX_buffer_size_1)
                except:
                    for i in range (GY39_data_header_1_frame_positon, (GY39_CRC_1_frame_positon + 1)):
                        rx_data_frame[i] = 0x00
                
                if(rx_data_frame[GY39_data_header_1_frame_positon] == GY39_header_frame):
                    
                    if(rx_data_frame[GY39_data_header_2_frame_positon] == GY39_header_frame):
                        
                        if(rx_data_frame[GY39_packet_identifier_frame_positon] == GY39_packet_identifier_1):
                            
                            if(rx_data_frame[GY39_packet_size_frame_positon] == GY39_packet_size_1):
                                
                                lux_current = ((rx_data_frame[GY39_light_byte_1_frame_positon] << 24) +
                                               (rx_data_frame[GY39_light_byte_2_frame_positon] << 16) +
                                               (rx_data_frame[GY39_light_byte_3_frame_positon] << 8) +
                                               (rx_data_frame[GY39_light_byte_4_frame_positon]))
                                
                                lux_current /= 100
                                
                                for i in range(GY39_data_header_1_frame_positon, GY39_CRC_1_frame_positon):
                                    crc += rx_data_frame[i]
                                
                                crc &= 0xFF
                                
                                if(crc == rx_data_frame[GY39_CRC_1_frame_positon]):
                                    if((lux_current >= self.lux_min) and (lux_current <= self.lux_max)):
                                        return lux_current
                                else:
                                    lux_current = -1
        except:
            print("Error in fetching sensor data!")
    
    
    def get_environment_output(self):
        i = 0
        crc = 0
        t = 0
        p = 0
        rh = 0
        alt = 0
        t_current = 0
        p_current = 0
        rh_current = 0
        alt_current = 0
        rx_data_frame = bytearray(GY39_RX_buffer_size_2)
        
        for i in range (GY39_data_header_1_frame_positon, (GY39_CRC_2_frame_positon + 1)):
            rx_data_frame[i] = 0x00
        
        self.set_output_type(GY39_environment_output_CMD)
        
        try:
            if(self.uart.any() > 0x00):
                try:
                    rx_data_frame = self.uart.read(GY39_RX_buffer_size_2)
                except:
                    for i in range (GY39_data_header_1_frame_positon, (GY39_CRC_2_frame_positon + 1)):
                        rx_data_frame[i] = 0x00
                
                if(rx_data_frame[GY39_data_header_1_frame_positon] == GY39_header_frame):
                    
                    if(rx_data_frame[GY39_data_header_2_frame_positon] == GY39_header_frame):
                        
                        if(rx_data_frame[GY39_packet_identifier_frame_positon] == GY39_packet_identifier_2):
                            
                            if(rx_data_frame[GY39_packet_size_frame_positon] == GY39_packet_size_2):
                                
                                t_current = (((rx_data_frame[GY39_temperture_MSB_frame_positon] << 8) +
                                              (rx_data_frame[GY39_temperture_LSB_frame_positon])) / 100)
                                
                                p_current = (((rx_data_frame[GY39_air_pressure_byte_1_frame_positon] << 24) +
                                              (rx_data_frame[GY39_air_pressure_byte_2_frame_positon] << 16) +
                                              (rx_data_frame[GY39_air_pressure_byte_3_frame_positon] << 8) +
                                              (rx_data_frame[GY39_air_pressure_byte_4_frame_positon])) / 10000)
                                
                                rh_current = (((rx_data_frame[GY39_humidity_MSB_frame_positon] << 8) +
                                               (rx_data_frame[GY39_humidity_LSB_frame_positon])) / 100)
                                
                                alt_current = ((rx_data_frame[GY39_altitude_MSB_frame_positon] << 8) +
                                               (rx_data_frame[GY39_altitude_LSB_frame_positon]))
                                
                                for i in range(GY39_data_header_1_frame_positon, GY39_CRC_2_frame_positon):
                                    crc += rx_data_frame[i]
                                
                                crc &= 0xFF
                                
                                if(crc == rx_data_frame[GY39_CRC_2_frame_positon]):
                                    if((t_current >= self.t_min) and (t_current <= self.t_max)):
                                        t = t_current                        
                                    else:
                                        t = -255
                                        
                                    if((p_current >= self.p_min) and (p_current <= self.p_max)):
                                        p = p_current                        
                                    else:
                                        p = -255
                                        
                                    if((rh_current >= self.rh_min) and (rh_current <= self.rh_max)):
                                        rh = rh_current                        
                                    else:
                                        rh = -255
                                    
                                    if((alt_current >= self.alt_min) and (alt_current <= self.alt_max)):
                                        alt = alt_current                        
                                    else:
                                        alt = -255
                                        
                                    return t, p, rh, alt
                                        
                                else:
                                    return 0, 0, 0, 0

        except:
            print("Error in fetching sensor data!")


    def get_data(self):
        l = 0
        t = 0
        p = 0
        rh = 0
        alt = 0
        
        l = self.get_light_output()
        t, p, rh, alt = self.get_environment_output()
        
        return l, t, p, rh, alt