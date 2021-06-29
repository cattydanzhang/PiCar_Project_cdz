import time
import board
import digitalio
from adafruit_motor import stepper

# LS => Lidar Stepper
LS_DIR_MODE_FW = stepper.FORWARD
LS_DIR_MODE_BW = stepper.BACKWARD
LS_STYLE_MODE_SINGLE = stepper.SINGLE
LS_STYLE_MODE_DOUBLE = stepper.DOUBLE
LS_STYLE_MODE_MICROSTEP = stepper.MICROSTEP

class	LidarStepper:
#    def __init__(self, delay=0.1, steps=400, coil1=board.D20, coil2=board.D16, coil3=board.D12, coil4=board.D26):
    def __init__(self, delay=0.03, steps=400, coil1=board.D20, coil2=board.D16, coil3=board.D12, coil4=board.D26):
        self.coils = (
            digitalio.DigitalInOut(coil1),  # A1
            digitalio.DigitalInOut(coil2),  # A2
            digitalio.DigitalInOut(coil3),  # B1
            digitalio.DigitalInOut(coil4),  # B2
        )
        self._steps=steps
        self._delay = delay
        for coil in self.coils:
            coil.direction = digitalio.Direction.OUTPUT
        self.motor = stepper.StepperMotor(self.coils[0], self.coils[1], self.coils[2], self.coils[3], microsteps=None)
        
    def setSteps(self, steps, direction_mode = LS_DIR_MODE_FW, style_mode = LS_STYLE_MODE_SINGLE):
        for step in range(steps):
            self.motor.onestep(direction=direction_mode, style=style_mode)
            time.sleep(self._delay)
        #motor.release()

    def turnAngle(self, angle):
        if angle > 0:
            self.setSteps(int(angle / (360.0 / self._steps)), direction_mode = LS_DIR_MODE_FW)
        else:
            self.setSteps(int(abs(angle) / (360.0 / self._steps)), direction_mode = LS_DIR_MODE_BW)
