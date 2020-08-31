#
# pythonでもCANを高速受信したい!
#
from lib.CANClient import CANClient

def main():
    client = CANClient("vcan1", callBack=onReceive)

    for _ in range(10):
        client.sendFrame(0x114, range(8))

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
        while True:
            pass
    except KeyboardInterrupt:
        print("break")