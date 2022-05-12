from microbit import *
import radio
from Ringbit import *
rb = RINGBIT(pin1, pin2) # initializes a  Joystickbi objectt
radio.on() # turns on the radio functionality to recieve instructions
while True: # main loop to recieve and execute radio instructions
    nextMessage = radio.receive() # variable containing the next message on the queue
    if nextMessage != None: # do not continue if the queue contains no messages
        speeds =  nextMessage.split(',') # break the instruction into speeds for the left and right wheels
        rb.set_motors_speed(int(speeds[0]), int(speeds[1])) # set the motors to the speeds in the instruction
