try:
    import RPi.GPIO as GPIO
    import time
except ModuleNotFoundError as error:
    print(error)


class PastaPortioner():
    def __init__(self, step, dir1):
        self.step = step
        self.dir1 = dir1
        self.delay = 0.0001

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.step, GPIO.OUT)
        GPIO.setup(self.dir1, GPIO.OUT)

    def RightTurn(self):
        GPIO.output(self.dir1, GPIO.LOW)

        for i in range(10000):
            GPIO.output(self.step, GPIO.LOW)
            time.sleep(self.delay)
            GPIO.output(self.step, GPIO.HIGH)
            time.sleep(self.delay)

    def LeftTurn(self):
        GPIO.output(self.dir1, GPIO.HIGH)
        
        for i in range(10000):
            GPIO.output(self.step, GPIO.LOW)
            time.sleep(self.delay)
            GPIO.output(self.step, GPIO.HIGH)
            time.sleep(self.delay)

    def destroy(self):
        GPIO.output(self.dir1, GPIO.LOW)
        GPIO.output(self.step, GPIO.LOW)
        GPIO.cleanup()