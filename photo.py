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

def flip(bm):
    # http://stackoverflow.com/a/12682003
    return [int('{:08b}'.format(n)[::-1], 2) for n in reversed(bm)]


def take_picture():
    time.sleep(0.25)
    bitmap(trinket, flip(threebm), 100, 0, 0)
    time.sleep(1)
    bitmap(trinket, flip(twobm), 0, 100, 0)
    time.sleep(1)
    bitmap(trinket, flip(onebm), 0, 0, 100)
    time.sleep(1)
    bitmap(trinket, onbm, 200, 200, 200)
    filename = "/home/pi/share/photo" + str(time.time()) + ".jpg"
    subprocess.call(['raspistill', '-t', '1', '-w', '1920', '-h', '1080', '-o', filename])
    bitmap(trinket, offbm, 0, 0, 0)


while True:
    time.sleep(0.25)
    buttonLight(255)
    GPIO.wait_for_edge(buttonPin, GPIO.FALLING)
    buttonLight(0)
    for ii in range(3):
        take_picture()
