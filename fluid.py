import RPi.GPIO as GPIO
import time, sys
GPIO.setmode(GPIO.BCM)

class fluid():
    def __init__(self, pin):
        self.inputPin = pin
        self.rate_cnt = 0
        self.tot_cnt = 0
        self.minutes = 0
        self.constant = 0.10
        self.time_new = 0.0
        GPIO.setup(self.inputPin, GPIO.IN)
        
    def measure(self):
        
        print("Water Flow - Approximate")
        print("Control C to exit")
        while True:
            time_new = time.time() + 10
        
            while time.time() <= time_new:
                if GPIO.input(self.inputPin) != 0:
                    self.rate_cnt += 1
                    self.tot_cnt += 1
                try:
                    print(GPIO.input(self.inputPin), end="")
                except KeyboardInterrupt:
                    print("\nCTRL C - Exiting very smoothly")
                    GPIO.cleanup()
                    sys.exit()
            self.minutes += 1
            print("\nLiters / min", round(self.rate_cnt * self.constant,4))
            print("Total Liters", round(self.tot_cnt * self.constant, 4))
            print("Time (min & clock) ", self.minutes, "\t", time.asctime(time.localtime(time.time())),"\n")
    def destroy(self):
        GPIO.cleanup()


if __name__ == "__main__":
    Fluid = fluid(16)
    Fluid.measure()
    
