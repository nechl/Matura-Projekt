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

            #HOW TO COOK: 
            
            # 1) let the cooking pot up
            print("Moving the cooking pot up")
            self.linservo.UpStep()
            
            # 2) let the water in, based on the amount in the db
            print("Letting water in")
            self.valve.openValveForLiters(2)

            # 3) boil the water
            print("Boil the water")
            self.funksteckdose.anschalten()
            
            while True:
                temperature = self.temperature.listenSerial()
                ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
                ser.flush()
                
                if ser.in_waiting < 0:
                    temp = 20
                    print(temp)
                    
                else:
                    temp = ser.readline().decode('utf-8').rstrip()
                    print(temp)
                        
                # 4) Now check if the temperature is already high enough to start cooking the pasta...
                print("Temperatur wird nun alle 30 Sekunden gemessen, sobald sie höher wie 90°C ist wird gekocht.")

                if float(temp) > 50.0:
                    # 5) Now salt the pasta:
                    print("Nun wird die Pasta gesalzen.")
                    self.salz_streuer.mahlen()

                    # 6) let the pasta in
                    print("Nun wird die Pasta reingelassen...")
                    self.pastaPortioner.LeftTurn()
                    
                    # 7) let the cooking pot down
                    print("Runterlassen des Kochtopfes...")
                    self.linservo.DownStep()
                
                    # 8) wait
                    print("Nun drehen wir Däumchen bis die 300 Sekunden abgelaufen sind...")
                    time.sleep(300)

                    # 9) shut off the funksteckdose
                    print("Nun wird die Steckdose fürs Kochen abgeschaltet...")
                    self.funksteckdose.abschalten()

                    # 10) drive the cooking pot up
                    print("Nun wird der Kochtopf hochgelassen...")
                    self.linservo.UpStep()

                    print("Nun sind wir fertig...")
                    break
                else:
                    print(temp)
                    print("We are not in the correct loop, guess why")
                time.sleep(5)
        except BaseException as e:
            self.linservo.destroy()
            self.valve.destroy()
            self.salz_streuer.destroy()
            self.pastaPortioner.destroy()

if __name__ == "__main__":
    cookbot = cookBot("Nechl")
    
    cookbot.cook("nothing yet")
