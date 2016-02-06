#! /usr/bin/env python

import subprocess
import time
from Adafruit_I2C import Adafruit_I2C
import RPi.GPIO as GPIO

# set up i2c
trinket_address = 8
trinket = Adafruit_I2C(trinket_address)

# set up gpio
GPIO.setmode(GPIO.BCM)
buttonPin = 5
GPIO.setup(buttonPin, GPIO.IN)

def buttonLight(bright):
    trinket.write8(ord('a'),bright)

while True:
    buttonLight(255)
    GPIO.wait_for_edge(buttonPin, GPIO.FALLING)
    buttonLight(0)
    time.sleep(3)
