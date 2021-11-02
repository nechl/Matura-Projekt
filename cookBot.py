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
    #pinout is the following: 
    #used pins: 17,27,21,20,18,23,24
    
    linservo = LinServo(17,27)
    valve = Valve(21,20)
    salz_streuer = salz_streuer(18)
    funksteckdose = Funksteckdose()
    pastaPortioner = PastaPortioner(23,24)
    temperature = Temperature()

    def __init__(self, name):
        self.name = name
    
    def cook(self, order):
        try:
            print(order)

        #      _  _   _    _  ______          __  _______ ____     _____ ____   ____  _  __
        #    _| || |_| |  | |/ __ \ \        / / |__   __/ __ \   / ____/ __ \ / __ \| |/ /
        #   |_  __  _| |__| | |  | \ \  /\  / /     | | | |  | | | |   | |  | | |  | | ' / 
        #    _| || |_|  __  | |  | |\ \/  \/ /      | | | |  | | | |   | |  | | |  | |  <  
        #   |_  __  _| |  | | |__| | \  /\  /       | | | |__| | | |___| |__| | |__| | . \ 
        #     |_||_| |_|  |_|\____/   \/  \/        |_|  \____/   \_____\____/ \____/|_|\_\

            # 1) let the cooking pot up
            print("Moving the cooking pot up")
            self.linservo.UpStepDistance(20)
            
            # 2) let the water in, based on the amount in the db
            print("Letting water in")
            self.valve.openValveForLiters(2)

            # 3) boil the water
            print("Boil the water")
            self.funksteckdose.anschalten()
            
            while True:
                # 4) Now check if the temperature is already high enough to start cooking the pasta...
                print("Temperatur wird nun alle 30 Sekunden gemessen, sobald sie höher wie 95°C ist wird gekocht.")

                ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
                ser.flush()
                
                if ser.in_waiting < 0:
                    temp = 20
                    print("No number pushed - Waiting")
                    print(temp)
                    
                else:
                    temp = ser.readline().decode('utf-8').rstrip()
                    print(temp)
                        
                
                
                if int(temperature) > 95:

                    # 5) Now salt the pasta:
                    print("[+]Nun wird die Pasta gesalzen.")
                    self.salz_streuer.mahlen()

                    # 6) let the pasta in
                    print("[+]Nun wird die Pasta reingelassen...")
                    self.pastaPortioner.LeftTurn()
                    
                    # 7) let the cooking pot down
                    print("[+]Runterlassen des Kochtopfes...")
                    self.linservo.DownStepDistance(20)
                
                    # 8) wait
                    print("[+]Nun drehen wir Däumchen bis die 500 Sekunden abgelaufen sind...")
                    time.sleep(500)

                    # 9) shut down the funksteckdose
                    print("[+]Nun wird die Steckdose fürs Kochen abgeschaltet...")
                    self.funksteckdose.abschalten()

                    # 10) drive the cooking pot up
                    print("[+]Nun wird der Kochtopf hochgelassen...")
                    self.linservo.UpStepDistance(15)

                    print("[+]Nun sind wir fertig...")
                    break

                else:
                    print(temp)
                time.sleep(5)

        except BaseException as e:
            try:
                self.linservo.destroy()
                self.valve.destroy()
                self.salz_streuer.destroy()
                self.pastaPortioner.destroy()
            except BaseException as e2:
                print(e2)

if __name__ == "__main__":
    cookbot = cookBot("Nechl")
    
    cookbot.cook("nothing yet")
