#
# pythonでもCANを高速受信したい!
#
import sys
from ctypes import CDLL, c_uint8, c_uint32, Structure, byref
# from ctypes import *
from CANFrame import CANFrame

def main():
    CANReceive = CDLL('./CANReceive.so')

    # ソケットを開ける
    socket = CANReceive.openCANSocket("vcan1")
    if socket < 0:
        print("socket open error!")
        return
    print("socket opened. receive loop...")
    
    # 受信待ち
    timeout = 5
    endReq = False
    frame = CANFrame()
    while not endReq:
        stat = CANReceive.readFrame(socket, byref(frame), timeout)
        if not (stat == 0):
            print("timeout or receive error")
            endReq = True
            continue

        # コールバック呼び出し
        onReceive(frame)

# 受信コールバック
def onReceive(frame):
    print("{0} [{1}] {2}".format(
        format(frame.can_id, '04X'),
        frame.can_dlc,
        ' '.join([format(frame.data[d], '02X') for d in range(frame.can_dlc)])
    ))

if __name__ == '__main__':
    try:
        main()
        print("main thread has started. type Ctrl+C to break.")
    except KeyboardInterrupt:
        print("break")