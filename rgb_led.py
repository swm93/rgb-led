#   RGB LED
#
# This script allows the user to change the color of a multi-color LED
# connected to the GPIO pins of the Raspberry Pi. It assumes that the pins
# that will be used are 11 (red), 13 (green), and 15 (blue). If this is not
# the case, modify the 'pins' list below. The circuit should consist of a
# multi-colored LED wired in series with three resistors: 330 ohms (red), 180
# ohms (green), and 120 ohms (blue). The cathode of the LED should go to 3.3V.
#
# This script and the resistor values were inspired by Gavin MacDonald's video
# 'Controlling an RGB LED with the Raspberry Pi'
# (https://www.youtube.com/watch?v=b4_R1eX9K6s). It is intended to work with
# the BL-L515 LED (http://www.adafruit.com/datasheets/BL-L515.PDF).
#
# Creator:  Scott Mielcarski
# Created:  January 26, 2015
# Modified: January 29, 2015


# import RPi.GPIO as GPIO
import json
import re


hex_color_regex = '^#(?:[0-9a-fA-F]{3}){1,2}$'
list_of_nums_regex = '[0-9]+\s+[0-9]+\s+[0-9]'


# load default and user settings, user settings take priority
default_settings = json.loads(open("./settings/default.json").read())
user_settings = json.loads(open("./settings/user.json").read())
settings = dict(default_settings.items() + user_settings.items())


# list of GPIO pins that should be used
pins = settings['pins']

# mapping of colors to their appropriate RGB value
colors = dict(zip(settings['color_names'], settings['color_codes']))

# frequency of pwm
pwm_frequency = settings['pwm_frequency']



#   Run
# This is the main function of the script. It creates a loop which waits
# for a users input. When the input is recieved, the multi-color LED is set
# accordingly.

def main():
    ports = []

    # setup the GPIO pins
    GPIO.setmode(GPIO.BOARD)
    for n in pins:
        GPIO.setup(n, GPIO.OUT)
        port = GPIO.PWM(n, pwm_frequency)
        port.start(0)
        ports.append(port)

    # loop until the user presses ^C
    try:
        while (True):
            req = raw_input("RGB: ")
            req = format_request(req)

            # update all pins with new values if req is invalid it will be an
            # empty list and nothing will happen
            for (i, v) in enumerate(req):
                ports[i].ChangeDutyCycle(v)

    # user pressed exit so clean up
    finally:
        for p in ports:
            p.stop()
        GPIO.cleanup()
        exit()

    return


#   Format Request
# Accepts a request from the user and converts it into a string containing
# values to achieve the appropriate LED output. Valid requests are color codes
# or color names that are outlined in defaults.json.
# Example:
#   "yellow" becomes "001"
#   "010" becomes "101"
#   "123" or "fish" becomes ""

def format_request(req):
    val = ""

    # request is a color, use lookup table to convert it to list
    if (isinstance(req, str) and req in colors):
        val = colors[req]
    # request is hex color, needs to be parsed and put in list
    elif (isinstance(req, str) and re.match(hex_color_regex, req)):
        req = req.lstrip('#')
        lv = len(req)
        mx = math.pow(17, (6-lv)/3)
        val = [int(req[i:i + lv // 3], 16)*mx for i in range(0, lv, lv // 3)]
    # request is a string of numbers, needs to be split into list
    elif (isinstance(req, str) and re.match(list_of_nums_regex, req)):
        req = re.split('\s+', req)
        val = [int(s) for s in req if (s.isdigit())]
    # request is a list, therefore it came from json file (formatted
    # correctly)
    elif (isinstance(req, list) and len(req) == 3):
        val = req

    # request is valid, flip its bits (low is active)
    # if (val):
        # val = flip_bits(val)

    return val


#   Flip Bits
# Accepts a string of 1s and 0s and returns a list of boolean values
# corresponding to the opposite bit.
# Warning:
#   This function does not validate that the string contains only 1s and 0s,
#   and will produce a strange output in the case that the string contains an
#   alternate value.
# Example:
#   1 becomes 0
#   0 becomes 1

def flip_bits(bits):
    def flip(x):
        return str(-(int(x)) + 1)

    return ''.join(map(str, map(flip, bits)))



# begin execution
# main()
