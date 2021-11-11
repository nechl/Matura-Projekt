#!/usr/bin/env python3
import json
class CookBot():
    try:
        from app import app, db
        from app.models import Order

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
        from physical.temperatur import Temperature
        
    except ModuleNotFoundError as e:
        print(e)
    import json
    #pinout is the following: 
    #used pins: 17,27,21,20,18,23,24
    
    linservo = LinServo(27,22)
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
            #Change atrribute in database to cooking, so that you know that it is in preparation.
            #order_to_edit = Order.query.filter_by(id=order.id).first_or_404()
            #order_to_edit.cooking = True
            #db.session.add(order_to_edit)
            #db.session.commit()
            # Opening JSON file
            f = open('data_recipe.json',)
        
            # returns JSON object as 
            # a dictionary
            data = json.load(f)
            
            # Iterating through the json
            # list
            for recipe in data['recipes']:
                if recipe["compound"] == order.food:
                    TimeToCook = (recipe["time_in_water"])
                    water_amount_per_1000_g = (recipe["water_amount_per_1000_g"])
                    print(TimeToCook)
                    print(water_amount_per_1000_g)
        
            # Closing file
            f.close()
            
            #HOW TO COOK

            # 1) let the cooking pot up
            print(self.name, ": Moving the cooking pot up")
            self.linservo.UpStepDistance(5)
            
            # 2) let the water in, based on the amount in the db
            print(self.name, ": Letting water in")
            #self.valve.openValveForLiters(order.amount/1000 * water_amount_per_1000_g)
            self.valve.openValveForLiters(3.5)
            # 3) boil the water
            print(self.name, ": Boil the water")
            self.funksteckdose.anschalten()
            
            while True:
                # 4) Now check if the temperature is already high enough to start cooking the pasta...
                print("[+]",self.name, ": Temperatur wird nun alle 30 Sekunden gemessen, sobald sie höher wie 95°C ist wird gekocht.")

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
                    print("[+]",self.name, ": Nun wird die Pasta gesalzen.")
                    self.salz_streuer.mahlen()

                    # 6) let the pasta in
                    print("[+]",self.name, ": Nun wird die Pasta reingelassen...")
                    self.pastaPortioner.LeftTurnGram(order.amount)
                    
                    # 7) let the cooking pot down
                    print("[+]",self.name, ": Runterlassen des Kochtopfes...")
                    self.linservo.DownStepDistance(15)
                
                    # 8) wait
                    print("[+]",self.name, ": Nun drehen wir Däumchen bis die 500 Sekunden abgelaufen sind...")
                    time.sleep(TimeToCook*60)

                    # 9) shut down the funksteckdose
                    print("[+]",self.name, ": Nun wird die Steckdose fürs Kochen abgeschaltet...")
                    self.funksteckdose.abschalten()

                    # 10) drive the cooking pot up
                    print("[+]",self.name, ": Nun wird der Kochtopf hochgelassen...")
                    self.linservo.UpStepDistance(15)

                    print("[+]",self.name, ": Nun sind wir fertig...")
                    break

                else:
                    print("[+]",self.name, ":  ", temp)
                time.sleep(5)

        except BaseException as e:
            try:
                print("[+]","Okay, we have a problem, shutting services down")
                print(e)
                self.linservo.destroy()
                self.valve.destroy()
                self.salz_streuer.destroy()
                self.pastaPortioner.destroy()
            except BaseException as e2:
                print(e2)

if __name__ == "__main__":
    cookbot = CookBot("Rata")
    order= 