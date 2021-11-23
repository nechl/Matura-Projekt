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

    def mahlen(self):
        GPIO.output(self.salz_pin, GPIO.HIGH)
        time.sleep(15)
        GPIO.output(self.salz_pin, GPIO.LOW)
        
    def destroy(self):
        GPIO.output(self.salz_pin, GPIO.LOW)
        GPIO.cleanup()
    
if __name__ == "__main__":
    salz_streuer = salz_streuer(18)
    while True:
        try:
            x = input("Mahlen[1] oder nichts tun... ")
            if x == "1":
                salz_streuer.mahlen()
		
        except KeyboardInterrupt:
            salz_streuer.destroy()
            pass
