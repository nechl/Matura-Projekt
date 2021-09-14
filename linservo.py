# import all required libraries
try:
    import RPi.GPIO as GPIO
    import time
except ModuleNotFoundError:
    print("Not all modules required were found...")

class LinServo():
    def __init__(self, pinINPUT, calPINS):
        self.motor_pin_A1 = pinINPUT[0]
        self.motor_pin_A2 = pinINPUT[1]
        self.motor_pin_B1 = pinINPUT[2]
        self.motor_pin_B2 = pinINPUT[3]
        self.calibratePinUp = calPINS[0]
        self.calibratePinDown = calPINS[1]
        self.delay = 0.01

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.motor_pin_A1, GPIO.OUT)
        GPIO.setup(self.motor_pin_A2, GPIO.OUT)
        GPIO.setup(self.motor_pin_B1, GPIO.OUT)
        GPIO.setup(self.motor_pin_B2, GPIO.OUT)
    def __repr__(self):
        return("LinServo([" + self.motor_pin_A1 + "," + self.motor_pin_A2 + "," + self.motor_pin_B1 + "," + self.motor_pin_B2 "],[" + self.calibratePinUp +","+ self.calibratePinDown +"])")
        
    def UpStep(self, cm):
        for i in range(cm * 133):
            self.setStepper(1,0,0,1)
            self.setStepper(0,1,0,1)
            self.setStepper(0,1,1,0)
            self.setStepper(1,0,1,0)
    
    def DownStep(self, cm):
        for i in range(cm * 133):
            self.setStepper(1,0,1,0)
            self.setStepper(0,1,1,0)
            self.setStepper(0,1,0,1)
            self.setStepper(1,0,0,1)

    def UpStepOld(self):
        self.setStepper(1,0,0,1)
        self.setStepper(0,1,0,1)
        self.setStepper(0,1,1,0)
        self.setStepper(1,0,1,0)

    def DownStepOld():
        self.setStepper(1,0,1,0)
        self.setStepper(0,1,1,0)
        self.setStepper(0,1,0,1)
        self.setStepper(1,0,0,1)
        
    def setStepper(in1, in2, in3, in4):
        GPIO.output(self.motor_pin_A1, in1)
        GPIO.output(self.motor_pin_A2, in2)
        GPIO.output(self.motor_pin_B1, in3)
        GPIO.output(self.motor_pin_B2, in4)
        time.sleep(self.delay)

    def destroy(self):
        GPIO.output(self.motor_pin_A1, GPIO.LOW)
        GPIO.output(self.motor_pin_A2, GPIO.LOW)
        GPIO.output(self.motor_pin_B1, GPIO.LOW)
        GPIO.output(self.motor_pin_B2, GPIO.LOW)
        GPIO.cleanup()

    def calibrate():
        while not GPIO.input(calibratePinUp) == HIGH: #important to make a pullup resistance
            UpStepOld()

        if GPIO.input(calibratePinUp) == HIGH:
            calibrateCountSteps = 0

        while not GPIO.input(calibratePinDown) == HIGH: # Important to make a pullup resistance
            DownStepOld()
            calibrateCountSteps += 1

        if GPIO.input(calibratePinDown) == HIGH:
            print("Made all the necessary steps: ", calibrateCountSteps)

        return calibrateCountSteps

if __name__ == '__main__':
    linservo = LinServo([17, 27, 5, 6], [0, 0])

    while True:        
        x =str(input("input[1 = down ; 2 = up]: "))
        y = int(input("Amount in centimeters: "))
        print (x)

        if x == "1":
            print("down")
            linservo.DownStep(y)

        elif x =="2":
            print("up")
            linservo.UpStep(y)
