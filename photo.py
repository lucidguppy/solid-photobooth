#! /usr/bin/env python

import subprocess
import time
from Adafruit_I2C import Adafruit_I2C
import RPi.GPIO as GPIO

# button graphs

offbm = [0b00000000,
        0b00000000,
        0b00000000,
        0b00000000,
        0b00000000,
        0b00000000,
        0b00000000,
        0b00000000]

onbm = [0b11111111,
        0b11111111,
        0b11111111,
        0b11111111,
        0b11111111,
        0b11111111,
        0b11111111,
        0b11111111]

threebm = [0b00000000,
        0b00111110,
        0b01000001,
        0b00000001,
        0b00011110,
        0b00000001,
        0b01000001,
        0b00111110]

twobm = [0b00000000,
        0b00111110,
        0b01000001,
        0b00000001,
        0b00001110,
        0b00110000,
        0b01000000,
        0b01111111]

onebm= [0b00000000,
        0b00001000,
        0b00011000,
        0b00101000,
        0b00001000,
        0b00001000,
        0b00001000,
        0b00111110]
# set up i2c
trinket_address = 8
trinket = Adafruit_I2C(trinket_address)

# set up gpio
GPIO.setmode(GPIO.BCM)
buttonPin = 5
GPIO.setup(buttonPin, GPIO.IN)

def buttonLight(bright):
    trinket.write8(ord('a'),bright)

def bitmap(trinket, bm, r, g, b):
    trinket.writeList(ord('b'), bm + [r,g,b])

while True:
    buttonLight(255)
    GPIO.wait_for_edge(buttonPin, GPIO.FALLING)
    buttonLight(0)
    bitmap(trinket, threebm, 100, 0, 0)
    time.sleep(1)
    bitmap(trinket, twobm, 0, 100, 0)
    time.sleep(1)
    bitmap(trinket, onebm, 0, 0, 100)
    time.sleep(1)
    bitmap(trinket, onbm, 255, 255, 255)
    filename = "photo" + str(time.time()) + ".jpg"
    subprocess.call(['raspistill', '-t', '1', '-w', '1920', '-h', '1080', '-o', filename])
    bitmap(trinket, offbm, 0, 0, 0)
