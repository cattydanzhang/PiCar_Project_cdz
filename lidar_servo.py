# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""Simple test for a standard servo on channel 0 and a continuous rotation servo on channel 1."""
import time
from adafruit_servokit import ServoKit

# Set channels to the number of servo channels on your kit.
# 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
class LidarServo:
    def __init__(self):
        self.kit = ServoKit(channels=16)
    def setAngle(self, angle):
        self.kit.servo[15].angle = angle
        time.sleep(0.1)


