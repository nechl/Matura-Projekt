#!/usr/bin/env python3
import serial
import os

class Temperature():
    def __init__(self):
        ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
        ser.flush()

    def listenSerial(self):
        if ser.in_waiting > 0:
            temperature = ser.readline().decode('utf-8').rstrip()
            print(temperature)
            return temperature
