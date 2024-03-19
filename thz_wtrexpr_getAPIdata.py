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

# worker instance
worker = terasense.worker.Worker()
worker.SetGamma(1)

# set the working area
x_left = 15
x_right = 16
y_top = 8
y_bottom = 23

x_left = 15
x_right = 16
y_top = 15
y_bottom = 16


n_pixels = (x_right - x_left + 1) * (y_bottom - y_top  + 1)

I_refs = []
I_smps = []
dB_refs = []
dB_smps = []
alphas = []
d_H2O = 0.05
saturated_threshold = 0.5
start_attenuation_value = 14

test_group = 'ref'

# alpha = [ ln(I_ref / I_smp) + 0.1*ln10 * (dB_ref - dB_smp) ] / d_H20

try:
    print("-----------------------------------")

    # set initail attenuation
    set_attenuation(serialPort, start_attenuation_value)
    attenuation_value = query_attenuation(serialPort)
    print_attenuation(attenuation_value)

    # pixel by pixel data collection
    for pixel in range(0, n_pixels):
        # data = proc.read()
        # pixel_value = data[x_left:x_right, y_top:y_bottom].flatten()[pixel]

        # collect pixel value and atnu of just not saturated pixel
        while True:
            set_attenuation(serialPort, attenuation_value-0.2)  # alter attenuation
            attenuation_value = query_attenuation(serialPort)
            print(attenuation_value)
            # read working area data
            data = proc.read()
            pixel_value = data[x_left:(x_right+1), y_top:(y_bottom+1)].flatten()
            print(data[x_left:x_right, y_top:y_bottom])
            print('pixel value:', pixel_value)
            print('pixel value shape:', pixel_value.shape)
            print('pixel: ', pixel)
            print('pixel_value[pixel]', pixel_value[pixel])
            
            # if saturated, then stop
            print('yes')
            if(pixel_value < saturated_threshold):
                if test_group == 'ref':   
                    I_refs.append(pixel_value)
                    dB_refs.append(attenuation_value)
                elif test_group == 'smp':
                    I_smps.append(pixel_value) 
                    dB_smps.append(attenuation_value)
                break
            
            if(attenuation_value <= 0.2):
                break

            attenuation_value -= 0.2
        

    # save data files
    if(test_group == 'ref'):
        np.savetxt('I_refs', I_refs, fmt='%f') 
        np.savetxt('dB_refs', dB_refs, fmt='%f') 
    elif(test_group == 'smp'):
        np.savetxt('I_smps', I_smps, fmt='%f') 
        np.savetxt('dB_smps', dB_smps, fmt='%f')
    # np.set_printoptions(suppress=True, precision=2)

    
except ValueError:
    print("Error reading attenuation value:", res.decode().strip())
finally:
    set_attenuation(serialPort, 0)

# close the serial port
serialPort.close()