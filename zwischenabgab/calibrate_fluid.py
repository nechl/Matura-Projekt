import RPi.GPIO as GPIO
import time, sys, datetime
GPIO.setmode(GPIO.BCM)

# it took 16 seconds for 1[L] of water to pass through, the 
inpt = 16

GPIO.setup(inpt, GPIO.IN)
rate_cnt = 0
tot_cnt = 0
minutes = 0
constant = 0.10
time_new = 0.0

try:
    f = open("log_fluidmeter.txt", "a")
except:
    pass

print("Water Flow - Approximate")
print("Control C to exit")

now = datetime.datetime.now()
f.write("\nInit of Flowmeter @ "+ now.strftime("%H:%M:%S - %d.%m.%Y"))

while True:
    time_new = time.time() + 10
    rate_cnt = 0
    while time.time() <= time_new:
        if GPIO.input(inpt) != 0:
            rate_cnt += 1
            tot_cnt += 1
        try:
            print(GPIO.input(inpt), end = "")
            f.write(str(GPIO.input(inpt)))
        except KeyboardInterrupt:
            print("\nCTRL C - Exiting nicely")
            GPIO.cleanup()
            sys.exit()
            f.close()
    minutes += 1
    print("\nLiters / min", round(rate_cnt * constant,4))
    print("Total Liters", round(tot_cnt * constant, 4))
    print("Time (min & clock) ", minutes, "\t", time.asctime(time.localtime(time.time())),"\n")
    f.write("\n")
    f.write("\nLiters / min" + str(rate_cnt))
    f.write("\nTotal Liters" + str(tot_cnt))
    f.write("\nTime (min & clock) "+ str(minutes) + "\t" + str(datetime.datetime.now().strftime("%H:%M:%S - %d.%m.%Y")))
    f.write("\n")
GPIO.cleanup()
print("Done")
f.close()
