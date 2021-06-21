
from lidar import LidarLite
from lidar_servo import LidarServo
from lidar_stepper import LidarStepper
from picar_wifi import PiCarWiFiUdpClient
import time
from threading import Thread, Lock
from _thread import *


#Set it by the number of pattern:
PATTERN_NUMBER = 1


mutex_reset = Lock()
mutex_running = Lock()
def send_alive_signal(wifi):
    while True:
        wifi.SendPacket("ALV")
        time.sleep(0.5)

def command_parser(command):
    if command == "START":
        mutex_running.release()
    elif command == "STOP":
        mutex_running.acquire(0)
    elif command == "RESET":
        mutex_reset.release()


lidarServo = LidarServo()
lidar = LidarLite()
lidarStepper = LidarStepper()
picar_rt = PiCarWiFiUdpClient(commands_callback=command_parser)
start_new_thread(send_alive_signal, (picar_rt,))
mutex_running.acquire()
a = 45
while a < 145:
    b = 0
    lidarServo.setAngle(a)
    while b < 360.0:
        mutex_running.acquire()
        mutex_running.release()
        if mutex_reset.acquire(blocking=False):
            time.sleep(1)
            print("Reset occured.")
            lidarStepper.turnAngle(-1 * b)
            b = 0
            a = 44
            break
        lidarStepper.turnAngle(0.9)
        b=b+0.9
        dist=lidar.measure()
        print("Lidar: %icm, Stepper: %.2f, Servo: %i" % (dist, b, a))
        picar_rt.SendPacket("M:%i,%i,%.2f,%i,0,0,0,0,0,0,0,0,0,0,0,0" % (PATTERN_NUMBER, a, b, dist))
        
        #print("Dist. : %i, Servo: %i, Stepper: %.2f" % (d, a, b)) 
        #time.sleep(0.1)
    a = a + 1
    #thrs.join()
    
