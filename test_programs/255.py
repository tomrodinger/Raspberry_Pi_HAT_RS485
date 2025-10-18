import serial
import time

# Open the serial port
ser = serial.Serial('/dev/tty.usbserial-1330', baudrate=1000000)

# Send the character 255 every 0.5 seconds
while True:
    ser.write(bytes([255]))
    time.sleep(0.5)
    