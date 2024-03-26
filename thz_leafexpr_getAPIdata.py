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
x_left = 6
x_right = 26
y_top = 7
y_bottom = 15

x_shape = x_right - x_left + 1
y_shape = y_bottom - y_top + 1

# set the background data
bg_data = np.loadtxt('thz_bg_data.txt', delimiter=' ', comments='#')
bg_data = bg_data[x_left:(x_right+1), y_top:(y_bottom+1)].flatten()

# pixel number in the working area
n_pixels = (x_right - x_left + 1) * (y_bottom - y_top  + 1)

# variables
alphas = []
d_H2O = 0.02
saturated_threshold = 0.5
start_attenuation_value = 15
attenuation_step = 0.4
top_elements = 10

test_group = 'dry'

try:
    print("-----------------------------------")

    # set initail attenuation
    set_attenuation(serialPort, start_attenuation_value)
    attenuation_value = query_attenuation(serialPort)
    print_attenuation(attenuation_value)

    # remove bg noise
    data = proc.read()[x_left:(x_right+1), y_top:(y_bottom+1)].flatten() - bg_data
    Is = proc.read()[x_left:(x_right+1), y_top:(y_bottom+1)].flatten() - bg_data

    while True:
        set_attenuation(serialPort, start_attenuation_value - attenuation_step)
        attenuation_value = query_attenuation(serialPort)
        print_attenuation(attenuation_value)
        data = proc.read()[x_left:(x_right+1), y_top:(y_bottom+1)].flatten() - bg_data
        
        
        # break when avrg intensity just not saturated
        print(np.mean(np.sort(data)[-top_elements:]))
        if(np.mean(np.sort(data)[-top_elements:]) > saturated_threshold):
            break

        # stronger beam
        Is = proc.read()[x_left:(x_right+1), y_top:(y_bottom+1)].flatten() - bg_data
        start_attenuation_value -= attenuation_step   

    # save data files
    Is = Is.reshape((x_shape, y_shape))  # reshape for plot
    Is = np.rot90(Is)  
    Is = np.rot90(Is)  
    Is = np.rot90(Is)
    Is = np.fliplr(Is) 
    if(test_group == 'wet'):
        np.savetxt('I_wets', Is, fmt='%f')
        plt.imshow(Is, cmap='jet')  # display the data as a pesudo color img
        plt.colorbar()  
        plt.title('Wet Sample')
        plt.show()
        # plt.close()
    elif(test_group == 'dry'):
        np.savetxt('I_drys', Is, fmt='%f')
        plt.imshow(Is, cmap='jet')  # display the data as a pesudo color img
        plt.colorbar()  
        plt.title('Dry Reference 5')
        plt.show()
        # plt.close()
    
except ValueError:
    print("Error: ", ValueError)
    print("Error reading attenuation value:", res.decode().strip())
finally:
    set_attenuation(serialPort, 0)

# close the serial port
serialPort.close()