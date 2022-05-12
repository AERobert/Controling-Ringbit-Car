from microbit import *
import radio
from Joystickbit import *
jsb = JOYSTICKBIT(pin0, pin1, pin2)
jsb.last_button_pressed = '0,0' # variable to contain the instruction of the last pressed dirrectional button
jsb.using = None # stores the last used component of the Joystickbit (iether 'button', 'joystick', or None)
# dictionary containing instructions for what to do after pushing the first five buttons
jsb.button_functions = {
'1': '100,100',
'2': '100,-100',
'3': '-100,-100',
'4': '-100,100',
'5': '0,0'}
# function to constrain a value within a range of avalues
def constrain_value(value, min, max):
    if value > max: return max
    elif value < min: return min
    else: return value
# a function to translate the position of the joystick into a readable speed instruction for the car
def vector_to_speeds(distance_supplied, angle_supplied):
    distance = int(distance_supplied)
    angle = int(angle_supplied)
    if angle >= 0 and angle < 90:
        left = distance
        right = mapValue(angle, 0, 89, -distance, distance)
    if angle >= 90 and angle < 180:
        left = mapValue(angle, 179, 90, -distance, distance)
        right = distance
    elif angle >= 180 and angle < 270:
        left = mapValue(angle, 279, 180, -distance, distance)
        right = -distance
    elif angle >= 270 and angle < 360:
        left = -distance
        right = mapValue(angle, 270, 359, -distance, distance)
    left = constrain_value(int(left), -100, 100)
    right = constrain_value(int(right), -100, 100)
    return str(left)+','+str(right)
while True: # main loop
    if not jsb.in_deadzone(): # do not perform the following if the joystick is currently located within the central deadzone
        jsb.using = 'joystick'
        radio.on() # turn on the radio to send messages
        radio.send(vector_to_speeds(jsb.get_distance_from_center(), jsb.get_angle_of_joystick()))
        radio.off() # Turn off the radio to save memory and power
    else: # perform the following only if the joystick is in its deadzone
        if jsb.using == 'joystick': jsb.using = None  # checks if the joystick was just being used and, if so, records that currently nothing is used
        if jsb.using == None: # do not continue if the car is currently executing a instruction from one of the buttons
            radio.on() # Turn on the radio to send messages
            radio.send('0,0') # send a instruction to stop the car
            radio.off() # turn off the radio to save power and memory
    buttonPressed = jsb.button_pressed() # stores the current button in a variable
    if buttonPressed != None: # continue only if a button is pressed
        jsb.using = 'button' # records that the button is being used
        if buttonPressed >= 1 and buttonPressed <= 5: # continue if the pressed button is one of the first five
            message = jsb.button_functions[str(buttonPressed)] # stores the speed instruction corosponding to the button pressed
            if buttonPressed < 5: jsb.last_button_pressed = message # stores the current instruction if one of the first four buttons are pressed
            radio.on() # turn on the radio to send messages
            radio.send(message) # send the speed instruction stored previusly to the car
            radio.off() # turrn off the radio to save memory and power
        elif buttonPressed == 6: # do the following only if button 6 is pressed
            radio.on() # turn on the radio to send messages
            radio.send(jsb.last_button_pressed) # send the message from the last button pressed
            radio.off() # turns off the radio to save power and memory
            while jsb.is_pressed(buttonPressed): pass  # wait until the button is released
