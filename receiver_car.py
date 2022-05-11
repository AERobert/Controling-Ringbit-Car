from microbit import *
import radio
from Ringbit import *
rb = RINGBIT(pin1, pin2)
radio.on()
while True:
    nextMessage = radio.receive()
    if nextMessage != None:
        speeds =  nextMessage.split(',')
        rb.set_motors_speed(int(speeds[0]), int(speeds[1]))
