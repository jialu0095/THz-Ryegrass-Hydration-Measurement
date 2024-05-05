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

I_drys = []
I_wets = []

dB_drys = []
dB_wets = []

I_0s = []
title = 'I_0s_dry.txt'


try:
    print("-----------------------------------")

    # set initail attenuation
    set_attenuation(serialPort, start_attenuation_value)
    attenuation_value = query_attenuation(serialPort)
    print_attenuation(attenuation_value)

    # remove bg noise
    data = proc.read() - bg_data

    # to store the blocks
    data_blocks = []

    # traverse data and extract 4x4 blocks in to a 1*64 array
    for i in range(0, 8):
        for j in range(0, 8):
            # extract 4x4 blocks
            flattened_block = data[i*4:(i+1)*4, j*4:(j+1)*4].flatten()
            # flatten the block
            data_blocks.append(flattened_block)

    Is = data_blocks

    for block in range(0, 64):
        # initial settings
        set_attenuation(serialPort, start_attenuation_value)
        attenuation_value = query_attenuation(serialPort)
        print("-----------------------------------")
        print_attenuation(attenuation_value)
        print("Block:", block+1, "of", len(data_blocks), "blocks")

        flag = True

        data = proc.read() - bg_data
        data_blocks = create_block_data(data)
        data_block = data_blocks[block]
        # remove empty pixel
        data_block = data_block[data_block < 0.5]
        data_block_I0 = 10**(attenuation_value/10)*data_block
        block_value = np.mean(data_block)

        if(block_value > saturated_threshold):
            flag = False

        # collect block avrg value and atnu of just not saturated pixel
        while flag:
            set_attenuation(serialPort, attenuation_value-attenuation_step)  # alter attenuation
            attenuation_value = query_attenuation(serialPort)
            
            # get data and change to block data
            data = proc.read() - bg_data

            # maybe remove outlier here?
            # need the died plant to compare

            data_blocks = create_block_data(data)
            data_block = data_blocks[block]

            # remove empty pixel
            data_block_I0 = 10**(attenuation_value/10)*data_block
            block_value = np.mean(data_block)

            # if saturated, then stop
            print(block_value, attenuation_value, flag)
            if(block_value > saturated_threshold or attenuation_value <= attenuation_step):
                print(data_block_I0)
                flag = False
                I_0s.append(data_block_I0)


            if(flag):
                nonsat_pixel_value = block_value
                attenuation_value -= attenuation_step

    np.savetxt(title, I_0s, delimiter=' ', comments='#')
    print('data saved')

    
except ValueError:
    print("Error: ", ValueError)
    print("Error reading attenuation value:", res.decode().strip())
finally:
    set_attenuation(serialPort, 0)

# close the serial port
serialPort.close()