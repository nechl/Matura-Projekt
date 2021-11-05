try:
    import RPi.GPIO as GPIO
    import time
except ModuleNotFoundError as error:
    print(error)
step = 21
dir1 = 12

delay = 0.0001
class motor_shield():
    def __init__(self, step, dir1):
        self.step = step
        self.dir1 = dir1
	
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.step, GPIO.OUT)
        GPIO.setup(self.dir1, GPIO.OUT)

    def DownStep(self):
        GPIO.output(self.dir1, GPIO.LOW)

        for i in range(10000):
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

    def destroy(self):
        GPIO.output(self.dir1, GPIO.LOW)
        GPIO.output(self.step, GPIO.LOW)
        GPIO.cleanup()
    
if __name__ == "__main__":
    motor_shield = motor_shield(step, dir1)
    while True:
        try:
            x = input("Up[1] or down[2]: ")
            motor_shield.UpStep() if x == "1" else motor_shield.DownStep()
        except KeyboardInterrupt:
            motor_shield.destroy()
            pass
