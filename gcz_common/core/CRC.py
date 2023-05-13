import crcmod

class CRCUtil:
    def __init__(self):
        pass

    def crc8(self, str):
        """

        :param str:
        :return: int
        """
        crc8_func = crcmod.predefined.mkCrcFun('CRC-8')
        return crc8_func(str.encode())

    def crc16(self, str):
        crc16_func = crcmod.predefined.mkCrcFun('CRC-16')
        return crc16_func(str.encode())

    def crc32(self, str):
        crc32_func = crcmod.predefined.mkCrcFun('CRC-32')
        return crc32_func(str.encode())

# crc32_func = crcmod.mkCrcFun(poly=0x104C11DB7, initCrc=0, xorOut=0xFFFFFFFF)
instance = CRCUtil()


if __name__ == '__main__':
    # hexStr = "\x01\x02\x03\x04"
    # print(crcmod.predefined.mkCrcFun('CRC-16')(b"\x01\x02\x03\x04"))
    # print(str(instance.crc32(hexStr)))
    # print(bytes().fromhex(hex(instance.crc32(hexStr))[2:]))
    # print(bytes().fromhex('0fa1'))
    # print(hex(instance.crc16(hexStr))[2:])
    # print(instance.crc16(hexStr))
    # print(hex(instance.crc32(hexStr))[2:])
    # print(bytes().fromhex('3c'))
    # print("\x01")

    print(hex(crcmod.predefined.mkCrcFun('CrcModbus')(b"\x5A\x81\x00")))