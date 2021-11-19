#!/usr/bin/env python3
import json
import serial
import time
from datetime import datetime, timedelta

from app.models import Order
from app import app, db
class CookBot():
    #import app, db

    try:
        import RPi.GPIO as GPIO
        import time
        import serial
        import os
        import json
        
        from physical.linservo import LinServo
        from physical.valve import Valve
        from physical.salzstreuer import salz_streuer
        from physical.funksteckdose import Funksteckdose
        from physical.pastaPortioner import PastaPortioner
        #from physical.temperatur import Temperature
        GPIO.setwarnings(False)
        
    except ModuleNotFoundError as e:
        print(e)
    import json
    import serial
    #pinout is the following: 
    #used pins: 17,27,21,20,18,23,24
    
    linservo = LinServo(27,22)
    valve = Valve(21,20)
    salz_streuer = salz_streuer(18)
    funksteckdose = Funksteckdose()
    pastaPortioner = PastaPortioner(23,24)
    #temperature = Temperature()

    def __init__(self, name):
        self.name = name
    
    def cook(self, order):
        try:
            print(order)
            #log_file = open("log_file.txt", "a")
            #log_file.write(str("Order: ", str(order)))
            #Change atrribute in database to cooking, so that you know that it is in preparation.

            order.cooking = True
            db.session.add(order)
            db.session.commit()
            
            # Opening JSON file
            #f = open('data_recipe.json',)
        
            # returns JSON object as 
            # a dictionary
            #data = json.load(f)
            
            # Iterating through the json
            # list
            #for recipe in data['recipes']:
            #    if recipe["compound"] == order.food:
            #        TimeToCook = (recipe["time_in_water"])
            #        water_amount_per_1000_g = (recipe["water_amount_per_1000_g"])
            #        print(TimeToCook)
            #        print(water_amount_per_1000_g)
            TimeToCook =10
            water_amount_per_1000_g = 2

            # Closing file
            #f.close()
            #HOW TO COOK

            # 1) let the cooking pot up
            print(self.name, ": Moving the cooking pot up")
            self.linservo.UpStepDistance(5)
            
            # 2) let the water in, based on the amount in the db
            print(self.name, ": Letting water in")
            #self.valve.openValveForLiters(order.amount/1000 * water_amount_per_1000_g)
            x = int(input("testing[0] or real[1]?"))
            if x == 1:
                self.valve.openValveForLiters(water_amount_per_1000_g)
            else:
                pass
            # 3) boil the water
            print(self.name, ": Boil the water")
            self.funksteckdose.anschalten()
            temp = 20.0
            ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
            ser.flush()
            while True:
                # 4) Now check if the temperature is already high enough to start cooking the pasta...
           
                if ser.in_waiting > 0:
                    temp = ser.readline().decode('utf-8').rstrip()
                    
                    try:
                        temp = float(temp)  
                        print(str(temp))
                        print(temp)  
                    except ValueError as e:
                        #write(str(datetime.now().strftime("[" , str(order.id), "]: " ,"%H:%M:%S, %d.%m.%Y occured an error: "),str(e)))
                        pass


                try:
                    if temp != '' and float(temp) > 85.0:

                        # 5) Now salt the water:
                        print("[+]",self.name, ": Nun wird die Pasta gesalzen.")
                        self.salz_streuer.mahlen()

                        # 6) let the pasta in
                        print("[+]",self.name, ": Nun wird die Pasta reingelassen...")
                        self.pastaPortioner.LeftTurnGram(order.amount)
                        
                        # 7) let the cooking pot down
                        print("[+]",self.name, ": Runterlassen des Kochtopfes...")
                        self.linservo.DownStepDistance(20)
                    
                        # 8) wait
                        print("[+]",self.name, ": Nun drehen wir Däumchen bis die "+ str(TimeToCook) +" Sekunden abgelaufen sind...")
                        print("[" , str(order.id), "]: " ,"Wird um ", (datetime.now()+timedelta(minutes = 10)).strftime("%H:%M:%S, %d.%m.%Y"), " beendet.")
                        time.sleep(TimeToCook*60)


                        # 9) shut down the funksteckdose
                        print("[+]",self.name, ": Nun wird die Steckdose fürs Kochen abgeschaltet...")
                        self.funksteckdose.abschalten()

                        # 10) drive the cooking pot up
                        print("[+]",self.name, ": Nun wird der Kochtopf hochgelassen...")
                        self.linservo.UpStepDistance(20)

                        print("[+]",self.name, ": Nun sind wir fertig...")
                        break
                except ValueError as e:
                    #log_file.write(str(datetime.now().strftime("%H:%M:S, %d.%m.%Y occured an error: "),str(e)))
                    pass
            
                

        except KeyboardInterrupt as e:
            pass
            #log_file.write(str("[" , str(order.id), "]: " ,datetime.now().strftime("%H:%M:%S, %d.%m.%Y occured an error: "),str(e)))
            try:
                print("[+]","Okay, we have a problem, shutting services down")
                self.funksteckdose.abschalten()
                print(e)
                self.linservo.destroy()
                self.valve.destroy()
                self.salz_streuer.destroy()
                self.pastaPortioner.destroy()
                
            except BaseException as e2:
                print(e2)
                #log_file.write(str("[" , str(order.id), "]"  ,datetime.now().strftime("%H:%M:%S, %d.%m.%Y occured an error: "),str(e2)))
            #log_file.write("--------------")
            #log_file.close()

if __name__ == "__main__":
    cookbot = CookBot("Rata")
