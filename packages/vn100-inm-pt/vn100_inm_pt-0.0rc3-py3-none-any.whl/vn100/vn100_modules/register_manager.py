# VectorNav VN-100's register manager
# See section 6 of VN-100 User Manual (pg. 56).
# Document number: UM001 v2.05.
# Firmware version: 2.0.0.0.
# This is the Python 3 version.
# Author of this script: Andrés Eduardo Torres Hernández.

from .resources import C8bit_cksm


class VN100_Register_Manager:
    '''VectorNav VN-100's register manager
    See section 6 of VN-100 User Manual (pg. 56).
    Document number: UM001 v2.05.
    Firmware version: 2.0.0.0.'''
    @staticmethod
    def _read_register(id_register):
        '''Read the contents from register of id_register given.
        args: (
            id_register: integer with a VectorNav VN-100's register id.
        )
        See section 6.1.1 of VN-100 User Manual (pg. 56).'''
        cmd = "$VNRRG," + str(id_register)
        cmd = cmd.encode("ascii")
        cmd = C8bit_cksm.put_in_data(cmd)
        return cmd + b"\r\n"

    @staticmethod
    def _write_register(id_register, args):
        '''Write to contents of register of id_register given.
        args: (
            id_register: integer with a VectorNav VN-100's register id.
            args: dictionary of fields and values to write to the module. The structure is: 
                {
                    "length": 2,
                    "contents": {
                        0: 12,
                        1: 30}
                    }
                }
                Where "length" is the number of key-value items into "contents" sub-dictionary, so:
                contents.keys are the contents.values positions on message to write to the module.
                contents.values are the values to write through the output message.
        )
        See section 6.1.2 of VN-100 User Manual (pg. 56).'''
        # Build the string from args:
        args_str = ""
        for i in range(args["length"]):
            args_str = args_str + "," + str(args["contents"][i])
        cmd = "$VNWRG," + str(id_register) + args_str
        cmd = cmd.encode("ascii")
        cmd = C8bit_cksm.put_in_data(cmd)
        return cmd + b"\r\n"



if __name__ == "__main__":
    # Demo
    print("---------- Demonstration of use ----------")
    uart_bit_rate_register = {
        "length": 1,
        "contents": {
            0: 9600
        }
    }
    print("Read from register 5: {}".format(
        VN100_Register_Manager._read_register(5)
    ))
    print("Write to register 5: {}".format(
        VN100_Register_Manager._write_register(5, uart_bit_rate_register))
    )