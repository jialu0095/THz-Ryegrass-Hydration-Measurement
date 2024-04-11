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

# set the accumulation
# proc.SetAccumulation(True)
# proc.SetAccuLength(1000)

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
start_attenuation_value = 8
attenuation_step = 0.1
top_elements = 10
nonsat_pixel_value = 0

I_drys = []
I_wets = []

dB_drys = []
dB_wets = []

test_group = 'dry'
group_number = "1"

wet_I_title = "wet_I" + group_number
wet_dB_title = "wet_dB"+ group_number

dry_I_title = "dry_I"
dry_dB_title = "dry_dB"

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
        block_value = np.mean(data_block)

        if(block_value > saturated_threshold):
            if test_group == 'wet':   
                I_wets.append(block_value)
                dB_wets.append(attenuation_value)
                flag = False
            elif test_group == 'dry':
                I_drys.append(block_value) 
                dB_drys.append(attenuation_value)
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
            block_value = np.mean(data_block)

            # if saturated, then stop
            print(block_value, attenuation_value, flag)
            if(block_value > saturated_threshold or attenuation_value <= attenuation_step):
                if test_group == 'wet':   
                    I_wets.append(nonsat_pixel_value)
                    dB_wets.append(attenuation_value)
                    flag = False
                elif test_group == 'dry':
                    I_drys.append(nonsat_pixel_value) 
                    dB_drys.append(attenuation_value)
                    flag = False

            if(flag):
                nonsat_pixel_value = block_value
                attenuation_value -= attenuation_step


    # save data files
    if(test_group == 'wet'):
        Is = np.array(I_wets)
        np.savetxt(f'{wet_I_title}.txt', I_wets, fmt='%f')
        np.savetxt(f'{wet_dB_title}.txt', dB_wets, fmt='%f')
        print("data saved")
    elif(test_group == 'dry'):
        Is = np.array(I_drys)
        np.savetxt(f'{dry_I_title}.txt', I_drys, fmt='%f')
        np.savetxt(f'{dry_dB_title}.txt', dB_drys, fmt='%f')
        print("data saved")

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