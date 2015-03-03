import serial

ser = serial.Serial('/dev/tty.usbserial',9600)
print ser.name
