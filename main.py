#
# pythonでもCANを高速受信したい!
#
import ctypes

def main():
    CANReceive = ctypes.CDLL('./CANReceive.so')
    CANReceive.main(0, ["", ])

if __name__ == '__main__':
    main()