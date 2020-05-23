#!/usr/bin/env python3
import serial
import time
m1pwm = 200
m2pwm = 140
if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.flush()
    while True:
        send_data = str(m1pwm)+"#"+str(m2pwm)+"#\n"
        ser.write(send_data.encode("UTF-8"))
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
        time.sleep(1)
