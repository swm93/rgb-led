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


import RPi.GPIO as GPIO
import json
import re


# load default and user settings, user settings take priority
default_settings = json.loads(open("./settings/default.json").read())
user_settings = json.loads(open("./settings/user.json").read())
settings = dict(default_settings.items() + user_settings.items())


# list of GPIO pins that should be used
pins = settings['pins']

# mapping of colors to their appropriate RGB value
colors = dict(zip(settings['color_names'], settings['color_codes']))

# list of requests that qualify as exit requests
exitReqs = ['exit', 'e']



#   Run
# This is the main function of the script. It creates a loop which waits
# for a users input. When the input is recieved, the multi-color LED is set
# accordingly.

def main():
    # setup the GPIO pins
    GPIO.setmode(GPIO.BOARD)
    for p, n in pins.iteritems():
	n = int(n)
        GPIO.setup(n, GPIO.OUT)
        GPIO.output(n, 1)

    # loop until the user presses ^C
    try:
        while(True):
            req = raw_input("RGB: ")

            if (isExitRequest(req)):
                break

            req = formatRequest(req)

            # update all pins with new values if req is invalid it will be an
            # empty list and nothing will happen
            GPIO.output(int(pins['r']), req[0])
            GPIO.output(int(pins['g']), req[1])
            GPIO.output(int(pins['b']), req[2])

    # user pressed ^C so exit
    #except KeyboardInterrupt:
    finally:
        GPIO.cleanup()
        exit()

    return


#   Format Request
# Accepts a request from the user and converts it into a list containing
# values to achieve the appropriate LED output.
# Example:
#   "yellow" becomes [False, False, True]
#   "010" becomes [True, False, True]

def formatRequest(req):
    val = []

    # request is a color, convert it to RGB
    if (req in colors):
        val = colors[req]
    # request is RGB, don't modify it
    elif (len(req) == 3 and re.match('^[0-1]*$', req)):
        val = req

    # request is valid, flip its bits (low is active)
    if (val):
        val = flipBits(val)

    return val


#   Flip Bits
# Accepts a string of 1s and 0s and returns a list of boolean values
# corresponding to the opposite bit.
# Example:
#   1 becomes False
#   0 becomes True

def flipBits(str):
    val = []

    for c in str:
        val.append(not bool(int(c)))

    return val


#   Is Exit Request
# Returns a boolean value based on whether the request made by the user is an
# exit request or not.

def isExitRequest(req):
    return req in exitReqs


# begin execution
main()
