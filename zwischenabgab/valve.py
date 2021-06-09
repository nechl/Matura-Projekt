#import modules
import RPi.GPIO as GPIO
import time

valve_in_1 = 21
valve_in_2 = 20

constantLitersPerSecond = 1.0
def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(valve_in_1, GPIO.OUT)
    GPIO.setup(valve_in_2, GPIO.OUT)

def openValve():
    GPIO.output(valve_in_1, GPIO.HIGH)
    GPIO.output(valve_in_2, GPIO.LOW)

def closeValve():
    GPIO.output(valve_in_1, GPIO.LOW)
    GPIO.output(valve_in_2, GPIO.LOW)

def openValveForLiters(liters):
    GPIO.output(valve_in_1, GPIO.HIGH)
    GPIO.output(valve_in_2, GPIO.LOW)

    time.sleep(liters / constantLitersPerSecond)

    GPIO.output(valve_in_1, GPIO.LOW)
    GPIO.output(valve_in_2, GPIO.LOW)

def loop():
    while True:
        x = str(input("Open/Close[1/2]"))
        if x == "1":
            print("[+]Open Valve")
            openValve()
        elif x == "2":
            print("[+]Close Valve")
            closeValve()
        else:
            pass

def destroy():
    GPIO.output(valve_in_1, GPIO.LOW)
    GPIO.output(valve_in_2, GPIO.LOW)
    GPIO.cleanup()

if __name__ == "__main__":
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()