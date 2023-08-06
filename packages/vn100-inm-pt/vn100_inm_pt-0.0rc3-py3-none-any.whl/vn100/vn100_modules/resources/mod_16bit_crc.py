# Integrity checker 16-bit CRC-CCITT based.
# See section 4.4.3 of VN-100 User Manual (pg. 34).
# Document number: UM001 v2.05.
# This is the Python 3 version.
# Author of this script: Andrés Eduardo Torres Hernández.


class CRC16_CCITT:
    '''Integrity checker 16-bit CRC-CCITT algorithm based.
    See section 4.4.2 of VN-100 User Manual (pg. 33).
    Document number: UM001 v2.05.'''
    @staticmethod
    def _calculate_checksum(data):
        '''Calculates the 16-bit CRC-CCITT algorithm based integrity sequence.
        args: (
            data: bytearray.
        )'''
        crc = 0
        for i in range(len(data)):
            crc = (((crc >> 8) & 0xFF) | (crc << 8)) & 0xFFFF   #uint16
            crc = (crc ^ data[i]) & 0xFFFF   #uint16
            crc = (crc ^ ((crc & 0xFF) >> 4)) & 0xFFFF   #uint16
            crc = (crc ^ (crc << 12)) & 0xFFFF   #uint16
            crc = (crc ^ (crc & 0x00FF) << 5) & 0xFFFF   #uint16
        return crc

    @staticmethod
    def put_in_vn_binary_data(data):
        '''Insert the 16-bit CRC according to VN-100 User Manual guideline.
        args: (
            data: bytearray.
        )'''
        _data = bytearray([data[1]])
        for i in range(2, len(data)):
            _data = b''.join([_data, bytes([data[i]])])
        # Calculate checksum at hexadecimal format:
        crc = CRC16_CCITT._calculate_checksum(_data)
        # Concatenate data with checksum:
        crc = crc.to_bytes(2, "big")
        data = b''.join([data, crc])
        return data

    @staticmethod
    def check_vn_binary_data(data):
        '''Check the integrity data, 16-bit CRC-CCITT algorithm based.
        args: (
            data: bytearray.
        )'''
        result = False
        msgWithCRC = bytearray([data[1]])
        # msgWithCRC
        datalength = len(data)
        for i in range(2, datalength):
            msgWithCRC = b''.join([msgWithCRC, bytes([data[i]])])
        # If CRC result of message with CRC is 0, then is valid (see section 5.3.5 of VN-100 User Manual (pg. 40))
        if (CRC16_CCITT._calculate_checksum(msgWithCRC) == 0):
            result = True
        else:
            result = False
        return result

if __name__ == "__main__":
    # Demo
    print("---------- Demonstration of use ----------")
    print("Example case 1 of section 5.3.7 of VN-100 User Manual (pg. 42)")
    # Data
    data = bytearray([0xFA, 0x1, 0x8, 0x0, 0x93, 0x50, 0x2E, 0x42, 0x83, 0x3E, 0xF1, 0x3F, 0x48, 0xB5, 0x4, 0xBB])
    bad_crc_data = bytearray([0x92, 0x91])
    # Make bad_crc_data bytearray with data + crc:
    bad_crc_data = b''.join([data, bad_crc_data])
    print("Data, with bad crc: {}".format(bad_crc_data))
    print("Putting a new good checksum...")
    dataWithCksm = CRC16_CCITT.put_in_vn_binary_data(data)
    print("dataWithCksm: {}".format(dataWithCksm))
    print("Checking checksums...")
    print("Good example (data processed):")
    cksmFromMsg = CRC16_CCITT.check_vn_binary_data(dataWithCksm)
    print("cksmFromMsg: {}".format(cksmFromMsg))
    print("Bad example (initial data):")
    res = CRC16_CCITT.check_vn_binary_data(data)
    print("cksmFromMsg: {}".format(res))