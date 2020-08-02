# Import Required Python libraries

import os
import glob
import time
import rrdtool

# Activate the GPIO and therm modules (Not sure if this is required)
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

# Identify thermal probe file path (this assumes only one probe at this stage)
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

# Define a function to read the raw data
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

# Define a function to intepret the raw data and output temperature in Celcius
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

# Loop every 1 second, reading and printing the temperature to the stdout (the screen)
while True:
	temp_c=read_temp()
	value="N:" + str(temp_c)
	rrdtool.update("tempdb.rrd", value)
	time.sleep(300)
