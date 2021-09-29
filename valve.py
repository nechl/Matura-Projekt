#import modules
try:
    import RPi.GPIO as GPIO
    import time
except ModuleNotFoundError:
    print("Not all modules required were found...")

#class for controlling the valve for the waterinflux
class Valve():
    def __init__(self, pinINPUT):
        self.valve_in_1 = pinINPUT[0]
        self.valve_in_2 = pinINPUT[1]
        self.constantLitersPerSecond = 1.0
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.valve_in_1, GPIO.OUT)
        GPIO.setup(self.valve_in_2, GPIO.OUT)
    
    def __repr__(self):
        return("Valve([" + self.valve_in_1 + "," + self.valve_in_2+ "])")
        
    def openValve(self):
        GPIO.output(self.valve_in_1, GPIO.HIGH)
        GPIO.output(self.valve_in_2, GPIO.LOW)

    def closeValve(self):
        GPIO.output(self.valve_in_1, GPIO.LOW)
        GPIO.output(self.valve_in_2, GPIO.LOW)

    def openValveForLiters(self, liters):
        GPIO.output(self.valve_in_1, GPIO.HIGH)
        GPIO.output(self.valve_in_2, GPIO.LOW)

        time.sleep(liters / self.constantLitersPerSecond)

        GPIO.output(self.valve_in_1, GPIO.LOW)
        GPIO.output(self.valve_in_2, GPIO.LOW)

    def destroy(self):
        GPIO.output(self.valve_in_1, GPIO.LOW)
        GPIO.output(self.valve_in_2, GPIO.LOW)
        GPIO.cleanup()

if __name__ == "__main__":
    valve = Valve([21,20])
    try:
        while True:
            x = str(input("Open/Close[1/2]"))
            if x == "1":
                print("[+]Open Valve")
                valve.openValve()
            elif x == "2":
                print("[+]Close Valve")
                valve.closeValve()
            else:
                pass
    except KeyboardInterrupt:
        valve.destroy()
