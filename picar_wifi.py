import socket
import time
import struct
from _thread import *
from threading import Thread, Lock
import queue

class PiCarWiFiUdpClient():
    UDP_DST_IP = "255.255.255.255"
    def __init__(self, commands_callback, time_out=6, dst_ip=UDP_DST_IP,recv_port=4210, send_port=4211):
        self.udp_dst_ip = dst_ip
        self.packets_sent = {}
        self.packets_to_send = queue.Queue()
        self.packet_id = 0
        self.udp_send_port = send_port
        self.udp_recv_port = recv_port
        self.time_start = time.time()
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.time_out = time_out
        self.udp_socket.bind(('',recv_port))
        self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.mutex_timeouts = Lock()
        self.c_callback = commands_callback
        # Creating Threads
        start_new_thread(self._packet_sending_thread,())
        start_new_thread(self._packet_receiving_thread,())
        start_new_thread(self._check_timeouts,())
        print("Initialization Done!")
    def _packet_sending_thread(self):
        print("Sending thread started!")
        while True:
            if not self.packets_to_send.empty():
                #print("Building new packet...")
                payload = self.packets_to_send.get()
                pkt_to_send = struct.pack("H%ds" % (len(payload)), self.packet_id, bytes(str(payload),'utf-8'))
                self.udp_socket.sendto(pkt_to_send, (self.udp_dst_ip, self.udp_send_port))
                pkt_sent = struct.pack("IH%ds" % (len(payload)), int(time.time() - self.time_start), len(payload), bytes(str(payload),'utf-8'))
                self.mutex_timeouts.acquire()
                self.packets_sent[self.packet_id] = pkt_sent
                self.mutex_timeouts.release()
                self.packet_id = self.packet_id + 1
            #time.sleep(0.1)
    def _packet_receiving_thread(self):
        print("Receiving thread started!")
        while True:
            data, addr = self.udp_socket.recvfrom(1024)
            res,id = struct.unpack("=BH",data[:3])
            self.mutex_timeouts.acquire()
            if res == 1 and (id in self.packets_sent.keys()):
                self.packets_sent.pop(id)
                #print("Acknowledge ID %i Received!" % (id))
            elif res != 1:
                # It's a command! TODO-Commands Implementation
                
                command = str(data,"utf-8")
               
                if self.c_callback:
                    self.c_callback(command)
            self.mutex_timeouts.release()
    def _check_timeouts(self):
        print("Checking thread started!")
        while True:
            items_to_remove=[]
            self.mutex_timeouts.acquire()
            for id in self.packets_sent:
                packet = self.packets_sent[id]
                (sent_time,payload_length) = struct.unpack("=IH",packet[:6])
                payload = struct.unpack("%ds" % (payload_length),packet[6:])
                if (sent_time + (time.time() - self.time_start)) > (self.time_out):
                    self.packets_to_send.put(payload)
                    #print("Packet %i Timeout!, Resending..." % id)
                    items_to_remove.append(id) 
            if items_to_remove:
                [self.packets_sent.pop(x) for x in items_to_remove]
            self.mutex_timeouts.release()
            time.sleep(0.5)
    def SendPacket(self, payload):
        self.packets_to_send.put(payload)

