import subprocess

class Funksteckdose():
    def anschalten(self):
        subprocess.call(["./send", "11111", "1", "1"])
    
    def abschalten(self):
        subprocess.call(["./send", "11111", "1", "0"])
