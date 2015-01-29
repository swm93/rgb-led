# RGB LED

RGB LED is a simple python script that allows a multicolor LED to be controlled using a Raspberry Pi. The script is written for and is intended to work with the Diffused RGB (tri-color) LED from Adafruit (http://www.adafruit.com/product/159); however, other simillar LEDs will likely work as well. The following color modes are supported: red, yellow, green, teal, blue, purple, white, off.

This script was inspired by Gavin MacDonalds video 'Controlling an RGB LED with the Raspberry Pi': https://www.youtube.com/watch?v=b4_R1eX9K6s.

## Getting Started

The script is intended to be run from the command line, so once the circuit is built, boot up the Pi and navigate to the directory where the rgb_led.py file exists. Run the python script by typing: ```python rgb_led.py```. The script should now be running! If everything is set up correctly you should now be able to set the color of the LED by typing one of the following colors or color codes followed by the return key.

Color Names | Color Codes
:-----------|-----------:
off         |000
red         |001
green       |010
yellow      |011
blue        |100
purple      |101
teal        |110
white       |111

## The Circuit

In order to build the circuit the following parts are required:
* 1x Raspberry Pi
* 1x Multi-color LED
* 3x Resistor (must meet the specs outlined on the LED datasheet)

I chose to use [Round Type, FULL COLOR LED lamp BL-L515](http://www.adafruit.com/product/159) from Adafruit, and 330Ω, 180Ω, and 120Ω resistors purchased from Amazon.

It is assumed that GPIO pins 11, 13, and 15 will be used for the red, green, and blue pins, respectively, of the LED. Unfortunately, there is no way to change this at the moment without modifying the python script. If you would like to do so, look for where the 'pins' array is initialized. The first number in the array corresponds to the GPIO pin to be used with the red LED pin, the second is for the green pin, and the third is for the blue pin.

### Schematic
![Schematic](https://raw.githubusercontent.com/swm93/rgb-led/master/images/schematic.png)

### Breadboard
![Breadboard](https://raw.githubusercontent.com/swm93/rgb-led/master/images/breadboard.png)
