try:
    import RPi.GPIO as GPIO
    import time
except ModuleNotFoundError:
    print("Not all modules required were found...")

from linservo import LinServo
from valve import Valve

class cookBot():
    linservo = LinServo([17, 27, 5, 6], [0, 0])
    valve = Valve([21,20])

    def __init__(self, name):
        self.name = name
    
    def cook(self, order):
        print(order)

        #HOW TO COOK: 
        # 1) let the cooking pot up
        self.linservo.UpStep(1)

        # 2) let the water in, based on the amount in the db

        self.valve.openValveForLiters(2)

        # 3) boil the water

        # 4) let the pasta in

        # 5) wait
        time.sleep(600)
        # 6) let the cooking pot down
        self.linservo.DownStep(1)
