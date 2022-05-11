from microbit import *
import math

# three math functions needed for parts of the class
def mapValue(x, in_min, in_max, out_min, out_max):
    return int((x-in_min)*(out_max-out_min)/(in_max-in_min)+out_min)

def find_distance(a, b):
    return abs(math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2))

def get_angle_on_circle(a, b):
    (dx,dy) =( b[0]-a[0], b[1]-a[1])
    return math.degrees(math.atan2(dy, dx))

# class to represent a Joystickbit V1
class JOYSTICKBIT:
    def __init__(self, x_pin, y_pin, button_pin):
        self.__x_pin = x_pin
        self.__y_pin = y_pin
        self.__button_pin = button_pin
    mapped_diameter = 100
    deadzone_ratio = 0.1
    def get_analog_x(self):
        return self.__x_pin.read_analog()
    def get_analog_y(self):
        return self.__y_pin.read_analog()
    def get_analog_xy(self):
        return [self.get_analog_x(), self.get_analog_y()]
    def get_x(self):
        return mapValue(self.get_analog_x(), 0, 1023, self.mapped_diameter, (-1)*self.mapped_diameter)
    def get_y(self):
        return mapValue(self.get_analog_y(), 0, 1023, self.mapped_diameter, (-1)*self.mapped_diameter)
    def get_xy(self):
        return [self.get_x(),self.get_y()]
    def get_distance_from_center(self):
        return find_distance([0,0], self.get_xy())
    def get_angle_of_joystick(self):
        return get_angle_on_circle([0,0], self.get_xy())+180
    def in_deadzone(self):
        deadzone_diameter= self.mapped_diameter*self.deadzone_ratio
        if self.get_distance_from_center() <= deadzone_diameter: return True
        else: return False
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
    def is_pressed(self, button):
        if self.button_pressed() == button:
            return True
        else:
            return False
