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

# create block data
def create_block_data(data):
    data_blocks = []
    for i in range(0, 8):
        for j in range(0, 8):
            flattened_block = data[i*4:(i+1)*4, j*4:(j+1)*4].flatten()
            data_blocks.append(flattened_block)
    return data_blocks

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
# bg_data = bg_data[x_left:(x_right+1), y_top:(y_bottom+1)].flatten()

# pixel number in the working area
n_pixels = (x_right - x_left + 1) * (y_bottom - y_top  + 1)

# variables
alphas = []
d_H2O = 0.02
saturated_threshold = 0.5
start_attenuation_value = 10
attenuation_step = 0.1
top_elements = 10
nonsat_pixel_value = 0

I_sat = [-1] * n_pixels
dB_sat = [-1] * n_pixels
pix_is_sat = [False] * n_pixels

test_group = 'dry'
group_number = "3"
plant_label = "1"
title = test_group + group_number + '_' + plant_label


try:
    print("-----------------------------------")

    # set initail attenuation
    set_attenuation(serialPort, start_attenuation_value)
    attenuation_value = query_attenuation(serialPort)
    print_attenuation(attenuation_value)

    # remove bg noise
    data = proc.read() - bg_data
    data_working = data[x_left:(x_right+1), y_top:(y_bottom+1)].flatten()

    # initial scan
    for index, pixel in enumerate(data_working):
        if pixel > saturated_threshold & pix_is_sat[index] == False:
            I_sat[index] = pixel
            dB_sat[index] = attenuation_value
            pix_is_sat[index] = True 

    # decrease attenuation
    while True:
        set_attenuation(serialPort, start_attenuation_value - attenuation_step)
        attenuation_value = query_attenuation(serialPort)
        print_attenuation(attenuation_value)
        data = proc.read() - bg_data
        data_working = data[x_left:(x_right+1), y_top:(y_bottom+1)].flatten()

        for index, pixel in enumerate(data_working):
            if pixel > saturated_threshold & pix_is_sat[index] == False:
                I_sat[index] = pixel
                dB_sat[index] = attenuation_value
                pix_is_sat[index] = True 

        start_attenuation_value -= attenuation_step

        if(start_attenuation_value <= 0.1):
            break


    # save data files
    np.savetxt(f'I_{title}.txt', I_sat, fmt='%f')
    np.savetxt(f'dB_{title}.txt', dB_sat, fmt='%f')
    print("data saved")

    Is = np.array(I_sat)
    # plot the data
    Is = Is.reshape((x_shape, y_shape))  # reshape for plot
    Is = np.rot90(Is)  
    Is = np.rot90(Is)  
    Is = np.rot90(Is)
    Is = np.fliplr(Is) 
    plt.imshow(Is, cmap='jet')  # display the data as a pesudo color img
    plt.colorbar()  
    plt.show()
    
except ValueError:
    print("Error: ", ValueError)
    print("Error reading attenuation value:", res.decode().strip())
finally:
    set_attenuation(serialPort, 0)

# close the serial port
serialPort.close()