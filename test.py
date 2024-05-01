import serial
from terasense import processor
import numpy as np

serialPort = serial.Serial( port="COM4", baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)

proc = processor.processor(threaded=False)

print('com4 is open', serialPort.isOpen())

serialPort.write(b'*IDN?\r')     ### you've used "read" wrongly
res = serialPort.read(100)    

serialPort.write(b':OUTP:ATT 14\r')              

res = serialPort.read(100)            ###   you always need to read a response after the write even if the command does not return anything.

x_left = 12
x_right = 23
y_top = 9
y_bottom = 23

start = 12

while True:
    data = proc.read()[x_left:(x_right+1), y_top:(y_bottom+1)].flatten()
    if np.mean(data) > 0.5:
        res = serialPort.read(100)
        attenuation_value = float(res.decode().strip())
        print(attenuation_value)
        break
    start -= 0.1
    serialPort.write(b':OUTP:ATT ' + str(start).encode() + b'\r')
    res = serialPort.read(100)  


serialPort.close()