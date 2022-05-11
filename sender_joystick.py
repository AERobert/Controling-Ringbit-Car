from microbit import *
import radio
from Joystickbit import *
jsb = JOYSTICKBIT(pin0, pin1, pin2)
jsb.last_message = '0,0'
jsb.button_functions = {
'1': '100,100',
'2': '100,-100',
'3': '-100,-100',
'4': '-100,100',
'5': '0,0'}
def constrain_value(value, min, max):
    if value > max: return max
    elif value < min: return min
    else: return value
def vector_to_speeds(distance_supplied, angle_supplied):
    distance = int(distance_supplied)
    angle = int(angle_supplied)
    if angle >= 0 and angle < 90:
        left = distance
        right = mapValue(angle, 0, 89, -distance, distance)
    if angle >= 90 and angle < 180:
        left = mapValue(angle, 90, 179, -distance, distance)
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
while True:
    if not jsb.in_deadzone():
        radio.on()
        radio.send(vector_to_speeds(jsb.get_distance_from_center(), jsb.get_angle_of_joystick()))
        radio.off()
    else:
        radio.on()
        radio.send('0,0')
        radio.off()
    if jsb.button_pressed() != None:
        buttonPressed = jsb.button_pressed()
        if buttonPressed >= 1 and buttonPressed <= 5:
            message = jsb.button_functions[str(buttonPressed)]
            if buttonPressed < 5: jsb.last_message = message
            radio.on()
            radio.send(message)
            radio.off()
        elif buttonPressed == 6:
            radio.on()
            radio.send(jsb.last_message)
            radio.off()
            while jsb.is_pressed(buttonPressed): pass 
