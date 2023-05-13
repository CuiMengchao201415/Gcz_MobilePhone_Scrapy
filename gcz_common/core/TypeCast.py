class TypeCast:
    def intToHexStrOnlyValue(self, data: int):
        """
        int10进制转16进制字符串，仅保留数值部分
        :param data: 10进制数值 in=10
        :return: 16进制字符串，仅保留数值部分 out=0a
        """
        hexstr = hex(data)
        if len(hexstr) % 2 == 0:
            return hexstr[2:]
        else:
            return f"0{hexstr[2:]}"

    def hexStrOnlyValueToHexByteStr(self, hexStr: str):
        """
        仅数值部分的16进制字符串转16进制字节串
        :param hexStr: 仅数值部分的16进制字符串 in=0a
        :return: 16进制字节串 out=b'\x0a'
        """
        return bytes().fromhex(hexStr)

    def intsToHexByteStr(self, ints: list):
        """
        10进制int数组转16进制字节串
        :param ints: 10进制int数组 in=[10, 01, 02]
        :return: 16进制字节串 out=b'\x0a\x01\x02'
        """
        return bytes(ints)

    def hexByteStrToHexStrs(self, hexStr: str):
        return [hex(x) for x in bytes(hexStr)]

    def hexByteStrToInts(self, hexStr: str):
        return [x for x in bytes(hexStr)]

    def hexByteStrToHexStrOnlyValue(self, hexStr: str):
        return [self.intToHexStrOnlyValue(x) for x in bytes(hexStr)]

    def hexStrOnlyValueToListStepTwo(self, hexStrOnlyValue: str):
        lent = int(len(hexStrOnlyValue) / 2)
        lis = []
        for i in range(lent):
            lis.append(hexStrOnlyValue[i:(i+1)*2])
        return lis


instance = TypeCast()

if __name__ == '__main__':
    instance.hexByteStrToHexs("1")