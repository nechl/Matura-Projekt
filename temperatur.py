#!/usr/bin/env python3
import serial
import os

class Temperature():
    def listenSerial(self):
        self.ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
        self.ser.flush()
        if self.ser.in_waiting > 0:
            temperature = self.ser.readline().decode('utf-8').rstrip()
            print(temperature)
            
            temperature = int(temperature)
            return temperature
