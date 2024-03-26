import numpy as np
import matplotlib.pyplot as plt
from terasense import processor
import terasense.worker
import serial
import os

# change working dir
os.chdir('water_layer_expr_API')
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
x_left = 15
x_right = 16
y_top = 8
y_bottom = 23

# set the background data
bg_data = np.loadtxt('thz_bg_data.txt', delimiter=' ', comments='#')
bg_data = bg_data[x_left:(x_right+1), y_top:(y_bottom+1)].flatten()

# pixel number in the working area
n_pixels = (x_right - x_left + 1) * (y_bottom - y_top  + 1)

# variables
I_refs = []
I_smps = []
dB_refs = []
dB_smps = []
alphas = []
d_H2O = 0.02
saturated_threshold = 0.5
start_attenuation_value = 13
attenuation_step = 0.4

test_group = 'smp'

# alpha = [ ln(I_ref / I_smp) + 0.1*ln10 * (dB_ref - dB_smp) ] / d_H20

try:
    print("-----------------------------------")

    # set initail attenuation
    set_attenuation(serialPort, start_attenuation_value)
    attenuation_value = query_attenuation(serialPort)
    print_attenuation(attenuation_value)

    # pixel by pixel data collection
    for pixel in range(0, n_pixels):
        set_attenuation(serialPort, start_attenuation_value)
        attenuation_value = query_attenuation(serialPort)
        print("-----------------------------------")
        print_attenuation(attenuation_value)
        print("Pixel:", pixel, "of", n_pixels, "pixels")
        # collect pixel value and atnu of just not saturated pixel
        flag = True
        while flag:
            set_attenuation(serialPort, attenuation_value-attenuation_step)  # alter attenuation
            attenuation_value = query_attenuation(serialPort)
            
            data = proc.read()
            pixel_value = data[x_left:(x_right+1), y_top:(y_bottom+1)].flatten()
            pixel_value = pixel_value - bg_data
            pixel_value = pixel_value[pixel]

            # if saturated, then stop
            print(pixel_value, attenuation_value, flag)
            if(pixel_value > saturated_threshold or attenuation_value <= attenuation_step):
                if test_group == 'ref':   
                    I_refs.append(nonsat_pixel_value)
                    dB_refs.append(attenuation_value)
                    flag = False
                elif test_group == 'smp':
                    I_smps.append(nonsat_pixel_value) 
                    dB_smps.append(attenuation_value)
                    flag = False

            if(flag):
                nonsat_pixel_value = pixel_value
                attenuation_value -= attenuation_step
        

    # save data files
    if(test_group == 'ref'):
        if(d_H2O == 0.05):
            np.savetxt('I_refs_05', I_refs, fmt='%f') 
            np.savetxt('dB_refs_05', dB_refs, fmt='%f') 
        elif(d_H2O == 0.02):
            np.savetxt('I_refs_02', I_refs, fmt='%f') 
            np.savetxt('dB_refs_02', dB_refs, fmt='%f')
    elif(test_group == 'smp'):
        if(d_H2O == 0.05):
            np.savetxt('I_smps_05', I_smps, fmt='%f') 
            np.savetxt('dB_smps_05', dB_smps, fmt='%f')
        elif(d_H2O == 0.02):
            np.savetxt('I_smps_02', I_smps, fmt='%f') 
            np.savetxt('dB_smps_02', dB_smps, fmt='%f')
    # np.set_printoptions(suppress=True, precision=2)

    
except ValueError:
    print("Error: ", ValueError)
    print("Error reading attenuation value:", res.decode().strip())
finally:
    set_attenuation(serialPort, 0)

# close the serial port
serialPort.close()