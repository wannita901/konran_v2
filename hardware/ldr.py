import pyfirmata
import time
from camera import capture_and_send_image
    
#board = pyfirmata.Arduino('COM6') #change to whatever port you are connected --> windows and mac
board = pyfirmata.Arduino('/dev/ttyACM0') #change to whatever port you are connected --> RPi (using this for demo)

it = pyfirmata.util.Iterator(board)
it.start()

ldr = board.analog[0]
ldr.enable_reporting()

while True:
    light = ldr.read()

    if light == None:
        light = 0.0

    if light >= 0.5:
        capture_and_send_image()
        exit()
    
    time.sleep(1)
    