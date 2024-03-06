import numpy as np
import matplotlib.pyplot as plt
import serial
from terasense import processor

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

# single-threaded mode instance
proc = processor.processor(threaded=False)

try:
    for i in range(0, 10, 3):
        # alter attenuation
        set_attenuation(serialPort, i)
        attenuation_value = query_attenuation(serialPort)
        print_attenuation(attenuation_value)

        data = proc.read()  # get img data
        print("Max value:", data.max())
        
    
    # data = proc.read()  # get img data
    # print("Data shape:", data.shape)
    # print("Max value:", data.max())
    # print("Min value:", data.min())
    # # np.savetxt('thz_data_API.txt', data, fmt='%f')  
    
except ValueError:
    print("Error reading attenuation value:", res.decode().strip())

# close the serial port
serialPort.close()