import subprocess
class Funksteckdose():
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
    
    def anschalten(self):
        subprocess.run("./send", args="11111 1 1")
    
    def abschalten(self):
        subprocess.run("./send", args="11111 1 0")