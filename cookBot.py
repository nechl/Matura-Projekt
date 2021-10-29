#!/usr/bin/env python3
try:
    import RPi.GPIO as GPIO
    import time
    import serial
    import os
    from linservo import LinServo
    from valve import Valve
    from salzstreuer import salz_streuer
    from funksteckdose import Funksteckdose
    from pastaPortioner import PastaPortioner
    from temperatur import Temperature
except ModuleNotFoundError:
    print("Not all modules required were found...")



class cookBot():
    linservo = LinServo([17, 27, 5, 6], [0, 0])
    valve = Valve([21,20])
    salz_streuer = salz_streuer(18)
    funksteckdose = Funksteckdose(pin)
    pastaPortioner = PastaPortioner(pin1, pin2)
    temperature = Temperature()

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
        self.funksteckdose.anschalten()
        
        while True:
            temperature = self.temperature.listenSerial()
            
            # 4) Now check if the temperature is already high enough to start cooking the pasta...
            if temperature > 90:
                # 5) Now salt the pasta:
                self.salz_streuer.mahlen()

                # 6) let the pasta in
                self.pastaPortioner.LeftTurn()
                
                # 7) let the cooking pot down
                self.linservo.DownStep(1)
            
                # 8) wait
                time.sleep(500)

                # 9) shut off the funksteckdose
                self.funksteckdose.abschalten()

                # 10) drive the cooking pot up
                self.linservo.UpStep(3)

                break

if __name__ == "__main__":
    cookbot = cookBot("Nechl")
    
    cookbot.cook("nothing yet")