try:
    import RPi.GPIO as GPIO
    import time
except ModuleNotFoundError as error:
    print(error)

step = 23
dir1 = 24
class PastaPortioner():
    def __init__(self, step, dir1):
        self.step = step
        self.dir1 = dir1
        self.delay = 0.0001

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.step, GPIO.OUT)
        GPIO.setup(self.dir1, GPIO.OUT)

    def turn(self):
        GPIO.output(self.dir1, GPIO.LOW)

        for i in range(int(13 * (grams/100))):
            GPIO.output(self.step, GPIO.LOW)
            time.sleep(self.delay)
            GPIO.output(self.step, GPIO.HIGH)
            time.sleep(self.delay)
        GPIO.output(self.dir1, GPIO.HIGH)
        for i in range(int(13 * (grams/100))):
            GPIO.output(self.step, GPIO.LOW)
            time.sleep(self.delay)
            GPIO.output(self.step, GPIO.HIGH)
            time.sleep(self.delay)

   
    def LeftTurnGram(self, grams):
        for i in range(int(13 * (grams/100))):
            
            GPIO.output(self.dir1, GPIO.HIGH)
            for i in range(2000):
                GPIO.output(self.step, GPIO.LOW)
                time.sleep(self.delay)
                GPIO.output(self.step, GPIO.HIGH)
                time.sleep(self.delay)

            GPIO.output(self.dir1, GPIO.LOW)
            for i in range(1000):
                GPIO.output(self.step, GPIO.LOW)
                time.sleep(self.delay)
                GPIO.output(self.step, GPIO.HIGH)
                time.sleep(self.delay)
    def configure(self):
        l = 0
        for i in range(10):
            GPIO.output(self.dir1, GPIO.LOW)

            for i in range(1000):
                GPIO.output(self.step, GPIO.LOW)
                time.sleep(self.delay)
                GPIO.output(self.step, GPIO.HIGH)
                time.sleep(self.delay)
            GPIO.output(self.dir1, GPIO.HIGH)
            for i in range(1000):
                GPIO.output(self.step, GPIO.LOW)
                time.sleep(self.delay)
                GPIO.output(self.step, GPIO.HIGH)
                time.sleep(self.delay)

            menge = int(input("How many grams were that? "))
            l += menge
        gramm_pro_umdrehung = l/20000
        umdrehung_pro_50_gramm = (20000 / l) * 50
        print(umdrehung_pro_50_gramm)

    def destroy(self):
        GPIO.output(self.dir1, GPIO.LOW)
        GPIO.output(self.step, GPIO.LOW)
        GPIO.cleanup()

if __name__ == "__main__":
    pasta_port = PastaPortioner(23, 24)
    #pasta_port.configure()
    try:
        while True:
            x = int(input("Pasta, yk, oder configure[2]"))
            if x==1:
                pasta_port.turn()
            elif x==2:
                pasta_port.configure()
            elif x==3:
                pasta_port.LeftTurnGram(50)
    except KeyboardInterrupt as e:
        print(e)
