#! /usr/bin/env python

import subprocess
import time
from Adafruit_I2C import Adafruit_I2C
trinket_address = 8

trinket = Adafruit_I2C(trinket_address)

trinket.write8(ord('a'),255)
