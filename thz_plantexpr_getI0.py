import numpy as np
import matplotlib.pyplot as plt
from terasense import processor
import terasense.worker
import serial
import os

# change working dir
os.chdir('plant_expr_API')
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

def cal_I0(attenuation_value, pixel_value):
    return 10**(attenuation_value/10)*pixel_value

# open the serial port
serialPort = serial.Serial(port="COM4", baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
print('COM4 is open:', serialPort.isOpen())
serialPort.write(b':OUTP:ATT?\r')   # query the attenuation
res = serialPort.read(100)  # read response

# proc instance
proc = processor.processor(threaded=False)

# worker instance
worker = terasense.worker.Worker()
worker.SetGamma(1)

# set the working area
x_left = 0
x_right = 31
y_top = 0
y_bottom = 31

x_shape = x_right - x_left + 1
y_shape = y_bottom - y_top + 1

# set the background data
bg_data = np.loadtxt('thz_bg_data.txt', delimiter=' ', comments='#')

# pixel number in the working area
n_pixels = (x_right - x_left + 1) * (y_bottom - y_top  + 1)

# variables
alphas = []
d_H2O = 0.02
saturated_threshold = 0.5
start_attenuation_value = 11
attenuation_step = 0.1
top_elements = 10
nonsat_pixel_value = 0

pix_is_sat = [False] * n_pixels
I_0s = [-1]*n_pixels

title = 'I_0s_dry.txt'


try:
    print("-----------------------------------")

    # set initail attenuation
    attenuation_value = start_attenuation_value
    set_attenuation(serialPort, attenuation_value)
    attenuation_value = query_attenuation(serialPort)
    print_attenuation(attenuation_value)

    # remove bg noise
    data = proc.read() - bg_data
    data_working = data[x_left:(x_right+1), y_top:(y_bottom+1)].flatten()

    # initial scan
    for index, pixel in enumerate(data_working):
        if pixel > saturated_threshold and pix_is_sat[index] == False:
            pix_is_sat[index] = True 

    # decrease attenuation
    while True:
        # data before altering attenuation
        data_pre = proc.read() - bg_data
        data_working_pre = data_pre[x_left:(x_right+1), y_top:(y_bottom+1)].flatten()

        # decrease attenuation
        set_attenuation(serialPort, attenuation_value - attenuation_step)
        attenuation_value = query_attenuation(serialPort)
        print_attenuation(attenuation_value)

        # data after altering attenuation
        data = proc.read() - bg_data
        data_working = data[x_left:(x_right+1), y_top:(y_bottom+1)].flatten()

        # check for saturated pixels
        for index, pixel in enumerate(data_working):
            if (pixel > saturated_threshold) and pix_is_sat[index] == False:
                I_0 = cal_I0(attenuation_value, data_working_pre[index])
                I_0s[index] = I_0
                pix_is_sat[index] = True 

        # set the decreased attenuation for next loop
        attenuation_value -= attenuation_step

        # check how many un-saturated pixel left
        false_count = pix_is_sat.count(False)
        print("Number of False in pix_is_sat:", false_count)
        if all(pix_is_sat):
            break

        # for pixel that are still not saturated at 0.1 dB, record current pixel value
        if(attenuation_value <= 0.1):
            I_0 = cal_I0(attenuation_value, data_working[index])
            for index, pixel in enumerate(pix_is_sat):
                if pixel == False:
                    I_0s[index] = I_0
                    pix_is_sat[index] = True 
            break


    np.savetxt(title, I_0s, delimiter=' ', comments='#')
    print('data saved')

    
except ValueError:
    print("Error: ", ValueError)
    print("Error reading attenuation value:", res.decode().strip())
finally:
    set_attenuation(serialPort, 0)

# close the serial port
serialPort.close()