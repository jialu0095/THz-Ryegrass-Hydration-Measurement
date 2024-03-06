import serial
import numpy as np
import matplotlib.pyplot as plt
from terasense import processor


# open the serial port
serialPort = serial.Serial(port="COM4", baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
print('COM4 is open:', serialPort.isOpen())

# query the current attenuation value
serialPort.write(b':OUTP:ATT?\r')  
# read the response

# single-threaded mode instance
proc = processor.processor(threaded=False)
proc.SetNorm(data=None)
proc.SetExposure(3)

res = serialPort.read(100)
try:
    attenuation_value = float(res.decode().strip())  # response with attenuation value
    print("Current Attenuation:", attenuation_value, "dB")

    data = proc.read_raw()  # get img data
    # data = proc.read()  # get img data
    print("Data shape:", data.shape)
    print("Max value:", data.max())
    print("Min value:", data.min())
    np.savetxt('thz_data_API.txt', data, fmt='%f')  
    
except ValueError:
    print("Error reading attenuation value:", res.decode().strip())

# close the serial port
serialPort.close()



