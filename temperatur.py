#!/usr/bin/env python3
import serial
import os

class Temperature():
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
        self.ser.flush()
    def listenSerial(self):


        if self.ser.in_waiting > 0:
            temperature = self.ser.readline().decode('utf-8').rstrip()
            print(temperature)

            temperature = float(temperature)
            return temperature
if __name__ == "__main__":
    
    ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
    ser.flush()

    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
