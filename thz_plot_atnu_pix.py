import numpy as np
import matplotlib.pyplot as plt
import serial
from terasense import processor
import terasense.worker


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

try:
    print("-----------------------------------")
    # collect average data values and attenuation
    attenuation_values = []
    average_values = []

    set_attenuation(serialPort, 0)
    attenuation_value = query_attenuation(serialPort)
    print_attenuation(attenuation_value)

    for i in range(0, 40, 1):
        # alter attenuation
        set_attenuation(serialPort, i)
        attenuation_value = query_attenuation(serialPort)
        print_attenuation(attenuation_value)

        # get average img data
        data = proc.read()
        average_value = np.mean(data)
        # average_value = data[15][15]

        # average_value = np.mean(data[10:22, 10:22])
        print("Average value:", average_value)
        # print("Max value:", data.max())
        print("-----------------------------------")

        # collect data
        attenuation_values.append(attenuation_value)
        average_values.append(average_value)

    # Plot attenuation against value
    plt.plot(attenuation_values, average_values)
    plt.xlabel("Attenuation (dB)")
    plt.ylabel("Average Data Value [0,1]")
    plt.show()
        
    print("Attenuation Values:", attenuation_values)
    print("Pixel Values:", average_values)
    
    np.set_printoptions(suppress=True, precision=2)

    
except ValueError:
    print("Error reading attenuation value:", res.decode().strip())
finally:
    set_attenuation(serialPort, 0)

# close the serial port
serialPort.close()