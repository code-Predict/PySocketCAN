#
# CANフレーム
#
# from ctypes import c_uint32, c_uint8, Structure
from ctypes import *

class CANFrame(Structure):

    def __init__(self, id=0, data = []):
        dlc = 0
        content = (c_uint8 * 8)()
        if len(data) > 0:
            if len(data) > 8:
                print("Invalid data length. data will send only [:8].")

            dlc = len(data[:8])
            content[:] = data[:8]

        super().__init__(c_uint32(id), c_uint8(dlc), 0, 0, 0, content)

    _fields_ = [
        ("can_id", c_uint32),
        ("can_dlc", c_uint8),
        ("__pad", c_uint8),
        ("__res0", c_uint8),
        ("__res1", c_uint8),
        ("data", c_uint8 * 8)
    ]