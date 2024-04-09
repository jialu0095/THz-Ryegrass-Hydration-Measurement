import numpy as np
import matplotlib.pyplot as plt
from terasense import processor
import terasense.worker
import serial
import os

# change working dir
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

# proc instance
proc = processor.processor(threaded=False)

# set the accumulation
# proc.SetAccumulation(True)
# proc.SetAccuLength(1000)

# worker instance
worker = terasense.worker.Worker()
worker.SetGamma(1)

# set the working area
x_left = 12
x_right = 23
y_top = 9
y_bottom = 23

x_shape = x_right - x_left + 1
y_shape = y_bottom - y_top + 1

working_index = np.loadtxt('working_index.txt', delimiter=' ', comments='#').astype(int)

# set the background data
bg_data = np.loadtxt('thz_bg_data.txt', delimiter=' ', comments='#')
bg_data = bg_data[x_left:(x_right+1), y_top:(y_bottom+1)].flatten()

# pixel number in the working area
# n_pixels = (x_right - x_left + 1) * (y_bottom - y_top  + 1)

# variables
alphas = []
d_H2O = 0.02
saturated_threshold = 0.5
start_attenuation_value = 15
attenuation_step = 0.1
top_elements = 10

test_group = 'empty'
wet_title = "wet9"

dry_title = "dry"

try:
    print("-----------------------------------")

    # set initail attenuation
    set_attenuation(serialPort, start_attenuation_value)
    attenuation_value = query_attenuation(serialPort)
    print_attenuation(attenuation_value)

    # remove bg noise
    data = proc.read()[x_left:(x_right+1), y_top:(y_bottom+1)].flatten() - bg_data
    data = data[working_index]
    Is = proc.read()[x_left:(x_right+1), y_top:(y_bottom+1)].flatten() - bg_data
    Is = Is[working_index]

    while True:
        set_attenuation(serialPort, start_attenuation_value - attenuation_step)
        attenuation_value = query_attenuation(serialPort)
        print_attenuation(attenuation_value)
        data = proc.read()[x_left:(x_right+1), y_top:(y_bottom+1)].flatten() - bg_data
        
        data = data[working_index]

        # break when avrg intensity just not saturated
        print(np.mean(data))
        if(np.mean(data) > saturated_threshold):
            break

        # stronger beam
        Is = proc.read()[x_left:(x_right+1), y_top:(y_bottom+1)].flatten() - bg_data
        Is = Is[working_index]
        start_attenuation_value -= attenuation_step

        if(start_attenuation_value <= 0.1):
            break

    # save data files (can't plot with polygon shape pixels)
    # Is = Is.reshape((x_shape, y_shape))  # reshape for plot
    # Is = np.rot90(Is)  
    # Is = np.rot90(Is)  
    # Is = np.rot90(Is)
    # Is = np.fliplr(Is) 
    if(test_group == 'wet'):
        np.savetxt(wet_title+'.txt', Is, fmt='%f')
    #     plt.imshow(Is, cmap='jet')  # display the data as a pesudo color img
    #     plt.colorbar()  
    #     plt.title(wet_title)
    #     plt.show()
    #     # plt.close()
    elif(test_group == 'dry'):
        np.savetxt(dry_title+'.txt', Is, fmt='%f')
    #     plt.imshow(Is, cmap='jet')  # display the data as a pesudo color img
    #     plt.colorbar()  
    #     plt.title(dry_title)
    #     plt.show()
    #     # plt.close()
    elif(test_group == 'empty'):
        np.savetxt('empty.txt', Is, fmt='%f')
    
except ValueError:
    print("Error: ", ValueError)
    print("Error reading attenuation value:", res.decode().strip())
finally:
    set_attenuation(serialPort, 0)

# close the serial port
serialPort.close()