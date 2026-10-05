import serial
#When endoder is plug to microcontroller tto read
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)

while True:
    line = ser.readline().decode('utf-8').strip()
    if line:
        print(line)  # will print "Angle: 82.3"