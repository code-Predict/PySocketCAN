#
# 高速CANクライアント
#
from threading import Thread
from queue import Queue, Empty
from ctypes import CDLL, c_uint8, c_uint32, byref
from CANFrame import CANFrame
import sys
try:
    import RPi.GPIO as GPIO
except ImportError:
    pass

class CANClient():

    def __init__(self, channel, intPin = 25, cname = "", callBack = None):
        name = "SocketCANUtil.so"
        if cname != "":
            name = cname
        self.SocketCAN = CDLL(name)

        self.socket = self.SocketCAN.openCANSocket()
        self.onReceive = callBack

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(intPin, GPIO.IN)

        listenerThread = Thread(target=self._rcvThread)
        listenerThread.setDaemon(True)
        listenerThread.start()
    
    def _rcvThread(self):
        frame = CANFrame()
        while True:
            stat = self.SocketCAN.readFrame(self.socket, byref(frame), 0)
            if not (stat == 0):
                print("receive error")
                continue

            if self.onReceive is not None:
                self.onReceive(frame)
        
        self.SocketCAN.closeCANSocket(self.socket)

    def sendFrame(self, id, data = [0x00]):
        frame = CANFrame(id, data)
        self.SocketCAN.sendFrame(self.socket, byref(frame))
        