import pyfirmata
import time
from camera import capture_and_send_image
    
#board = pyfirmata.Arduino('COM6') #change to whatever port you are connected --> windows and mac
board = pyfirmata.Arduino('/dev/ttyACM0') #change to whatever port you are connected --> RPi/Linux (using this for demo)

# start iterator
it = pyfirmata.util.Iterator(board)
it.start()

# connect input pin from LDR module
ldr = board.analog[0]
ldr.enable_reporting()

while True:
    # read LDR sensor
    light = ldr.read()

    # convert value to float type
    if light == None:
        light = 0.0

    # if light detected, trigger camera function
    if light >= 0.5:
        capture_and_send_image()
        time.sleep(299) # wait 5 minutes (299 + 1 seconds = 5 minutes)
    
    time.sleep(1) # run loop every second
    