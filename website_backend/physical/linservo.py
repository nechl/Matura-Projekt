# import all required libraries
try:
    import RPi.GPIO as GPIO
    import time
except ModuleNotFoundError:
    print("Not all modules required were found...")

delay = 0.0001

class LinServo():
    def __init__(self, step, dir1):
        self.step = step
        self.dir1 = dir1
	
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.step, GPIO.OUT)
        GPIO.setup(self.dir1, GPIO.OUT)

    def __repr__(self):
        return("LinServo(["+ str(self.step) +"," + str(self.dir1) +"])")
        
    def DownStep(self):
        GPIO.output(self.dir1, GPIO.LOW)
        for i in range(10000):
            GPIO.output(self.step, GPIO.LOW)
            time.sleep(delay)
            GPIO.output(self.step, GPIO.HIGH)
            time.sleep(delay)
            
    def DownStepDistance(self, cm=1):
        GPIO.output(self.dir1, GPIO.LOW)
        for i in range(4000*cm):
            GPIO.output(self.step, GPIO.LOW)
            time.sleep(delay)
            GPIO.output(self.step, GPIO.HIGH)
            time.sleep(delay)
        
    def UpStep(self):
        GPIO.output(self.dir1, GPIO.HIGH)
        for i in range(10000):
            GPIO.output(self.step, GPIO.LOW)
            time.sleep(delay)
            GPIO.output(self.step, GPIO.HIGH)
            time.sleep(delay)

    def UpStepDistance(self, cm=1):
        GPIO.output(self.dir1, GPIO.HIGH)
        for i in range(4000*cm):
            GPIO.output(self.step, GPIO.LOW)
            time.sleep(delay)
            GPIO.output(self.step, GPIO.HIGH)
            time.sleep(delay)
    def destroy(self):
        GPIO.output(self.dir1, GPIO.LOW)
        GPIO.output(self.step, GPIO.LOW)
        GPIO.cleanup()


if __name__ == '__main__':
    linservo = LinServo(27,22)

    while True:        
        x =str(input("input[1 = down ; 2 = up]: "))
        y =int(input("Distance? "))
        print (x)

        if x == "1":
            print("down")
            linservo.DownStepDistance(y)

        elif x =="2":
            print("up")
            linservo.UpStepDistance(y)
