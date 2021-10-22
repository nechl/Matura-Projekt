try:
    import RPi.GPIO as GPIO
    import time
except ModuleNotFoundError as error:
    print(error)

salz_pin = 18

delay = 0.0001

class salz_streuer():
    def __init__(self, salz_pin):
        self.salz_pin = salz_pin
	
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.salz_pin, GPIO.OUT)
        
    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.salz_pin, GPIO.OUT)

    def mahlen(self):
        GPIO.output(self.salz_pin, GPIO.HIGH)
        time.sleep(5)
        GPIO.output(self.salz_pin, GPIO.LOW)
        
    def destroy(self):
        GPIO.output(self.salz_pin, GPIO.LOW)
        GPIO.cleanup()
    
if __name__ == "__main__":
    salz_streuer = salz_streuer(salz_pin)
    while True:
        try:
            x = input("Up[1] or down[2]: ")
            salz_streuer.mahlen() if x == "1" else print("nothing")
        except KeyboardInterrupt:
            motor_shield.destroy()
            pass
