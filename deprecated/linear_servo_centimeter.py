# import all required libraries
try:
    import RPi.GPIO as GPIO
    import time
except ModuleNotFoundError:
    print("Not all modules required were found...")
motor_pin_A1 = 17
motor_pin_A2 = 27

motor_pin_B1 = 5
motor_pin_B2 = 6

delay = 0.01
# old delay 0.01
def setup():
    global motor_pin_A1, motor_pin_A2, motor_pin_B1, motor_pin_B2
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(motor_pin_A1, GPIO.OUT)
    GPIO.setup(motor_pin_A2, GPIO.OUT)
    GPIO.setup(motor_pin_B1, GPIO.OUT)
    GPIO.setup(motor_pin_B2, GPIO.OUT)
        
def DownStep(cm):
    for i in range(cm * 133):
        setStepper(1,0,1,0)
        setStepper(0,1,1,0)
        setStepper(0,1,0,1)
        setStepper(1,0,0,1)

def UpStep(cm):
    for i in range(cm * 133):
        setStepper(1,0,0,1)
        setStepper(0,1,0,1)
        setStepper(0,1,1,0)
        setStepper(1,0,1,0)
    
def setStepper(in1, in2, in3, in4):
    GPIO.output(motor_pin_A1, in1)
    GPIO.output(motor_pin_A2, in2)
    GPIO.output(motor_pin_B1, in3)
    GPIO.output(motor_pin_B2, in4)
    time.sleep(delay)

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
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
