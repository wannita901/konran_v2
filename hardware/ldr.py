import RPi.GPIO as GPIO

#set GPIO numbering
GPIO.setmode(GPIO.BCM)

#set input at GPIO4
GPIO.setup(4, GPIO.IN)

for i in range(0,5):
    print GPIO.input(4)
