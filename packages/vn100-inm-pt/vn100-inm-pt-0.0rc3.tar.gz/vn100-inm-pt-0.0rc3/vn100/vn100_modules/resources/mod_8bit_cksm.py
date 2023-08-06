# 8-bit checksum
# See section 4.4.2 of VN-100 User Manual (pg. 33).
# Document number: UM001 v2.05.
# This is the Python 3 version.
# Author of this script: Andrés Eduardo Torres Hernández.


class C8bit_cksm:
    '''8-bit checksum
    See section 4.4.2 of VN-100 User Manual (pg. 33).
    Document number: UM001 v2.05.'''
    CHECK_SEQUENCE_MESSAGE_LENGTH = 2   # 2 characters (bytes).
    @staticmethod
    def _calculate_checksum(data):
        '''Calculates the 8-bit checksum for the given sequence.
        args: (
            data: bytearray. This must be an ASCII encoded.
        )'''
        cksm = 0
        for i in range(len(data)):
            #  Exclude asterisk (*) and the next characters:
            data_length = 0
            if (data[i] == int.from_bytes("*".encode("ascii"), "big")):
                data_length = i
                break
        for i in range(data_length):
            # Exclude the dollar sign ($):
            if (data[i] == int.from_bytes("$".encode("ascii"), "big")):
                continue
            cksm = (cksm ^ data[i]) & 0xFF  # uint8
        return cksm

    @staticmethod
    def put_in_data(data):
        '''Insert the 8-bit checksum according to VN-100 User Manual guideline.
        args: (
            data: bytearray. This must be an ASCII encoded.
        )'''
        # Checking if an asterisk is there. If it is not, then put one there:
        asteriskIsThere = 0
        data_length = 0
        for i in range(len(data)):
            if (data[i] == int.from_bytes("*".encode("ascii"), "big")):
                asteriskIsThere = 1
                data_length = i
        if (asteriskIsThere == 0):
            data = data + "*".encode("ascii")
        # If the asterisk is there, delete the next characters:
        elif (asteriskIsThere == 1):
            data = data[:data_length + 1]
        # Calculate checksum at hexadecimal format:
        cksm_hex = "{0:0{1}X}".format(
            C8bit_cksm._calculate_checksum(data),
            C8bit_cksm.CHECK_SEQUENCE_MESSAGE_LENGTH
        )
        # Concatenate data with checksum:
        data = data + cksm_hex.encode("ascii")
        return data

    @staticmethod
    def check_data(data):
        '''Check the integrity data, 8-bit checksum based.
        args: (
            data: bytearray. This must be an ASCII encoded.
        )'''
        result = False
        cksmFromMsg = None
        for i in range(len(data)):
            if (data[i] == int.from_bytes("*".encode("ascii"), "big")):
                cksmFromMsg = b''.join(
                    [data[i+1].to_bytes(1, "big"),
                     data[i+2].to_bytes(1, "big")])
                cksmFromMsg = int(str(cksmFromMsg, encoding="ascii"), 16)
                break
        if (cksmFromMsg == C8bit_cksm._calculate_checksum(data)):
            result = True
        else:
            result = False
        return result


if __name__ == "__main__":
    # Demo
    print("---------- Demonstration of use ----------")
    data = "$VNRRG,8*24"
    print("Initial data, with bad checksum: {}".format(data))
    print("Putting a new good checksum...")
    data = data.encode("ascii")
    dataWithCksm = C8bit_cksm.put_in_data(data)
    print("dataWithCksm: {}".format(dataWithCksm))
    print("Checking checksums...")
    print("Good example (data processed):")
    cksmFromMsg = C8bit_cksm.check_data(dataWithCksm)
    print("cksmFromMsg: {}".format(cksmFromMsg))
    print("Bad example (initial data):")
    res = C8bit_cksm.check_data(data)
    print("cksmFromMsg: {}".format(res))
