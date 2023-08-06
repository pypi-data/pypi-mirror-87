# VectorNav VN-100's system module
# See section 6 of VN-100 User Manual (pg. 56).
# Document number: UM001 v2.05.
# Firmware version: 2.0.0.0.
# This is the Python 3 version.
# Author of this script: Andrés Eduardo Torres Hernández.
from .register_manager import VN100_Register_Manager
from .resources import C8bit_cksm


class VN100_System_module(VN100_Register_Manager):
    '''VectorNav VN-100's system module
    See section 6 of VN-100 User Manual (pg. 56).
    Document number: UM001 v2.05.
    Firmware version: 2.0.0.0.'''
    # Register variables:
    serial_ports = {
        "CURRENT": 0,
        "SERIAL_PORT_1": 1,
        "SERIAL_PORT_2": 2
    }

    serial_baud_rate = {
        "BaudRate": {
            "position": 0,
            "data_type": "uint32",
            "unit": "b/s",
            "valid_values_scope": [
                9600,
                19200,
                38400,
                57600,
                115200,
                128000,
                230400,
                460800,
                921600]
        },
        "SerialPort": {
            "position": 1,
            "data_type": "uint8",
            "unit": "b/s",
            "valid_values_scope": serial_ports
        }
    }

    async_data_output_type = {
        "ADOR": {
            "position": 0,
            "data_type": "uint32",
            "unit": "-",
            "valid_values_scope": {
                "N/A": 0,
                "VNYPR": 1,
                "VNQTN": 2,
                "VNQMR": 8,
                "VNMAG": 10,
                "VNACC": 11,
                "VNGYR": 12,
                "VNMAR": 13,
                "VNYMR": 14,
                "VNYBA": 16,
                "VNYIA": 17,
                "VNIMU": 19,
                "VNDTV": 30
            }
        },
        "SerialPort": {
            "position": 1,
            "data_type": "uint8",
            "unit": "-",
            "valid_values_scope": serial_ports
        }
    }

    async_data_output_frequency = {
        "ADOF": {
            "position": 0,
            "data_type": "uint32",
            "unit": "Hz",
            "valid_values_scope": [
                1,
                2,
                4,
                5,
                10,
                20,
                25,
                40,
                50,
                100,
                200
            ]
        },
        "SerialPort": {
            "position": 1,
            "data_type": "uint8",
            "unit": "-",
            "valid_values_scope": serial_ports
        }
    }

    synchronization_control = {
        "SyncInMode": {
            "position": 0,
            "data_type": "uint8",
            "unit": "-",
            "valid_values_scope": {
                "COUNT": 3,
                "IMU": 4,
                "ASYNC": 5
            }
        },
        "SyncInEdge": {
            "position": 1,
            "data_type": "uint8",
            "unit": "-",
            "valid_values_scope": {
                "RISING": 0,
                "FALLING": 1
            }
        },
        "SyncInSkipFactor": {
            "position": 2,
            "data_type": "uint16",
            "unit": "-",
            "valid_values_scope": {
                "__min": 0,
                "__max": 8
            }
        },
        "RESERVED_1": {
            "position": 3,
            "data_type": "uint32",
            "unit": "-",
            "valid_values_scope": {
            }
        },
        "SyncOutMode": {
            "position": 4,
            "data_type": "uint8",
            "unit": "-",
            "valid_values_scope": {
                "NONE": 0,
                "IMU_START": 1,
                "IMU_READY": 2,
                "AHRS": 3
            }
        },
        "SyncOutPolarity": {
            "position": 5,
            "data_type": "uint8",
            "unit": "-",
            "valid_values_scope": {
                "NEGATIVE": 0,
                "POSITIVE": 1
            }
        },
        "SyncOutSkipFactor": {
            "position": 6,
            "data_type": "uint16",
            "unit": "-",
            "valid_values_scope": {
                "__min": 0,
                "__max": 8
            }
        },
        "SyncOutPulseWidth": {
            "position": 7,
            "data_type": "uint32",
            "unit": "ns",
            "valid_values_scope": {
                "__min": 1,
                "__max": 999999999
            }
        },
        "RESERVED_2": {
            "position": 8,
            "data_type": "uint32",
            "unit": "-",
            "valid_values_scope": {
            }
        }
    }

    communication_protocol_control = {
        "SerialCount": {
            "position": 0,
            "data_type": "uint8",
            "unit": "-",
            "valid_values_scope": {
                "NONE": 0,
                "SYNCIN_COUNT": 1,
                "SYNCIN_TIME": 2,
                "SYNCOUT_COUNT": 3
            }
        },
        "SerialStatus": {
            "position": 1,
            "data_type": "uint8",
            "unit": "-",
            "valid_values_scope": {
                "OFF": 0,
                "VPE_STATUS": 1
            }
        },
        "SPICount": {
            "position": 2,
            "data_type": "uint8",
            "unit": "-",
            "valid_values_scope": {
                "NONE": 0,
                "SYNCIN_COUNT": 1,
                "SYNCIN_TIME": 2,
                "SYNCOUT_COUNT": 3
            }
        },
        "SPIStatus": {
            "position": 3,
            "data_type": "uint8",
            "unit": "-",
            "valid_values_scope": {
                "OFF": 0,
                "VPE_STATUS": 1
            }
        },
        "SerialChecksum": {
            "position": 4,
            "data_type": "uint8",
            "unit": "-",
            "valid_values_scope": {
                "8-BIT": 1,
                "16-BIT": 3
            }
        },
        "SPIChecksum": {
            "position": 5,
            "data_type": "uint8",
            "unit": "-",
            "valid_values_scope": {
                "OFF": 0,
                "8-BIT": 1,
                "16-BIT": 3
            }
        },
        "ErrorMode": {
            "position": 6,
            "data_type": "uint8",
            "unit": "-",
            "valid_values_scope": {
                "IGNORE": 0,
                "SEND": 1,
                "SEND_ADOROFF": 2
            }
        }
    }

    _binary_output_registers_output_groups_fields = {
        "NONE": 0,
        "GROUP_1": {
            "bit_offset": 0,
            "Fields": {
                "TimeStartUp": 0,
                "TimeSyncIn": 2,
                "YawPitchRoll": 3,
                "Quaternion": 4,
                "AngularRate": 5,
                "Accel": 8,
                "Imu": 9,
                "MagPres": 10,
                "DeltaTheta": 11,
                "VpeStatus": 12,
                "SyncInCnt": 13
            }
        },
        "GROUP_3": {
            "bit_offset": 2,
            "Fields": {
                "ImuStatus": 0,
                "UncompMag": 1,
                "UncompAccel": 2,
                "UncompGyro": 3,
                "Temp": 4,
                "Pres": 5,
                "DeltaTheta": 6,
                "DeltaVel": 7,
                "Mag": 8,
                "Accel": 9,
                "Gyro": 10,
                "SensSat": 11,
                "Raw": 12
            }
        },
        "GROUP_5": {
            "bit_offset": 4,
            "Fields": {
                "VpeStatus": 0,
                "YawPitchRoll": 1,
                "Quaternion": 2,
                "DCM": 3,
                "MagNed": 4,
                "AccelNed": 5,
                "LinearAccelBody": 6,
                "LinearAccelNed": 7,
                "YprU": 8
            }
        }
    }

    binary_output_registers = {
        "Binary_output_register_number": {
            "data_type": "uint16",
            "unit": "-",
            "valid_values_scope": {
                1: 75,
                2: 76,
                3: 77
            }
        },
        "AsyncMode": {
            "position": 0,
            "data_type": "uint16",
            "unit": "-",
            "valid_values_scope": {
                "NONE": 0,
                "SERIAL_PORT_1": 1,
                "SERIAL_PORT_2": 2,
                    "BOTH_SERIAL_PORTS": 3
            }
        },
        "RateDivisor": {
            "position": 1,
            "data_type": "uint16",
            "unit": "-",
            "valid_values_scope": {
                "__min": 0,
                "__max": 100
            }
        },
        "OutputGroup": {
            "position": 2,
            "data_type": "uint16",
            "unit": "-",
            "valid_values_scope": _binary_output_registers_output_groups_fields

        },
        "OutputField": {
            "position": 3,
            "data_type": "uint16",
            "unit": "-",
            "valid_values_scope": _binary_output_registers_output_groups_fields
        }
    }

    synchronization_status = {
        "Counter": {
            "valid_values_scope": {
                "SyncInCount": 0,
                "SyncOutCount": 2
            }
        }
    }

    # Methods:
    @staticmethod
    def write_settings():
        '''Write settings into static memory.
        See section 6.1.3 of VN-100 User Manual (pg. 57).'''
        cmd = "$VNWNV"
        cmd = cmd.encode("ascii")
        return C8bit_cksm.put_in_data(cmd)

    @staticmethod
    def restore_factory_settings():
        '''Restore factory settings.
        See section 6.1.4 of VN-100 User Manual (pg. 57).'''
        cmd = "$VNRFS"
        cmd = cmd.encode("ascii")
        return C8bit_cksm.put_in_data(cmd)

    @staticmethod
    def tare():
        '''Set in zero out the current orientation of the module.
        See section 6.1.5 of VN-100 User Manual (pg. 57).'''
        cmd = "$VNTAR"
        cmd = cmd.encode("ascii")
        return C8bit_cksm.put_in_data(cmd)

    @staticmethod
    def reset():
        '''Reset the module.
        See section 6.1.6 of VN-100 User Manual (pg. 58).'''
        cmd = "$VNRST"
        cmd = cmd.encode("ascii")
        return C8bit_cksm.put_in_data(cmd)

    @staticmethod
    def set_user_tag(tag):
        '''Sets the "User tag" register content.
        args: (
            tag: string with the new tag. The max length is 20 characters.
        )
        See section 6.2.1 of VN-100 User Manual (pg. 60).'''
        # If not a str:
        if (not isinstance(tag, str)):
            raise ValueError("User tag must be a string.")
        # If too large:
        if (len(tag) > 20):
            raise ValueError("User tag is too large. 20 characters max.")
        # If it has "$", "," and/or "*":
        if ("$" in tag or
            "*" in tag or
                "," in tag):
            raise ValueError(
                "User tag string has invalid characters. Avoid to use '$', '*' or ','.")
        tag_args = {
            "length": 1,
            "contents": {
                0: tag
            }
        }
        return VN100_System_module._write_register(0, tag_args)

    @staticmethod
    def get_user_tag():
        '''Gets the "User tag" register content.
        See section 6.2.1 of VN-100 User Manual (pg. 60).'''
        return VN100_System_module._read_register(0)

    @staticmethod
    def get_model_number():
        '''Gets the "Model number" register content.
        See section 6.2.2 of VN-100 User Manual (pg. 61).'''
        return VN100_System_module._read_register(1)

    @staticmethod
    def get_hardware_revision():
        '''Gets the "Hardware revision" register content.
        See section 6.2.3 of VN-100 User Manual (pg. 62).'''
        return VN100_System_module._read_register(2)

    @staticmethod
    def get_serial_number():
        '''Gets the "Serial number" register content.
        See section 6.2.4 of VN-100 User Manual (pg. 63).'''
        return VN100_System_module._read_register(3)

    @staticmethod
    def get_firmware_version():
        '''Gets the "Firmware version" register content.
        See section 6.2.5 of VN-100 User Manual (pg. 64).'''
        return VN100_System_module._read_register(4)

    @staticmethod
    def set_serial_baud_rate(
            BaudRate,
            SerialPort="CURRENT"):
        '''Sets the "Serial baud rate" register content.
        args: (
            baud_rate: integer with the new baud rate value.
                For valid values consult on this class the serial_baud_rate["BaudRate"]["valid_values_scope"] attribute.
            SerialPort: integer with the serial port number.
                For valid values consult on this class the serial_ports.keys() attribute.
        )
        See section 6.2.6 of VN-100 User Manual (pg. 65).'''
        # Datagram dictionary:
        sbr_args = {
            "length": 0,
            "contents": {}
        }
        # BaudRate:
        if (not isinstance(BaudRate, int)):
            raise ValueError("Baud rate must be an integer.")
        # If baud rate is not a valid value:
        elif (BaudRate not in VN100_System_module.serial_baud_rate["BaudRate"]["valid_values_scope"]):
            raise ValueError(
                "Baud rate value arg is not valid. See Table 25 of VN-100 User Manual (pg. 65) about valid values.")
        elif (sbr_args["length"] == VN100_System_module.serial_baud_rate["BaudRate"]["position"]):
            sbr_args["length"] += 1
            sbr_args["contents"].update(
                {VN100_System_module.serial_baud_rate["BaudRate"][
                    "position"]: BaudRate})
        else:
            raise IndexError("Index position message isn't coherent.")

        # SerialPort:
        if (SerialPort not in VN100_System_module.serial_baud_rate["SerialPort"]["valid_values_scope"]):
            raise ValueError(
                "Serial port value arg is not valid. See VN-100 User Manual at pg. 65 about valid values.")
        elif (not isinstance(SerialPort, str)):
            raise ValueError("Serial port must be a string.")
        elif (sbr_args["length"] == VN100_System_module.serial_baud_rate["SerialPort"]["position"]):
            if (SerialPort == "CURRENT"):
                pass
            else:
                sbr_args["length"] += 1
                sbr_args["contents"].update(
                    {VN100_System_module.serial_baud_rate["SerialPort"][
                        "position"]: VN100_System_module.serial_baud_rate["SerialPort"][
                        "valid_values_scope"][SerialPort]})
        else:
            raise IndexError("Index position message isn't coherent.")

        return VN100_System_module._write_register(5, sbr_args)

    @staticmethod
    def get_serial_baud_rate():
        '''Gets the "Serial baud rate" register content.
        See section 6.2.6 of VN-100 User Manual (pg. 65).'''
        return VN100_System_module._read_register(5)

    @staticmethod
    def set_async_data_output_type(
            ADOR,
            SerialPort="CURRENT"):
        '''Sets the "Async data output type" register content.
        args: (
            ADOR: string with asynchronous solution output settings.
                For valid values consult on this class the async_data_output_type["ADOR"]["valid_values_scope"].keys() attribute.
            SerialPort: integer with serial port number.
                For valid values consult on this class the serial_ports.keys() attribute.
        )
        See section 6.2.7 of VN-100 User Manual (pg. 66).'''
        # Datagram dictionary:
        ador_args = {
            "length": 0,
            "contents": {}
        }
        # ADOR:
        if (not isinstance(ADOR, str)):
            raise ValueError("ADOR must be an string.")
        # If ADOR is not a valid value:
        elif (ADOR not in VN100_System_module.async_data_output_type["ADOR"]["valid_values_scope"].keys()):
            raise ValueError(
                "ADOR value arg is not valid. See Table 26 of VN-100 User Manual (pg. 66) about valid values.")
        elif (ador_args["length"] == VN100_System_module.async_data_output_type["ADOR"]["position"]):
            ador_args["length"] += 1
            ador_args["contents"].update(
                {VN100_System_module.async_data_output_type["ADOR"][
                    "position"]: VN100_System_module.async_data_output_type["ADOR"]["valid_values_scope"][ADOR]})
        else:
            raise IndexError("Index position message isn't coherent.")
        # SerialPort:
        if (SerialPort not in VN100_System_module.async_data_output_type["SerialPort"]["valid_values_scope"].keys()):
            raise ValueError(
                "Serial port value arg is not valid. See VN-100 User Manual at pg. 66 about valid values.")
        elif (not isinstance(SerialPort, str)):
            raise ValueError("Serial port must be string.")
        elif (ador_args["length"] == VN100_System_module.serial_baud_rate["SerialPort"]["position"]):
            if (SerialPort == "CURRENT"):
                pass
            else:
                ador_args["length"] += 1
                ador_args["contents"].update(
                    {VN100_System_module.serial_baud_rate["SerialPort"][
                        "position"]: VN100_System_module.serial_baud_rate["SerialPort"][
                        "valid_values_scope"][SerialPort]})
        else:
            raise IndexError("Index position message isn't coherent.")
        return VN100_System_module._write_register(6, ador_args)

    @staticmethod
    def get_async_data_output_type():
        '''Gets the "Async data output type" register content.
        See section 6.2.7 of VN-100 User Manual (pg. 66).'''
        return VN100_System_module._read_register(6)

    @staticmethod
    def set_async_data_output_frequency(
            ADOF,
            SerialPort="CURRENT"):
        '''Sets the "Async data output frequency" register content.
        args: (
            ADOF: integer with the async data output frequency value, in Hz.
                For valid values consult on this class the async_data_output_frequency["ADOF"]["valid_values_scope"] attribute.
            SerialPort: integer with serial port number.
                For valid values consult on this class the serial_ports.keys() attribute.
        )
        See section 6.2.8 of VN-100 User Manual (pg. 67).'''
        # Datagram dictionary:
        adof_args = {
            "length": 0,
            "contents": {}
        }
        # ADOF:
        if (not isinstance(ADOF, int)):
            raise ValueError("ADOF must be an integer.")
        # If ADOF is not a valid value:
        elif (ADOF not in VN100_System_module.async_data_output_frequency["ADOF"]["valid_values_scope"]):
            raise ValueError(
                "ADOR value arg is not valid. See Table 26 of VN-100 User Manual (pg. 66) about valid values.")
        elif (adof_args["length"] == VN100_System_module.async_data_output_frequency["ADOF"]["position"]):
            adof_args["length"] += 1
            adof_args["contents"].update(
                {VN100_System_module.async_data_output_frequency["ADOF"][
                    "position"]: ADOF})
        else:
            raise IndexError("Index position message isn't coherent.")
        # SerialPort:
        if (SerialPort not in VN100_System_module.async_data_output_frequency["SerialPort"]["valid_values_scope"].keys()):
            raise ValueError(
                "Serial port value arg is not valid. See VN-100 User Manual at pg. 66 about valid values.")
        # If serial port is not a valid value:
        elif (SerialPort not in VN100_System_module.serial_ports):
            raise ValueError(
                "Serial port value arg is not valid. See VN-100 User Manual at pg. 67 about valid values.")
        elif (adof_args["length"] == VN100_System_module.serial_baud_rate["SerialPort"]["position"]):
            if (SerialPort == "CURRENT"):
                pass
            else:
                adof_args["length"] += 1
                adof_args["contents"].update(
                    {VN100_System_module.serial_baud_rate["SerialPort"][
                        "position"]: VN100_System_module.serial_baud_rate["SerialPort"][
                        "valid_values_scope"][SerialPort]})
        else:
            raise IndexError("Index position message isn't coherent.")
        return VN100_System_module._write_register(7, adof_args)

    @staticmethod
    def get_async_data_output_frequency():
        '''Gets the "Async data output frequency" register content.
        See section 6.2.8 of VN-100 User Manual (pg. 67).'''
        return VN100_System_module._read_register(7)

    @staticmethod
    def set_synchronization_control(
            SyncInMode,
            SyncInEdge,
            SyncInSkipFactor,
            SyncOutMode,
            SyncOutPolarity,
            SyncOutSkipFactor,
            SyncOutPulseWidth):
        '''Sets the "Synchronization control" register content.
        args: (
            SyncInMode: string with sync in mode.
                For valid values consult on this class the synchronization_control["SyncInMode"]["valid_values_scope"].keys() attribute.
            SyncInEdge: string with sync in trigger edge.
                For valid values consult on this class the synchronization_control["SyncInEdge"]["valid_values_scope"].keys() attribute.
            SyncInSkipFactor: integer with the sync in skip factor.
                For valid values consult on this class the synchronization_control["SyncInSkipFactor"]["valid_values_scope"] attribute.
            SyncOutMode: string with sync out mode.
                For valid values consult on this class the synchronization_control["SyncOutMode"]["valid_values_scope"].keys() attribute.
            SyncOutPolarity: string with the sync out polarity.
                For valid values consult on this class the synchronization_control["SyncOutPolarity"]["valid_values_scope"].keys() attribute.
            SyncOutSkipFactor: integer with the sync out skip factor.
                For valid values consult on this class the synchronization_control["SyncOutSkipFactor"]["valid_values_scope"] attribute.
            SyncOutPulseWidth: integer with the sync out pulse width.
                For valid values consult on this class the synchronization_control["SyncOutPulseWidth"]["valid_values_scope"] attribute.
        )
        See section 6.2.9 of VN-100 User Manual (pgs. 68 - 69).'''
        # Datagram dictionary:
        sc_args = {
            "length": 0,
            "contents": {}
        }
        # SyncInMode:
        if (not isinstance(SyncInMode, str)):
            raise ValueError("SyncInMode must be a string.")
        # If SyncInMode is not a valid value:
        elif (SyncInMode not in VN100_System_module.synchronization_control["SyncInMode"]["valid_values_scope"].keys()):
            raise ValueError(
                "SyncInMode value arg is not valid. See Table 28 of VN-100 User Manual (pg. 68) about valid values.")
        elif (sc_args["length"] == VN100_System_module.synchronization_control["SyncInMode"]["position"]):
            sc_args["length"] += 1
            sc_args["contents"].update(
                {VN100_System_module.synchronization_control["SyncInMode"][
                    "position"]: SyncInMode})
        else:
            raise IndexError("Index position message isn't coherent.")

        # SyncInEdge:
        if (not isinstance(SyncInEdge, str)):
            raise ValueError("SyncInEdge must be a string.")
        # If SyncInEdge is not a valid value:
        elif (SyncInEdge not in VN100_System_module.synchronization_control["SyncInEdge"]["valid_values_scope"].keys()):
            raise ValueError(
                "SyncInEdge value arg is not valid. See Table 29 of VN-100 User Manual (pg. 69) about valid values.")
        elif (sc_args["length"] == VN100_System_module.synchronization_control["SyncInEdge"]["position"]):
            sc_args["length"] += 1
            sc_args["contents"].update(
                {VN100_System_module.synchronization_control["SyncInEdge"][
                    "position"]: SyncInEdge})
        else:
            raise IndexError("Index position message isn't coherent.")

        # SyncInSkipFactor:
        if (not isinstance(SyncInSkipFactor, int)):
            raise ValueError("SyncInSkipFactor must be an integer.")
        # If SyncInSkipFactor is not a valid value:
        elif (SyncInSkipFactor > VN100_System_module.synchronization_control["SyncInSkipFactor"]["valid_values_scope"]["__max"] or
                SyncInSkipFactor < VN100_System_module.synchronization_control["SyncInSkipFactor"]["valid_values_scope"]["__min"]):
            raise ValueError(
                "SyncInSkipFactor value arg is not valid. Range [{} - {}].".format(
                    VN100_System_module.synchronization_control[
                        "SyncInSkipFactor"]["valid_values_scope"]["__min"],
                    VN100_System_module.synchronization_control["SyncInSkipFactor"]["valid_values_scope"]["__max"]))
        elif (sc_args["length"] == VN100_System_module.synchronization_control["SyncInSkipFactor"]["position"]):
            sc_args["length"] += 1
            sc_args["contents"].update(
                {VN100_System_module.synchronization_control["SyncInSkipFactor"][
                    "position"]: SyncInSkipFactor})
        else:
            raise IndexError("Index position message isn't coherent.")

        # RESERVED_1
        if (sc_args["length"] == VN100_System_module.synchronization_control["RESERVED_1"]["position"]):
            sc_args["length"] += 1
            sc_args["contents"].update(
                {VN100_System_module.synchronization_control["RESERVED_1"][
                    "position"]: 0})
        else:
            raise IndexError("Index position message isn't coherent.")

        # SyncOutMode:
        if (not isinstance(SyncOutMode, str)):
            raise ValueError("SyncOutMode must be a string.")
        # If SyncOutMode is not a valid value:
        elif (SyncOutMode not in VN100_System_module.synchronization_control["SyncOutMode"]["valid_values_scope"].keys()):
            raise ValueError(
                "SyncOutMode value arg is not valid. See Table 30 of VN-100 User Manual (pg. 69) about valid values.")
        elif (sc_args["length"] == VN100_System_module.synchronization_control["SyncOutMode"]["position"]):
            sc_args["length"] += 1
            sc_args["contents"].update(
                {VN100_System_module.synchronization_control["SyncOutMode"][
                    "position"]: SyncOutMode})
        else:
            raise IndexError("Index position message isn't coherent.")

        # SyncOutPolarity:
        if (not isinstance(SyncOutPolarity, str)):
            raise ValueError("SyncOutPolarity must be a string.")
        # If SyncOutPolarity is not a valid value:
        elif (SyncOutPolarity not in VN100_System_module.synchronization_control["SyncOutPolarity"]["valid_values_scope"].keys()):
            raise ValueError(
                "SyncOutPolarity value arg is not valid. See Table 31 of VN-100 User Manual (pg. 69) about valid values.")
        elif (sc_args["length"] == VN100_System_module.synchronization_control["SyncOutPolarity"]["position"]):
            sc_args["length"] += 1
            sc_args["contents"].update(
                {VN100_System_module.synchronization_control["SyncOutPolarity"][
                    "position"]: SyncOutPolarity})
        else:
            raise IndexError("Index position message isn't coherent.")

        # SyncOutSkipFactor:
        if (not isinstance(SyncOutSkipFactor, int)):
            raise ValueError("SyncOutSkipFactor must be an integer.")
        # If SyncOutSkipFactor is not a valid value:
        elif (SyncOutSkipFactor > VN100_System_module.synchronization_control["SyncOutSkipFactor"]["valid_values_scope"]["__max"] or
                SyncOutSkipFactor < VN100_System_module.synchronization_control["SyncOutSkipFactor"]["valid_values_scope"]["__min"]):
            raise ValueError(
                "SyncOutSkipFactor value arg is not valid. Range [{} - {}].".format(
                    VN100_System_module.synchronization_control[
                        "SyncOutSkipFactor"]["valid_values_scope"]["__min"],
                    VN100_System_module.synchronization_control["SyncOutSkipFactor"]["valid_values_scope"]["__max"]))
        elif (sc_args["length"] == VN100_System_module.synchronization_control["SyncOutSkipFactor"]["position"]):
            sc_args["length"] += 1
            sc_args["contents"].update(
                {VN100_System_module.synchronization_control["SyncOutSkipFactor"][
                    "position"]: SyncOutSkipFactor})
        else:
            raise IndexError("Index position message isn't coherent.")

        # SyncOutPulseWidth:
        if (not isinstance(SyncOutPulseWidth, int)):
            raise ValueError("SyncOutPulseWidth must be an integer.")
        # If SyncOutPulseWidth is not a valid value:
        elif (SyncOutPulseWidth > VN100_System_module.synchronization_control["SyncOutPulseWidth"]["valid_values_scope"]["__max"] or
                SyncOutPulseWidth < VN100_System_module.synchronization_control["SyncOutPulseWidth"]["valid_values_scope"]["__min"]):
            raise ValueError(
                "SyncOutPulseWidth value arg is not valid. Range [{} - {}] ns.".format(
                    VN100_System_module.synchronization_control[
                        "SyncOutPulseWidth"]["valid_values_scope"]["__min"],
                    VN100_System_module.synchronization_control["SyncOutPulseWidth"]["valid_values_scope"]["__max"]))
        elif (sc_args["length"] == VN100_System_module.synchronization_control["SyncOutPulseWidth"]["position"]):
            sc_args["length"] += 1
            sc_args["contents"].update(
                {VN100_System_module.synchronization_control["SyncOutPulseWidth"][
                    "position"]: SyncOutPulseWidth})
        else:
            raise IndexError("Index position message isn't coherent.")

        # RESERVED_2
        if (sc_args["length"] == VN100_System_module.synchronization_control["RESERVED_2"]["position"]):
            sc_args["length"] += 1
            sc_args["contents"].update(
                {VN100_System_module.synchronization_control["RESERVED_2"][
                    "position"]: 0})
        else:
            raise IndexError("Index position message isn't coherent.")

        return VN100_System_module._write_register(32, sc_args)

    @staticmethod
    def get_synchronization_control():
        '''Gets the "Synchronization control" register content.
        See section 6.2.9 of VN-100 User Manual (pgs. 68 - 69):'''
        return VN100_System_module._read_register(32)

    @staticmethod
    def set_communication_protocol_control(
            SerialCount,
            SerialStatus,
            SPICount,
            SPIStatus,
            SerialChecksum,
            SPIChecksum,
            ErrorMode):
        '''Sets the "Communication protocol control" register content.
        args: (
            SerialCount: string with serial count field.
                For valid values consult on this class the communication_protocol_control["SerialCount"]["valid_values_scope"].keys() attribute.
            SerialStatus: string with serial status field.
                For valid values consult on this class the communication_protocol_control["SerialStatus"]["valid_values_scope"].keys() attribute.
            SPICount: string with SPI count field.
                For valid values consult on this class the communication_protocol_control["SPICount"]["valid_values_scope"].keys() attribute.
            SPIStatus: string with SPI status field.
                For valid values consult on this class the communication_protocol_control["SPIStatus"]["valid_values_scope"].keys() attribute.
            SerialChecksum: string with serial integrity data checker.
                For valid values consult on this class the communication_protocol_control["SerialChecksum"]["valid_values_scope"].keys() attribute.
            SPIChecksum: string with SPI integrity data checker.
                For valid values consult on this class the communication_protocol_control["SPIChecksum"]["valid_values_scope"].keys() attribute.
            ErrorMode: string with actions taken when a error event occurs.
                For valid values consult on this class the communication_protocol_control["ErrorMode"]["valid_values_scope"].keys() attribute.
        )
        See section 6.2.10 of VN-100 User Manual (pgs. 70 - 73).'''
        cpc_args = {
            "length": 0,
            "contents": {}
        }
        # SerialCount:
        if (not isinstance(SerialCount, str)):
            raise ValueError("SerialCount must be a string.")
        # If SerialCount is not a valid value:
        elif (SerialCount not in
                VN100_System_module.communication_protocol_control["SerialCount"]["valid_values_scope"].keys()):
            raise ValueError(
                "SerialCount value arg is not valid. See Table 32 of VN-100 User Manual (pg. 71) about valid values.")
        elif (cpc_args["length"] == VN100_System_module.communication_protocol_control["SerialCount"]["position"]):
            cpc_args["length"] += 1
            cpc_args["contents"].update(
                {VN100_System_module.communication_protocol_control["SerialCount"][
                    "position"]: VN100_System_module.communication_protocol_control["SerialCount"]["valid_values_scope"][SerialCount]})
        else:
            raise IndexError("Index position message isn't coherent.")

        # SerialStatus:
        if (not isinstance(SerialStatus, str)):
            raise ValueError("SerialStatus must be a string.")
        # If SerialStatus is not a valid value:
        elif (SerialStatus not in
                VN100_System_module.communication_protocol_control["SerialStatus"]["valid_values_scope"].keys()):
            raise ValueError(
                "SerialStatus value arg is not valid. See Table 33 of VN-100 User Manual (pg. 71) about valid values.")
        elif (cpc_args["length"] == VN100_System_module.communication_protocol_control["SerialStatus"]["position"]):
            cpc_args["length"] += 1
            cpc_args["contents"].update(
                {VN100_System_module.communication_protocol_control["SerialStatus"][
                    "position"]: VN100_System_module.communication_protocol_control["SerialStatus"]["valid_values_scope"][SerialStatus]})
        else:
            raise IndexError("Index position message isn't coherent.")

        # SPICount:
        if (not isinstance(SPICount, str)):
            raise ValueError("SPICount must be a string.")
        # If SPICount is not a valid value:
        elif (SPICount not in
                VN100_System_module.communication_protocol_control["SPICount"]["valid_values_scope"].keys()):
            raise ValueError(
                "SPICount value arg is not valid. See Table 34 of VN-100 User Manual (pg. 72) about valid values.")
        elif (cpc_args["length"] == VN100_System_module.communication_protocol_control["SPICount"]["position"]):
            cpc_args["length"] += 1
            cpc_args["contents"].update(
                {VN100_System_module.communication_protocol_control["SPICount"][
                    "position"]: VN100_System_module.communication_protocol_control["SPICount"]["valid_values_scope"][SPICount]})
        else:
            raise IndexError("Index position message isn't coherent.")

        # SPIStatus:
        if (not isinstance(SPIStatus, str)):
            raise ValueError("SPIStatus must be a string.")
        # If SPIStatus is not a valid value:
        elif (SPIStatus not in
                VN100_System_module.communication_protocol_control["SPIStatus"]["valid_values_scope"].keys()):
            raise ValueError(
                "SPIStatus value arg is not valid. See Table 35 of VN-100 User Manual (pg. 72) about valid values.")
        elif (cpc_args["length"] == VN100_System_module.communication_protocol_control["SPIStatus"]["position"]):
            cpc_args["length"] += 1
            cpc_args["contents"].update(
                {VN100_System_module.communication_protocol_control["SPIStatus"][
                    "position"]: VN100_System_module.communication_protocol_control["SPIStatus"]["valid_values_scope"][SPIStatus]})
        else:
            raise IndexError("Index position message isn't coherent.")

        # SerialChecksum:
        if (not isinstance(SerialChecksum, str)):
            raise ValueError("SerialChecksum must be a string.")
        # If SerialChecksum is not a valid value:
        elif (SerialChecksum not in
                VN100_System_module.communication_protocol_control["SerialChecksum"]["valid_values_scope"].keys()):
            raise ValueError(
                "SerialChecksum value arg is not valid. See Table 36 of VN-100 User Manual (pg. 72) about valid values.")
        elif (cpc_args["length"] == VN100_System_module.communication_protocol_control["SerialChecksum"]["position"]):
            cpc_args["length"] += 1
            cpc_args["contents"].update(
                {VN100_System_module.communication_protocol_control["SerialChecksum"][
                    "position"]: VN100_System_module.communication_protocol_control["SerialChecksum"]["valid_values_scope"][SerialChecksum]})
        else:
            raise IndexError("Index position message isn't coherent.")

        # SPIChecksum:
        if (not isinstance(SPIChecksum, str)):
            raise ValueError("SPIChecksum must be a string.")
        # If SPIChecksum is not a valid value:
        elif (SPIChecksum not in
                VN100_System_module.communication_protocol_control["SPIChecksum"]["valid_values_scope"].keys()):
            raise ValueError(
                "SPIChecksum value arg is not valid. See Table 37 of VN-100 User Manual (pg. 72) about valid values.")
        elif (cpc_args["length"] == VN100_System_module.communication_protocol_control["SPIChecksum"]["position"]):
            cpc_args["length"] += 1
            cpc_args["contents"].update(
                {VN100_System_module.communication_protocol_control["SPIChecksum"][
                    "position"]: VN100_System_module.communication_protocol_control["SPIChecksum"]["valid_values_scope"][SPIChecksum]})
        else:
            raise IndexError("Index position message isn't coherent.")

        # ErrorMode:
        if (not isinstance(ErrorMode, str)):
            raise ValueError("ErrorMode must be a string.")
        # If ErrorMode is not a valid value:
        elif (ErrorMode not in
                VN100_System_module.communication_protocol_control["ErrorMode"]["valid_values_scope"].keys()):
            raise ValueError(
                "ErrorMode value arg is not valid. See Table 38 of VN-100 User Manual (pg. 73) about valid values.")
        elif (cpc_args["length"] == VN100_System_module.communication_protocol_control["ErrorMode"]["position"]):
            cpc_args["length"] += 1
            cpc_args["contents"].update(
                {VN100_System_module.communication_protocol_control["ErrorMode"][
                    "position"]: VN100_System_module.communication_protocol_control["ErrorMode"]["valid_values_scope"][ErrorMode]})
        else:
            raise IndexError("Index position message isn't coherent.")

        return VN100_System_module._write_register(30, cpc_args)

    @staticmethod
    def get_communication_protocol_control():
        '''Gets the "Synchronization control" register content.
        See section 6.2.10 of VN-100 User Manual (pgs. 70 - 73).'''
        return VN100_System_module._read_register(30)

    @staticmethod
    def set_binary_output_registers(
            Binary_output_register_number,
            AsyncMode,
            RateDivisor,
            OutputGroup_fields):
        '''Sets the "Binary output register 1 - 3" register content.
        args: (
            Binary_output_register_number: integer with the binary output register number.
                For valid values consult on this class the binary_output_registers["Binary_output_register_number"]["valid_values_scope"].keys() attribute.
            AsyncMode: string with the output serial ports desired for this task.
                For valid values consult on this class the binary_output_registers["AsyncMode"]["valid_values_scope"].keys() attribute.
            RateDivisor: integer with the rate divisor respect of the ImuRate = 800 Hz.
                For valid values consult on this class the binary_output_registers["RateDivisor"]["valid_values_scope"] attribute.
            OutputGroup_fields: dictionary of groups and fields variables of output messages. The structure is:
                {
                    "GROUP_X": [
                        "Field_X",
                        "Field_Y",
                        ...
                    ],
                    "GROUP_Y": [
                        "Field_X",
                        "Field_Y",
                        ...
                    ]
                }
                For valid values for "GROUPS" dictionary index consult on this class the binary_output_registers["OutputGroup"]["valid_values_scope"].keys() attribute.
                For valid values for "Fields" list values consult on this class the binary_output_registers["OutputField"]["valid_values_scope"][inquired group]["Fields"].keys() attribute,
                example: binary_output_registers["OutputField"]["valid_values_scope"]["GROUP_1"]["Fields"].keys()
        )
        See section 6.2.11 - 6.2.13 of VN-100 User Manual (pgs. 74 - 76).'''
        # Datagram dictionary
        bor_args = {
            "length": 0,
            "contents": {}
        }
        # Binary_output_register_number:
        if (not isinstance(Binary_output_register_number, int)):
            raise ValueError(
                "Binary_output_register_number must be an integer.")
        # If Binary_output_register_number is not a valid value:
        elif (Binary_output_register_number not in VN100_System_module.binary_output_registers["Binary_output_register_number"]["valid_values_scope"].keys()):
            raise ValueError(
                "Binary_output_register_number value arg is not valid. Range [{} - {}].".format(
                    VN100_System_module.binary_output_registers[
                        "Binary_output_register_number"]["valid_values_scope"]["__min"],
                    VN100_System_module.binary_output_registers["Binary_output_register_number"]["valid_values_scope"]["__max"]))

        # AsyncMode:
        if (not isinstance(AsyncMode, str)):
            raise ValueError("AsyncMode must be a string.")
        # If AsyncMode is not a valid value:
        elif (AsyncMode not in
                VN100_System_module.binary_output_registers["AsyncMode"]["valid_values_scope"].keys()):
            raise ValueError(
                "AsyncMode value arg is not valid. See VN-100 User Manual at pg. 74 about valid values.")
        elif (bor_args["length"] == VN100_System_module.binary_output_registers["AsyncMode"]["position"]):
            bor_args["length"] += 1
            bor_args["contents"].update(
                {VN100_System_module.binary_output_registers["AsyncMode"][
                    "position"]: VN100_System_module.binary_output_registers["AsyncMode"]["valid_values_scope"][AsyncMode]})
        else:
            raise IndexError("Index position message isn't coherent.")

        # RateDivisor:
        if (not isinstance(RateDivisor, int)):
            raise ValueError("RateDivisor must be an integer.")
        # If RateDivisor is not a valid value:
        elif (RateDivisor > VN100_System_module.binary_output_registers["RateDivisor"]["valid_values_scope"]["__max"] or
                RateDivisor < VN100_System_module.binary_output_registers["RateDivisor"]["valid_values_scope"]["__min"]):
            raise ValueError(
                "RateDivisor value arg is not valid. Range [{} - {}].".format(
                    VN100_System_module.binary_output_registers[
                        "RateDivisor"]["valid_values_scope"]["__min"],
                    VN100_System_module.binary_output_registers["RateDivisor"]["valid_values_scope"]["__max"]))
        elif (bor_args["length"] == VN100_System_module.binary_output_registers["RateDivisor"]["position"]):
            bor_args["length"] += 1
            bor_args["contents"].update(
                {VN100_System_module.binary_output_registers["RateDivisor"][
                    "position"]: RateDivisor})
        else:
            raise IndexError("Index position message isn't coherent.")

        # ----- OutputGroup and OutputFields: -----
        # OutputGroup:
        if (not isinstance(OutputGroup_fields, dict)):
            raise ValueError("OutputGroup_fields must be a dictionary.")
        for output_group in OutputGroup_fields.keys():
            if (not isinstance(output_group, str)):
                raise ValueError(
                    "OutputGroup_fields index items must be string type.")
            # If OutputGroup_fields index has invalid values:
            if (output_group not in
                    VN100_System_module.binary_output_registers["OutputGroup"]["valid_values_scope"].keys()):
                raise ValueError(
                    "OutputGroup_fields index item '{}' is not a valid arg. See section 5.2.1 of VN-100 User Manual (pg. 36) about valid values.".format(
                        output_group
                    ))

        # Sort OutputGroup_fields keys:
        OutputGroup_fields = {
            k: OutputGroup_fields[k] for k in sorted(OutputGroup_fields)}
        # Build the OutputGroup data segment:
        output_groups_res = 0
        for output_group in OutputGroup_fields.keys():
            # If OutputGroup_fields index has "NONE" key:
            if (output_group == "NONE"):
                # GROUP = 0
                print("Aquí llegó: {}".format(output_group))
                output_groups_res = VN100_System_module.binary_output_registers["OutputGroup"]["valid_values_scope"][output_group]
                output_groups_res = "{0:0{1}X}".format(output_groups_res, 2)
                if (bor_args["length"] == VN100_System_module.binary_output_registers["OutputGroup"]["position"]):
                    bor_args["length"] += 1
                    bor_args["contents"].update(
                        {VN100_System_module.binary_output_registers["OutputGroup"][
                            "position"]: output_groups_res})
                    return VN100_System_module._write_register(
                        VN100_System_module.binary_output_registers[
                            "Binary_output_register_number"]["valid_values_scope"][Binary_output_register_number], bor_args)
            output_groups_res += (
                1 << VN100_System_module.binary_output_registers["OutputGroup"]["valid_values_scope"][
                    output_group]["bit_offset"])
        output_groups_res = "{0:0{1}X}".format(output_groups_res, 2)
        if (bor_args["length"] == VN100_System_module.binary_output_registers["OutputGroup"]["position"]):
            bor_args["length"] += 1
            bor_args["contents"].update(
                {VN100_System_module.binary_output_registers["OutputGroup"][
                    "position"]: output_groups_res})
        else:
            raise IndexError("Index position message isn't coherent.")

        # OutputFields
        # According to added groups, new segments are inserted into datagram,
        # which one corresponds to fields of which group.
        for output_group in OutputGroup_fields.keys():
            for output_field in OutputGroup_fields[output_group]:
                if (not isinstance(output_field, str)):
                    raise ValueError(
                        "OutputGroup_fields value items must be string type.")
                # If OutputGroup_fields items has invalid values:
                if (output_field not in
                        VN100_System_module.binary_output_registers["OutputGroup"]["valid_values_scope"][
                            output_group]["Fields"].keys()):
                    raise ValueError(
                        "OutputGroup_fields field '{}' is not in {} or is a invalid arg. See section 5.2.1 of VN-100 User Manual (pg. 36) about valid values.".format(
                            output_field,
                            output_group
                        ))
        # Build the OutputFields data segments:
        # '3' Is the initial position for GroupFields in the message.
        msg_init_group_field_offset = VN100_System_module.binary_output_registers["OutputField"][
            "position"]
        for output_group in OutputGroup_fields.keys():
            output_field_res = 0
            for output_field in OutputGroup_fields[output_group]:
                output_field_res += (
                    1 << VN100_System_module.binary_output_registers[
                        "OutputGroup"]["valid_values_scope"][output_group]["Fields"][output_field])
            output_field_res = "{0:0{1}X}".format(output_field_res, 4)
            bor_args["length"] += 1
            bor_args["contents"].update(
                {msg_init_group_field_offset: output_field_res})
            msg_init_group_field_offset += 1

        return VN100_System_module._write_register(
            VN100_System_module.binary_output_registers[
                "Binary_output_register_number"]["valid_values_scope"][Binary_output_register_number], bor_args)

    @staticmethod
    def get_binary_output_registers(Binary_output_register_number):
        '''Gets the "Binary output register 1 - 3" register content.
        args: (
            Binary_output_register_number: integer with the binary output register number.
                For valid values consult on this class the binary_output_registers["Binary_output_register_number"]["valid_values_scope"].keys() attribute.
        )
        See section 6.2.11 - 6.2.13 of VN-100 User Manual (pgs. 74 - 76).'''
        return VN100_System_module._read_register(VN100_System_module.binary_output_registers[
            "Binary_output_register_number"]["valid_values_scope"][Binary_output_register_number])

    # Methods for status registers:
    @staticmethod
    def reset_synchronization_status_counters(
            Counter):
        '''Sets the "Synchronization status" register content.
        args: (
            Counter: string with the counters available in the module.
                For valid values consult on this class the synchronization_status["Counter"]["valid_values_scope"].keys() attribute.
        )
        See section 6.3 of VN-100 User Manual (pg. 77).'''
        # Datagram dictionary
        ss_args = {
            "length": 0,
            "contents": {}
        }
        # Counter:
        if (not isinstance(Counter, str)):
            raise ValueError("Counter must be a string.")
        # If Counter is not a valid value:
        elif (Counter not in
                VN100_System_module.synchronization_status["Counter"]["valid_values_scope"].keys()):
            raise ValueError(
                "Counter value arg {} is not valid. See VN-100 User Manual at pg. 77 about valid values.".format(
                    Counter))
        else:
            for i in range(3):
                ss_args["length"] += 1
                if (i == VN100_System_module.synchronization_status["Counter"]["valid_values_scope"][Counter]):
                    # Reiniciar contador
                    ss_args["contents"].update(
                        {i: 0})
                else:
                    ss_args["contents"].update(
                        {i: 1})

        return VN100_System_module._write_register(33, ss_args)

    @staticmethod
    def get_synchronization_status_counters():
        '''Gets the "Synchronization status" register content.
        See section 6.3 of VN-100 User Manual (pg. 77).'''
        return VN100_System_module._read_register(33)
