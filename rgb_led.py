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

try:
    import RPi.GPIO as GPIO
    from pwm import PWM
except:
    class PWM:
        def __init__(self, pin_num, pwm_frequency):
            return None
        def ChangeDutyCycle(self, dc):
            return dc
        def start(self, dc):
            return dc
    class GPIO:
        IN = 0
        OUT = 1
        BOARD = 2
        @staticmethod
        def setmode(opt):
            return opt
        @staticmethod
        def setup(pin, io):
            return pin
        @staticmethod
        def PWM(pin, freq):
            return PWM(pin, freq)

import math
import colorsys



class RgbLed:
    pin_names = ('r', 'g', 'b')


    def __init__(self, pins, pwm_frequency):
        GPIO.setmode(GPIO.BOARD)

        self.pwm_frequency = pwm_frequency
        self.pins = dict(zip(self.pin_names, map(self.setup_pin, pins)))


    # RGB color
    def get_rgb_color(self):
        return tuple(round(math.fabs(self.pins[x].duty_cycle * 255.0 / 100.0 - 255.0), 6) for x in self.pin_names)


    def set_rgb_color(self, r, g, b):
        for c, p in self.pins.items():
            dc = math.fabs(locals()[c] * 100.0 / 255.0 - 100.0)
            self.set_duty_cycle(p, dc)


    # HSV color
    def get_hsv_color(self):
        rgb = tuple(x/255.0 for x in self.get_rgb_color())
        hsv = colorsys.rgb_to_hsv(*rgb)
        return (hsv[0]*360.0, hsv[1]*100.0, hsv[2]*100.0)


    def set_hsv_color(self, h, s, v):
        rgb = tuple(x*255.0 for x in colorsys.hsv_to_rgb((h%360)/360.0, s/100.0, v/100.0))
        self.set_rgb_color(*rgb)


    # HLS color
    def get_hsl_color(self):
        rgb = tuple(x/255.0 for x in self.get_rgb_color())
        hls = colorsys.rgb_to_hls(*rgb)
        return (hls[0]*360.0, hls[2]*100.0, hls[1]*100.0)


    def set_hsl_color(self, h, s, l):
        rgb = tuple(x*255.0 for x in colorsys.hls_to_rgb((h%360)/360.0, l/100.0, s/100.0))
        self.set_rgb_color(*rgb)


    # Hex color
    def get_hex_color(self):
        return '#%02x%02x%02x' % self.get_rgb_color()

    def set_hex_color(self, hexc):
        hexc = hexc.lstrip('#')
        lc = len(hexc)
        mx = math.pow(17, (6-lc)/3)
        rgb = (int(hexc[i:i+lc//3], 16)*mx for i in range(0, lc, lc//3))

        self.set_rgb_color(*rgb)


    # Brightness
    def get_brightness(self):
        return self.get_hsl_color()[2]


    def set_brightness(self, brightness):
        hsl = self.get_hsl_color()
        self.set_hsl_color(hsl[0], hsl[1], brightness)


    # Duty Cycle
    def set_duty_cycle(self, pin, duty_cycle):
        pin.duty_cycle = duty_cycle
        pin.ChangeDutyCycle(duty_cycle)


    def setup_pin(self, pin_num):
        GPIO.setup(pin_num, GPIO.OUT)
        pin = PWM(pin_num, self.pwm_frequency)
        self.set_duty_cycle(pin, 100)
        pin.start(100)

        return pin