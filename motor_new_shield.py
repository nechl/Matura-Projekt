try:
    import RPi.GPIO as GPIO
    import time
except ModuleNotFoundError as error:
    print(error)
step = 21
dir = 12
class motor_shield():
    def __init__(self, step, dir):
        self.step = step
        self.dir = dir

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.step, GPIO.OUT)
        GPIO.setup(self.dir, GPIO.OUT)

    def DownStep(self):
        GPIO.output(self.dir, GPIO.LOW)

        for i in range(100):
            GPIO.output(self.step, GPIO.LOW)
            time.sleep(0.01)
            GPIO.output(self.step, GPIO.HIGH)
            time.sleep(0.01)

    def UpStep(self):
        GPIO.output(self.dir, GPIO.HIGH)
        
        for i in range(100):
            GPIO.output(self.step, GPIO.LOW)
            time.sleep(0.01)
            GPIO.output(self.step, GPIO.HIGH)
            time.sleep(0.01)

    def destroy(self):
        GPIO.output(self.dir, GPIO.LOW)
        GPIO.output(self.step, GPIO.LOW)
        GPIO.cleanup()
    
if __name__ == "__main__":
    motor_shield = motor_shield(step, dir)
    while True:
        x = input("Up[1] or down[2]: ")
        motor_shield.UpStep() if x == "1" else motor_shield.DownStep()