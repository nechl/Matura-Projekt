#import modules
try:
    import RPi.GPIO as GPIO
    import time
except ModuleNotFoundError:
    print("Not all modules required were found...")

#class for controlling the valve for the waterinflux
class Valve():
    def __init__(self, valve1, valve2):
        self.valve_in_1 = valve1
        self.valve_in_2 = valve2
        self.constantSecondsPerLiter = 8
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

        time.sleep(self.constantSecondsPerLiter * liters)

        GPIO.output(self.valve_in_1, GPIO.LOW)
        GPIO.output(self.valve_in_2, GPIO.LOW)
   
    def destroy(self):
        GPIO.output(self.valve_in_1, GPIO.LOW)
        GPIO.output(self.valve_in_2, GPIO.LOW)
        GPIO.cleanup()

if __name__ == "__main__":
    valve = Valve(21,20)
    try:
        while True:
            x = str(input("Open/Close[1/2]"))
            if x == "1":
                print("[+]Open Valve")
                valve.openValve()
            elif x == "2":
                print("[+]Close Valve")
                valve.closeValve()
            elif x == "3":
                print("[+]Testing Valve")
            elif x == "4":

                valve.openValveForLiters(3.5)
    except KeyboardInterrupt:
        valve.destroy()
