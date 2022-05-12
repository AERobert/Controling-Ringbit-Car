from microbit import *
import math

# three math functions needed for parts of the class

# function to map a value from a given range to a given range (Translated from Arduino's map() function)
def mapValue(x, in_min, in_max, out_min, out_max):
    return int((x-in_min)*(out_max-out_min)/(in_max-in_min)+out_min)

# find the distance between two points on a cartesian plain.
def find_distance(a, b):
    return abs(math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2))

# find the angle of a point in a circle (relitive to the positive x-axis)
def get_angle_on_circle(a, b):
    (dx,dy) =( b[0]-a[0], b[1]-a[1])
    return math.degrees(math.atan2(dy, dx))+180

# class to represent a Joystickbit V1
class JOYSTICKBIT:
    #initialize the class with the propper pin assignments
    def __init__(self, x_pin=pin0, y_pin=pin1, button_pin=pin2):
        self.__x_pin = x_pin
        self.__y_pin = y_pin
        self.__button_pin = button_pin
    mapped_radius = 100 # variable which represents the radius of the circle to be mapped on to
    deadzone_ratio = 0.1 # The size of the centeral deadzone as compared to the overall size of the mapped circle
    # function to get the analog value on the x-axis rocker
    def get_analog_x(self):
        return self.__x_pin.read_analog()
 # function to get an anlog reading from the y-axis rocker
    def get_analog_y(self):
        return self.__y_pin.read_analog()
     # function to get a list containing the analog readings from both the x and y rockers.
    def get_analog_xy(self):
        return [self.get_analog_x(), self.get_analog_y()]
    # function to get the value of x as mapped on a circle.
    def get_x(self):
        return mapValue(self.get_analog_x(), 0, 1023, self.mapped_radius, (-1)*self.mapped_radius)
    # function to get the value of y as mapped on a circle.
    def get_y(self):
        return mapValue(self.get_analog_y(), 0, 1023, self.mapped_radius, (-1)*self.mapped_radius)
    # function to get a list containing the mapped values for x and y.
    def get_xy(self):
        return [self.get_x(),self.get_y()]
    # function get the current distance of the joystick from the center of the mapped circle.
    def get_distance_from_center(self):
        return find_distance([0,0], self.get_xy())
    # get the angle of the joystick around the mapped circle (relitive to the rightwards positive x-axis)
    def get_angle_of_joystick(self):
        return get_angle_on_circle([0,0], self.get_xy())
    # function to determine if the joystick is currently positioned within its centeral deadzone
    def in_deadzone(self):
        deadzone_radius= self.mapped_radius*self.deadzone_ratio
        if self.get_distance_from_center() <= deadzone_radius: return True
        else: return False
    # returns the number of the button that is currently pressed or None if no button is pressed
    def button_pressed(self):
        buttonVal = self.__button_pin.read_analog()
        if buttonVal < 256:
            return 1
        if buttonVal < 597:
            return 2
        if buttonVal < 725:
            return 3
        if buttonVal < 793:
            return 4
        if buttonVal < 836:
            return 5
        if buttonVal < 938:
            return 6
        else:
            return None 
    # returns True if the given button is pressed
    def is_pressed(self, button):
        if self.button_pressed() == button:
            return True
        else:
            return False
