import subprocess

while True:
    x = int(input("Anschalten[1] oder Abschalten[0] der Funksteckdose"))
    if x== 1:
        subprocess.call(["./send", "11111", "1", "1"])
    elif x == 0:
        subprocess.call(["./send", "11111", "1", "0"])
    else:
        pass
