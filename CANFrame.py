#
# CANフレーム
#
from ctypes import c_uint32, c_uint8, Structure

class CANFrame(Structure):

    def __init__(self,id=0, dlc=0):
        super().__init__(id, dlc, 0, 0, 0, (c_uint8 * 8)(0))

    _fields_ = [
        ("can_id", c_uint32),
        ("can_dlc", c_uint8),
        ("__pad", c_uint8),
        ("__res0", c_uint8),
        ("__res1", c_uint8),
        ("data", c_uint8 * 8)
    ]