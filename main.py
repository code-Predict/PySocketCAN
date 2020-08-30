#
# pythonでもCANを高速受信したい!
#
import sys
# from ctypes import CDLL, c_uint8, c_uint32, Structure, pointer
from ctypes import *

def main():
    CANReceive = CDLL('./CANReceive.so')

    # can_frame構造体
    CANDATA = c_uint8 * 8
    class CAN_Frame(Structure):
        _fields_ = [
            ("can_id", c_uint32),
            ("can_dlc", c_uint8),
            ("__pad", c_uint8),
            ("__res0", c_uint8),
            ("__res1", c_uint8),
            ("data", CANDATA)
        ]

    # ソケットを開ける
    socket = CANReceive.openCANSocket("vcan1")
    if socket < 0:
        print("socket open error!")
        return
    print("socket opened. receive loop...")
    
    # 受信待ち
    timeout = 0
    endReq = False
    frame = CAN_Frame(0, 0, 0, 0, 0, CANDATA(0))
    while not endReq:
        stat = CANReceive.readFrame(socket, byref(frame), timeout)
        if stat < 0:
            print("timeout...")
            endReq = True
            continue
        elif stat > 0:
            print("invalid can frame.")
            endReq = True
            continue

        print("Received!")
        print(frame)

if __name__ == '__main__':
    main()