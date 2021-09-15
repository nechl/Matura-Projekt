# import all required libraries
try:
    import RPi.GPIO as GPIO
    import time
except ModuleNotFoundError:
    print("Not all modules required were found...")

motor_pin_A1 = 21
motor_pin_A2 = 12

calibratePinUp = 0
calibratePinDown = 0
delay = 0.02
# old delay 0.01
def setup():
    global motor_pin_A1, motor_pin_A2, motor_pin_B1, motor_pin_B2
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(motor_pin_A1, GPIO.OUT)
    GPIO.setup(motor_pin_A2, GPIO.OUT)

def UpStep(cm):
        
def DownStep(cm):

def UpStepOld():

def DownStepOld():
    
def setStepper(in1, in2):
    GPIO.output(motor_pin_A1, in1)
    GPIO.output(motor_pin_A2, in2)
    time.sleep(delay)

def calcStart():
    while not GPIO.input(calibratePinUp) ==GPIO. HIGH: #important to make a pullup resistance
        UpStepOld()

    if GPIO.input(calibratePinUp) ==GPIO. HIGH:
        calibrateCountSteps = 0

    while not GPIO.input(calibratePinDown) == GPIO.HIGH: # Important to make a pullup resistance
        DownStepOld()
        calibrateCountSteps += 1

    if GPIO.input(calibratePinDown) ==GPIO. HIGH:
        print("Made all the necessary steps: ", calibrateCountSteps)
    
    return calibrateCountSteps
    
def loop():
    while True:        
        x =str(input("input[1 = down ; 2 = up]: "))
        y = int(input("Amount in centimeters: "))
        print (x)

        if x == "1":
            print("down")
            DownStep(y)

        elif x =="2":
            print("up")
            UpStep(y)        

def destroy():
    GPIO.output(motor_pin_A1, GPIO.LOW)
    GPIO.output(motor_pin_A2, GPIO.LOW)
    GPIO.output(motor_pin_B1, GPIO.LOW)
    GPIO.output(motor_pin_B2, GPIO.LOW)
    GPIO.cleanup()

if __name__ == '__main__':
    setup()
    #heightInSteps = calcStart()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
