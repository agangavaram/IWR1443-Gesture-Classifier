import subprocess
from sys import platform
import serial
import time
import numpy as np
from main_classifier import process_gesture_metrics

cli_port = {}
data_port = {}
byte_buffer = np.zeros(52, dtype='uint8')
byte_buffer_length = 0
result = 0
mode = 0

def send_config_to_sensor(p_form, config_file):
    global cli_port
    global data_port
    global robot_port
   # Initialize serial ports for config and data
#   if p_form == "linux" or p_form == "linux2":
#       cli_port = serial.Serial('/dev/ttyACM0', 115200)
#       data_port = serial.Serial('/dev/ttyACM1', 921600)
#   elif p_form == "win32":
#       p = subprocess.Popen('wmic path win32_pnpentity get caption /format:list | find "COM"')
#       (output, err) = p.communicate()
    cli_port = serial.Serial('COM6', 115200)
    data_port = serial.Serial('COM7', 921600)
   # Read config and send to sensor
    config = [line.rstrip('\r\n') for line in open('sensorConfig.cfg')]
    for i in config:
        cli_port.write((i + '\n').encode())
        time.sleep(0.01)

    return cli_port, data_port


def process_data(data_port):
    global byte_buffer
    global byte_buffer_length
    global result
    global mode
   # size of packet received from sensor & how many packets wanted
    packet_size = 13
    num_packet_collect = 4
    packet_counter = 0

    try:
        while packet_counter < num_packet_collect:
            read_buffer = data_port.read(data_port.in_waiting)
            byte_vec = np.frombuffer(read_buffer, dtype='float32')
            byte_count = byte_vec.size

       # check whether buffer is full
            if byte_count != 0:
                if (byte_buffer_length + byte_count) < (packet_size * (num_packet_collect+1)):
                    byte_buffer[byte_buffer_length:byte_buffer_length + byte_count] = byte_vec[:byte_count]
                    byte_buffer_length = byte_buffer_length + byte_count
                else:
                    byte_buffer_length = 0

                # increment packet counter
                packet_counter += 1
       # check magic word
        if byte_buffer[0] == 11:
            result = process_gesture_metrics(byte_buffer, packet_size, num_packet_collect)
            if result == 3:
                print("Swipe")
            if result == 1:
                print("Twirl")
    except ValueError:
        pass


# initialize serial, read config file & send to sensor
cli_port, data_port = send_config_to_sensor(platform, 'sensorConfig.cfg')

while 1:
    process_data(data_port)
    time.sleep(0.02)

