import serial
import numpy as np
import matplotlib.pyplot as plt
from terasense import processor


# Open the serial port
serialPort = serial.Serial(port="COM4", baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
print('COM4 is open:', serialPort.isOpen())

# Query the current attenuation value
serialPort.write(b':OUTP:ATT?\r')  # Assuming this is the command to query the attenuation value
# Read the response

# Initialize an instance of the processor class in single-threaded mode
proc = processor.processor(threaded=False)
proc.SetNorm(data=None)

res = serialPort.read(100)
try:
    attenuation_value = float(res.decode().strip())  # response with attenuation value
    print("Current Attenuation:", attenuation_value, "dB")

    data = proc.read()  # get img data
    print("Data shape:", data.shape)
    print("Max value:", data.max())
    print("Min value:", data.min())
    # np.savetxt('thz_data_test.txt', data, fmt='%f')  
    
except ValueError:
    print("Error reading attenuation value:", res.decode().strip())

# Close the serial port
serialPort.close()
