import serial

ser = serial.Serial('/dev/tty.usbmodem1421',9600)
print ser.name

while(True):
    print ser.readline();
