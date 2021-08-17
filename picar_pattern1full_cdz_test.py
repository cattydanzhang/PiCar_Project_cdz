
from lidar import LidarLite
from lidar_servo import LidarServo
from lidar_stepper import LidarStepper
from picar_wifi import PiCarWiFiUdpClient
import time
from threading import Thread, Lock
from _thread import *

import datetime
import csv


#Set it by the number of pattern:
#PATTERN_NUMBER = 1


#mutex_reset = Lock()
#mutex_running = Lock()
#def send_alive_signal(wifi):
#    while True:
#        wifi.SendPacket("ALV")
#        time.sleep(0.5)

#def command_parser(command):
#    if command == "START":
#        mutex_running.release()
#    elif command == "STOP":
#        mutex_running.acquire(0)
#    elif command == "RESET":
#        mutex_reset.release()


#def write_to_csv():
    # the a is for append, if w for write is used then it overwrites the file
#    with open('/home/pi/PiCar_Project_cdz/lidar_scans01.csv', mode='a') as lidar_scans:
#        sensor_write = csv.writer(lidar_scans, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#        write_to_log = sensor_write.writerow([date_now(),time_now(),get_temp(),get_pressure(),get_lux(),cpu_temperature()])
#        return(write_to_log)

 

#https://stackoverflow.com/questions/57314552/saving-sensor-data-from-pi-into-csv-file
def store_data(stepper,servo,lidar):
    append = [stepper,servo,lidar]
    with open('lidarscan_output08.csv', 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(append)
    csvFile.close()

lidarServo = LidarServo()
lidar = LidarLite()
lidarStepper = LidarStepper()
#picar_rt = PiCarWiFiUdpClient(commands_callback=command_parser)
#start_new_thread(send_alive_signal, (picar_rt,))
#mutex_running.acquire()
#a = 45
#a = 75
#while a < 156:
# 75-92.9, 93-110.9, 111-128.9, 129-146.9,147-164.9
a=75
while a < 164.9:
    b = 0
    lidarServo.setAngle(a)
    while b < 359.9:
#        mutex_running.acquire()
#        mutex_running.release()
#        if mutex_reset.acquire(blocking=False):
#            time.sleep(1)
#            print("Reset occured.")
#            lidarStepper.turnAngle(-1 * b)
#            b = 0
#            a = 44
#            break
        lidarStepper.turnAngle(0.9)
        b=b+0.9
        dist=lidar.measure()
#        print("Lidar: %icm, Stepper: %.2f, Servo: %i" % (dist, b, a))
#        picar_rt.SendPacket("M:%i,%i,%.2f,%i,0,0,0,0,0,0,0,0,0,0,0,0" % (PATTERN_NUMBER, a, b, dist))

        store_data(b,a,dist)

#    write_to_csv(dist, b, a)

    a = a + 1

    
