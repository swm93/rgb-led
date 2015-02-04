# RGB LED

RGB LED is a simple python script that allows a multicolor LED to be controlled using a Raspberry Pi. The script is written for and is intended to work with the Diffused RGB (tri-color) LED from Adafruit (http://www.adafruit.com/product/159); however, other simillar LEDs will likely work as well. The following color modes are supported: red, yellow, green, teal, blue, purple, white, off.

This script was inspired by Gavin MacDonalds video 'Controlling an RGB LED with the Raspberry Pi': https://www.youtube.com/watch?v=b4_R1eX9K6s.

## Getting Started

The script is intended to be run from the command line, so once the circuit is built, boot up the Pi and navigate to the directory where the rgb_led.py file exists. Run the python script by typing: ```python rgb_led.py```. The script should now be running! If everything is set up correctly you should now be able to set the color of the LED by typing one of the following colors or color codes followed by the return key. To modify the mapping between the color names and color codes, refer to the 'JSON Settings' section of this document.

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

## JSON Settings

The settings files, ```default.json``` and ```user.json```, set properties that will be loaded into the script at runtime. The ```default.json``` file should not be modified, however, any setting that you wish to change can be set within the ```user.json``` file. Settings from this file will override anything set within ```default.json```. The following is a list of settings that may be modified:

### color_codes
An array of strings which represent color codes that will be mapped to the color names. The strings must meet the following format: "{r}{g}{b}" where r, g, and b are either 0 or 1; 0 corresponds to off and 1 corresponds to on.
Example:
  "011" corresponds to a teal color (red: off, green: on, blue: on).

### color_names
An array of strings which represent color names that can be entered by the user instead of color codes. The order of this array is important as it is directly mapped to the color codes array.
Example:
  If "green" is the third value in ```color_names``` and "010" is the third value in ```color_codes``` then "green" will be mapped to "010".

### pins
An array of integers which represent GPIO pins that will be used for the RGB input. The pin numbers should be ordered as follows: [{R}, {G}, {B}].
Example:
  [11, 13, 15] corresponds to red input GPIO pin 11, green input GPIO pin 13, and blue input GPIO pin 15.

## The Circuit

In order to build the circuit the following parts are required:
* 1x Raspberry Pi
* 1x Multi-color LED
* 3x Resistor (must meet the specs outlined on the LED datasheet)

I chose to use [Round Type, FULL COLOR LED lamp BL-L515](http://www.adafruit.com/product/159) from Adafruit, and 330Ω, 180Ω, and 120Ω resistors purchased from Amazon.

It is assumed that GPIO pins 11, 13, and 15 will be used for the red, green, and blue pins, respectively, of the LED. In order to change these pin numbers, refer to the 'JSON Settings' section of this document.

### Schematic
![Schematic](https://raw.githubusercontent.com/swm93/rgb-led/master/images/schematic.png)

### Breadboard
![Breadboard](https://raw.githubusercontent.com/swm93/rgb-led/master/images/breadboard.png)
