import numpy as np
import numpy as np
import matplotlib.pyplot as plt
from terasense import processor
import terasense.worker
import serial
import os

os.chdir('leaf_expr_API')
print(os.getcwd())

def set_attenuation(serialPort, attenuation):
    serialPort.write(b':OUTP:ATT ' + str(attenuation).encode() + b'\r')

def query_attenuation(serialPort):
    serialPort.write(b':OUTP:ATT?\r')
    res = serialPort.read(100)
    attenuation_value = float(res.decode().strip())
    return attenuation_value

def print_attenuation(attenuation_value):
    print("Current Attenuation:", attenuation_value, "dB")


# open the serial port
serialPort = serial.Serial(port="COM4", baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
print('COM4 is open:', serialPort.isOpen())
serialPort.write(b':OUTP:ATT?\r')   # query the attenuation
res = serialPort.read(100)  # read response

set_attenuation(serialPort, 6)
attenuation_value = query_attenuation(serialPort)
print_attenuation(attenuation_value)

# proc instance
proc = processor.processor(threaded=False)

# worker instance
worker = terasense.worker.Worker()
worker.SetGamma(1)

data = proc.read()

# set the working area
x_left = 12
x_right = 23
y_top = 9
y_bottom = 23

x_shape = x_right - x_left + 1
y_shape = y_bottom - y_top + 1

data = data[x_left:(x_right+1), y_top:(y_bottom+1)].flatten()

# set the background data
bg_data = np.loadtxt('thz_bg_data.txt', delimiter=' ', comments='#')
bg_data = bg_data[x_left:(x_right+1), y_top:(y_bottom+1)].flatten()

data = data - bg_data

# pixel number in the working area
n_pixels = (x_right - x_left + 1) * (y_bottom - y_top  + 1)

working_index = []
not_working_index = []
for i in range(n_pixels):
    if data[i] > 0.5:
        working_index.append(i)
    else:   
        not_working_index.append(i)

print(working_index)
print(not_working_index)

np.savetxt('working_index.txt', working_index, fmt='%d')



