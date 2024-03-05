import serial

serialPort = serial.Serial( port="COM4", baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
 

print('com4 is open', serialPort.isOpen())

serialPort.write(b'*IDN?\r')     ### you've used "read" wrongly
res = serialPort.read(100)    

serialPort.write(b':OUTP:ATT 3\r')              

res = serialPort.read(100)            ###   you always need to read a response after the write even if the command does not return anything.


if res==b'\r':                                  ### empty string is returned if there should be no response and everything is OK
    print('OK')
else:
    print("Error code: "+ res.decode().strip())     ### error code is returned if something is wrong

serialPort.close()