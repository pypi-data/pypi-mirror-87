# VectorNav VN-100's Attitude subsystem
# See section 8 of VN-100 User Manual (pg. 95).
# Document number: UM001 v2.05.
# Firmware version: 2.0.0.0.
# This is the Python 3 version.
# Author of this script: Andrés Eduardo Torres Hernández.


from .register_manager import VN100_Register_Manager
from .resources import C8bit_cksm
from .logger import init_logger


class VN100_Attitude_Subsystem(VN100_Register_Manager):
    '''VectorNav VN-100's Attitude subsystem
    See section 8 of VN-100 User Manual (pg. 95).
    Document number: UM001 v2.05.
    Firmware version: 2.0.0.0.'''
    # Register variables:
    vpe_basic_control = {
        "Enable": {
            "position": 0,
            "data_type": "uint8",
            "unit": "-",
            "valid_values_scope": {
                "DISABLE": 0,
                "ENABLE": 1
            }
        },
        "HeadingMode": {
            "position": 1,
            "data_type": "uint8",
            "unit": "-",
            "valid_values_scope": {
                "ABSOLUTE": 0,
                "RELATIVE": 1,
                "INDOOR": 2
            }
        },
        "FilteringMode": {
            "position": 2,
            "data_type": "uint8",
            "unit": "-",
            "valid_values_scope": {
                "OFF": 0,
                "MODE_1": 1
            }
        },
        "TuningMode": {
            "position": 3,
            "data_type": "uint8",
            "unit": "-",
            "valid_values_scope": {
                "OFF": 0,
                "MODE_1": 1
            }
        }
    }

    vpe_magnetometer_basic_tuning = {
        "BaseTuningX": {
            "position": 0,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {
                "__min": 0,
                "__max": 10
            }
        },
        "BaseTuningY": {
            "position": 1,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {
                "__min": 0,
                "__max": 10
            }
        },
        "BaseTuningZ": {
            "position": 2,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {
                "__min": 0,
                "__max": 10
            }
        },
        "AdaptiveTuningX": {
            "position": 3,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {
                "__min": 0,
                "__max": 10
            }
        },
        "AdaptiveTuningY": {
            "position": 4,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {
                "__min": 0,
                "__max": 10
            }
        },
        "AdaptiveTuningZ": {
            "position": 5,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {
                "__min": 0,
                "__max": 10
            }
        },
        "AdaptiveFilteringX": {
            "position": 6,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {
                "__min": 0,
                "__max": 10
            }
        },
        "AdaptiveFilteringY": {
            "position": 7,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {
                "__min": 0,
                "__max": 10
            }
        },
        "AdaptiveFilteringZ": {
            "position": 8,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {
                "__min": 0,
                "__max": 10
            }
        }
    }

    vpe_accelerometer_basic_tuning = {
        "BaseTuningX": {
            "position": 0,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {
                "__min": 0,
                "__max": 10
            }
        },
        "BaseTuningY": {
            "position": 1,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {
                "__min": 0,
                "__max": 10
            }
        },
        "BaseTuningZ": {
            "position": 2,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {
                "__min": 0,
                "__max": 10
            }
        },
        "AdaptiveTuningX": {
            "position": 3,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {
                "__min": 0,
                "__max": 10
            }
        },
        "AdaptiveTuningY": {
            "position": 4,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {
                "__min": 0,
                "__max": 10
            }
        },
        "AdaptiveTuningZ": {
            "position": 5,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {
                "__min": 0,
                "__max": 10
            }
        },
        "AdaptiveFilteringX": {
            "position": 6,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {
                "__min": 0,
                "__max": 10
            }
        },
        "AdaptiveFilteringY": {
            "position": 7,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {
                "__min": 0,
                "__max": 10
            }
        },
        "AdaptiveFilteringZ": {
            "position": 8,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {
                "__min": 0,
                "__max": 10
            }
        }
    }

    _logger = init_logger(__name__)

    # Methods:
    @staticmethod
    def get_yaw_pitch_roll():
        '''Gets the "Yaw Pitch Roll" register content.
        See section 8.2.1 of VN-100 User Manual (pg. 95).'''
        return VN100_Attitude_Subsystem._read_register(8)

    @staticmethod
    def get_attitude_quaternion():
        '''Gets the "Attitude quaternion" register content.
        See section 8.2.2 of VN-100 User Manual (pg. 96).'''
        return VN100_Attitude_Subsystem._read_register(9)

    @staticmethod
    def get_ypr_magnetic_acceleration_angular_rates():
        '''Gets the "Yaw, pitch, roll, magnetic, acceleration and angular rates" register content.
        See section 8.2.3 of VN-100 User Manual (pg. 97).'''
        return VN100_Attitude_Subsystem._read_register(27)

    @staticmethod
    def get_quaternion_magnetic_acceleration_angular_rates():
        '''Gets the "Quaternion, magnetic, acceleration and angular rates" register content.
        See section 8.2.4 of VN-100 User Manual (pg. 98).'''
        return VN100_Attitude_Subsystem._read_register(15)

    @staticmethod
    def get_magnetic_measurements():
        '''Gets the "Magnetic measurements" register content.
        See section 8.2.5 of VN-100 User Manual (pg. 99).'''
        return VN100_Attitude_Subsystem._read_register(17)

    @staticmethod
    def get_acceleration_measurements():
        '''Gets the "Acceleration measurements" register content.
        See section 8.2.6 of VN-100 User Manual (pg. 100).'''
        return VN100_Attitude_Subsystem._read_register(18)

    @staticmethod
    def get_angular_rate_measurements():
        '''Gets the "Angular rate measurements" register content.
        See section 8.2.7 of VN-100 User Manual (pg. 101).'''
        return VN100_Attitude_Subsystem._read_register(19)

    @staticmethod
    def get_magnetic_acceleration_angular_rates():
        '''Gets the "Magnetic, acceleration and angular rate measurements" register content.
        See section 8.2.8 of VN-100 User Manual (pg. 102).'''
        return VN100_Attitude_Subsystem._read_register(20)

    @staticmethod
    def get_ypr_true_body_acceleration_angular_rates():
        '''Gets the "Yaw, pitch, roll, true body acceleration and angular rates" register content.
        See section 8.2.9 of VN-100 User Manual (pg. 103).'''
        return VN100_Attitude_Subsystem._read_register(239)

    @staticmethod
    def get_ypr_true_inertial_acceleration_angular_rates():
        '''Gets the "Yaw, pitch, roll, true inertial acceleration and angular rates" register content.
        See section 8.2.10 of VN-100 User Manual (pg. 104).'''
        return VN100_Attitude_Subsystem._read_register(240)

    @staticmethod
    def set_vpe_basic_control():
        '''Sets the "VPE basic control" register content.
        See section 8.3.1 of VN-100 User Manual (pg. 105).'''
        VN100_Attitude_Subsystem._logger.warning(
            "This method isn't implemented yet.")

    @staticmethod
    def get_vpe_basic_control():
        '''Gets the "VPE basic control" register content.
        See section 8.3.1 of VN-100 User Manual (pg. 105).'''
        return VN100_Attitude_Subsystem._read_register(35)

    @staticmethod
    def set_vpe_magnetometer_basic_tuning(
            BaseTuningX,
            BaseTuningY,
            BaseTuningZ,
            AdaptiveTuningX,
            AdaptiveTuningY,
            AdaptiveTuningZ,
            AdaptiveFilteringX,
            AdaptiveFilteringY,
            AdaptiveFilteringZ):
        '''Sets the "VPE magnetometer basic tuning" register content.
        args: (
            BaseTuningX: float with the basic tuning X value.
                For valid values consult on this class the vpe_magnetometer_basic_tuning["BaseTuningX"]["valid_values_scope"] attribute.
            BaseTuningY: float with the basic tuning Y value.
                For valid values consult on this class the vpe_magnetometer_basic_tuning["BaseTuningY"]["valid_values_scope"] attribute.
            BaseTuningZ: float with the basic tuning Z value.
                For valid values consult on this class the vpe_magnetometer_basic_tuning["BaseTuningZ"]["valid_values_scope"] attribute.
            AdaptiveTuningX: float with the adaptive tuning X value.
                For valid values consult on this class the vpe_magnetometer_basic_tuning["AdaptiveTuningX"]["valid_values_scope"] attribute.
            AdaptiveTuningY: float with the adaptive tuning Y value.
                For valid values consult on this class the vpe_magnetometer_basic_tuning["AdaptiveTuningY"]["valid_values_scope"] attribute.
            AdaptiveTuningZ: float with the adaptive tuning Z value.
                For valid values consult on this class the vpe_magnetometer_basic_tuning["AdaptiveTuningZ"]["valid_values_scope"] attribute.
            AdaptiveFilteringX: float with the adaptive filtering X value.
                For valid values consult on this class the vpe_magnetometer_basic_tuning["AdaptiveFilteringX"]["valid_values_scope"] attribute.
            AdaptiveFilteringY: float with the adaptive filtering Y value.
                For valid values consult on this class the vpe_magnetometer_basic_tuning["AdaptiveFilteringY"]["valid_values_scope"] attribute.
            AdaptiveFilteringZ: float with the adaptive filtering Z value.
                For valid values consult on this class the vpe_magnetometer_basic_tuning["AdaptiveFilteringZ"]["valid_values_scope"] attribute.
        )
        See section 8.3.2 of VN-100 User Manual (pg. 106).'''
        # Datagram dictionary
        vmbt_args = {
            "length": 0,
            "contents": {}
        }
        # BaseTuningX:
        if (not isinstance(BaseTuningX, float)):
            raise ValueError("BaseTuningX must be an float.")
        # If BaseTuningX is not a valid value:
        elif (BaseTuningX > VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["BaseTuningX"]["valid_values_scope"]["__max"] or
                BaseTuningX < VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["BaseTuningX"]["valid_values_scope"]["__min"]):
            raise ValueError(
                "BaseTuningX value arg is not valid. Range [{} - {}].".format(
                    VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning[
                        "BaseTuningX"]["valid_values_scope"]["__min"],
                    VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["BaseTuningX"]["valid_values_scope"]["__max"]))
        elif (vmbt_args["length"] == VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["BaseTuningX"]["position"]):
            vmbt_args["length"] += 1
            vmbt_args["contents"].update(
                {VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["BaseTuningX"][
                    "position"]: BaseTuningX})
        else:
            raise IndexError("Index position message isn't coherent.")

        # BaseTuningY:
        if (not isinstance(BaseTuningY, float)):
            raise ValueError("BaseTuningY must be an float.")
        # If BaseTuningY is not a valid value:
        elif (BaseTuningY > VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["BaseTuningY"]["valid_values_scope"]["__max"] or
                BaseTuningY < VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["BaseTuningY"]["valid_values_scope"]["__min"]):
            raise ValueError(
                "BaseTuningY value arg is not valid. Range [{} - {}].".format(
                    VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning[
                        "BaseTuningY"]["valid_values_scope"]["__min"],
                    VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["BaseTuningY"]["valid_values_scope"]["__max"]))
        elif (vmbt_args["length"] == VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["BaseTuningY"]["position"]):
            vmbt_args["length"] += 1
            vmbt_args["contents"].update(
                {VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["BaseTuningY"][
                    "position"]: BaseTuningY})
        else:
            raise IndexError("Index position message isn't coherent.")

        # BaseTuningZ:
        if (not isinstance(BaseTuningZ, float)):
            raise ValueError("BaseTuningZ must be an float.")
        # If BaseTuningZ is not a valid value:
        elif (BaseTuningZ > VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["BaseTuningZ"]["valid_values_scope"]["__max"] or
                BaseTuningZ < VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["BaseTuningZ"]["valid_values_scope"]["__min"]):
            raise ValueError(
                "BaseTuningZ value arg is not valid. Range [{} - {}].".format(
                    VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning[
                        "BaseTuningZ"]["valid_values_scope"]["__min"],
                    VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["BaseTuningZ"]["valid_values_scope"]["__max"]))
        elif (vmbt_args["length"] == VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["BaseTuningZ"]["position"]):
            vmbt_args["length"] += 1
            vmbt_args["contents"].update(
                {VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["BaseTuningZ"][
                    "position"]: BaseTuningZ})
        else:
            raise IndexError("Index position message isn't coherent.")

        # AdaptiveTuningX:
        if (not isinstance(AdaptiveTuningX, float)):
            raise ValueError("AdaptiveTuningX must be an float.")
        # If AdaptiveTuningX is not a valid value:
        elif (AdaptiveTuningX > VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["AdaptiveTuningX"]["valid_values_scope"]["__max"] or
                AdaptiveTuningX < VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["AdaptiveTuningX"]["valid_values_scope"]["__min"]):
            raise ValueError(
                "AdaptiveTuningX value arg is not valid. Range [{} - {}].".format(
                    VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning[
                        "AdaptiveTuningX"]["valid_values_scope"]["__min"],
                    VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["AdaptiveTuningX"]["valid_values_scope"]["__max"]))
        elif (vmbt_args["length"] == VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["AdaptiveTuningX"]["position"]):
            vmbt_args["length"] += 1
            vmbt_args["contents"].update(
                {VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["AdaptiveTuningX"][
                    "position"]: AdaptiveTuningX})
        else:
            raise IndexError("Index position message isn't coherent.")

        # AdaptiveTuningY:
        if (not isinstance(AdaptiveTuningY, float)):
            raise ValueError("AdaptiveTuningY must be an float.")
        # If AdaptiveTuningY is not a valid value:
        elif (AdaptiveTuningY > VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["AdaptiveTuningY"]["valid_values_scope"]["__max"] or
                AdaptiveTuningY < VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["AdaptiveTuningY"]["valid_values_scope"]["__min"]):
            raise ValueError(
                "AdaptiveTuningY value arg is not valid. Range [{} - {}].".format(
                    VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning[
                        "AdaptiveTuningY"]["valid_values_scope"]["__min"],
                    VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["AdaptiveTuningY"]["valid_values_scope"]["__max"]))
        elif (vmbt_args["length"] == VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["AdaptiveTuningY"]["position"]):
            vmbt_args["length"] += 1
            vmbt_args["contents"].update(
                {VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["AdaptiveTuningY"][
                    "position"]: AdaptiveTuningY})
        else:
            raise IndexError("Index position message isn't coherent.")

        # AdaptiveTuningZ:
        if (not isinstance(AdaptiveTuningZ, float)):
            raise ValueError("AdaptiveTuningZ must be an float.")
        # If AdaptiveTuningZ is not a valid value:
        elif (AdaptiveTuningZ > VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["AdaptiveTuningZ"]["valid_values_scope"]["__max"] or
                AdaptiveTuningZ < VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["AdaptiveTuningZ"]["valid_values_scope"]["__min"]):
            raise ValueError(
                "AdaptiveTuningZ value arg is not valid. Range [{} - {}].".format(
                    VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning[
                        "AdaptiveTuningZ"]["valid_values_scope"]["__min"],
                    VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["AdaptiveTuningZ"]["valid_values_scope"]["__max"]))
        elif (vmbt_args["length"] == VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["AdaptiveTuningZ"]["position"]):
            vmbt_args["length"] += 1
            vmbt_args["contents"].update(
                {VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["AdaptiveTuningZ"][
                    "position"]: AdaptiveTuningZ})
        else:
            raise IndexError("Index position message isn't coherent.")

        # AdaptiveFilteringX:
        if (not isinstance(AdaptiveFilteringX, float)):
            raise ValueError("AdaptiveFilteringX must be an float.")
        # If AdaptiveFilteringX is not a valid value:
        elif (AdaptiveFilteringX > VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["AdaptiveFilteringX"]["valid_values_scope"]["__max"] or
                AdaptiveFilteringX < VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["AdaptiveFilteringX"]["valid_values_scope"]["__min"]):
            raise ValueError(
                "AdaptiveFilteringX value arg is not valid. Range [{} - {}].".format(
                    VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning[
                        "AdaptiveFilteringX"]["valid_values_scope"]["__min"],
                    VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["AdaptiveFilteringX"]["valid_values_scope"]["__max"]))
        elif (vmbt_args["length"] == VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["AdaptiveFilteringX"]["position"]):
            vmbt_args["length"] += 1
            vmbt_args["contents"].update(
                {VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["AdaptiveFilteringX"][
                    "position"]: AdaptiveFilteringX})
        else:
            raise IndexError("Index position message isn't coherent.")

        # AdaptiveFilteringY:
        if (not isinstance(AdaptiveFilteringY, float)):
            raise ValueError("AdaptiveFilteringY must be an float.")
        # If AdaptiveFilteringY is not a valid value:
        elif (AdaptiveFilteringY > VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["AdaptiveFilteringY"]["valid_values_scope"]["__max"] or
                AdaptiveFilteringY < VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["AdaptiveFilteringY"]["valid_values_scope"]["__min"]):
            raise ValueError(
                "AdaptiveFilteringY value arg is not valid. Range [{} - {}].".format(
                    VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning[
                        "AdaptiveFilteringY"]["valid_values_scope"]["__min"],
                    VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["AdaptiveFilteringY"]["valid_values_scope"]["__max"]))
        elif (vmbt_args["length"] == VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["AdaptiveFilteringY"]["position"]):
            vmbt_args["length"] += 1
            vmbt_args["contents"].update(
                {VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["AdaptiveFilteringY"][
                    "position"]: AdaptiveFilteringY})
        else:
            raise IndexError("Index position message isn't coherent.")

        # AdaptiveFilteringZ:
        if (not isinstance(AdaptiveFilteringZ, float)):
            raise ValueError("AdaptiveFilteringZ must be an float.")
        # If AdaptiveFilteringZ is not a valid value:
        elif (AdaptiveFilteringZ > VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["AdaptiveFilteringZ"]["valid_values_scope"]["__max"] or
                AdaptiveFilteringZ < VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["AdaptiveFilteringZ"]["valid_values_scope"]["__min"]):
            raise ValueError(
                "AdaptiveFilteringZ value arg is not valid. Range [{} - {}].".format(
                    VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning[
                        "AdaptiveFilteringZ"]["valid_values_scope"]["__min"],
                    VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["AdaptiveFilteringZ"]["valid_values_scope"]["__max"]))
        elif (vmbt_args["length"] == VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["AdaptiveFilteringZ"]["position"]):
            vmbt_args["length"] += 1
            vmbt_args["contents"].update(
                {VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["AdaptiveFilteringZ"][
                    "position"]: AdaptiveFilteringZ})
        else:
            raise IndexError("Index position message isn't coherent.")

        return VN100_Attitude_Subsystem._write_register(36, vmbt_args)

    @staticmethod
    def get_vpe_magnetometer_basic_tuning():
        '''Gets the "VPE magnetometer basic tuning" register content.
        See section 8.3.2 of VN-100 User Manual (pg. 106).'''
        return VN100_Attitude_Subsystem._read_register(36)

    @staticmethod
    def set_vpe_accelerometer_basic_tuning(
            BaseTuningX,
            BaseTuningY,
            BaseTuningZ,
            AdaptiveTuningX,
            AdaptiveTuningY,
            AdaptiveTuningZ,
            AdaptiveFilteringX,
            AdaptiveFilteringY,
            AdaptiveFilteringZ):
        '''Sets the "VPE accelerometer basic tuning" register content.
        args: (
            BaseTuningX: float with the basic tuning X value.
                For valid values consult on this class the vpe_accelerometer_basic_tuning["BaseTuningX"]["valid_values_scope"] attribute.
            BaseTuningY: float with the basic tuning Y value.
                For valid values consult on this class the vpe_accelerometer_basic_tuning["BaseTuningY"]["valid_values_scope"] attribute.
            BaseTuningZ: float with the basic tuning Z value.
                For valid values consult on this class the vpe_accelerometer_basic_tuning["BaseTuningZ"]["valid_values_scope"] attribute.
            AdaptiveTuningX: float with the adaptive tuning X value.
                For valid values consult on this class the vpe_accelerometer_basic_tuning["AdaptiveTuningX"]["valid_values_scope"] attribute.
            AdaptiveTuningY: float with the adaptive tuning Y value.
                For valid values consult on this class the vpe_accelerometer_basic_tuning["AdaptiveTuningY"]["valid_values_scope"] attribute.
            AdaptiveTuningZ: float with the adaptive tuning Z value.
                For valid values consult on this class the vpe_accelerometer_basic_tuning["AdaptiveTuningZ"]["valid_values_scope"] attribute.
            AdaptiveFilteringX: float with the adaptive filtering X value.
                For valid values consult on this class the vpe_accelerometer_basic_tuning["AdaptiveFilteringX"]["valid_values_scope"] attribute.
            AdaptiveFilteringY: float with the adaptive filtering Y value.
                For valid values consult on this class the vpe_accelerometer_basic_tuning["AdaptiveFilteringY"]["valid_values_scope"] attribute.
            AdaptiveFilteringZ: float with the adaptive filtering Z value.
                For valid values consult on this class the vpe_accelerometer_basic_tuning["AdaptiveFilteringZ"]["valid_values_scope"] attribute.
        )
        See section 8.3.3 of VN-100 User Manual (pg. 107).'''
        # Datagram dictionary
        vabt_args = {
            "length": 0,
            "contents": {}
        }
        # BaseTuningX:
        if (not isinstance(BaseTuningX, float)):
            raise ValueError("BaseTuningX must be an float.")
        # If BaseTuningX is not a valid value:
        elif (BaseTuningX > VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["BaseTuningX"]["valid_values_scope"]["__max"] or
                BaseTuningX < VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["BaseTuningX"]["valid_values_scope"]["__min"]):
            raise ValueError(
                "BaseTuningX value arg is not valid. Range [{} - {}].".format(
                    VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning[
                        "BaseTuningX"]["valid_values_scope"]["__min"],
                    VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["BaseTuningX"]["valid_values_scope"]["__max"]))
        elif (vabt_args["length"] == VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["BaseTuningX"]["position"]):
            vabt_args["length"] += 1
            vabt_args["contents"].update(
                {VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["BaseTuningX"][
                    "position"]: BaseTuningX})
        else:
            raise IndexError("Index position message isn't coherent.")

        # BaseTuningY:
        if (not isinstance(BaseTuningY, float)):
            raise ValueError("BaseTuningY must be an float.")
        # If BaseTuningY is not a valid value:
        elif (BaseTuningY > VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["BaseTuningY"]["valid_values_scope"]["__max"] or
                BaseTuningY < VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["BaseTuningY"]["valid_values_scope"]["__min"]):
            raise ValueError(
                "BaseTuningY value arg is not valid. Range [{} - {}].".format(
                    VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning[
                        "BaseTuningY"]["valid_values_scope"]["__min"],
                    VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["BaseTuningY"]["valid_values_scope"]["__max"]))
        elif (vabt_args["length"] == VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["BaseTuningY"]["position"]):
            vabt_args["length"] += 1
            vabt_args["contents"].update(
                {VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["BaseTuningY"][
                    "position"]: BaseTuningY})
        else:
            raise IndexError("Index position message isn't coherent.")

        # BaseTuningZ:
        if (not isinstance(BaseTuningZ, float)):
            raise ValueError("BaseTuningZ must be an float.")
        # If BaseTuningZ is not a valid value:
        elif (BaseTuningZ > VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["BaseTuningZ"]["valid_values_scope"]["__max"] or
                BaseTuningZ < VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["BaseTuningZ"]["valid_values_scope"]["__min"]):
            raise ValueError(
                "BaseTuningZ value arg is not valid. Range [{} - {}].".format(
                    VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning[
                        "BaseTuningZ"]["valid_values_scope"]["__min"],
                    VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["BaseTuningZ"]["valid_values_scope"]["__max"]))
        elif (vabt_args["length"] == VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["BaseTuningZ"]["position"]):
            vabt_args["length"] += 1
            vabt_args["contents"].update(
                {VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["BaseTuningZ"][
                    "position"]: BaseTuningZ})
        else:
            raise IndexError("Index position message isn't coherent.")

        # AdaptiveTuningX:
        if (not isinstance(AdaptiveTuningX, float)):
            raise ValueError("AdaptiveTuningX must be an float.")
        # If AdaptiveTuningX is not a valid value:
        elif (AdaptiveTuningX > VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["AdaptiveTuningX"]["valid_values_scope"]["__max"] or
                AdaptiveTuningX < VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["AdaptiveTuningX"]["valid_values_scope"]["__min"]):
            raise ValueError(
                "AdaptiveTuningX value arg is not valid. Range [{} - {}].".format(
                    VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning[
                        "AdaptiveTuningX"]["valid_values_scope"]["__min"],
                    VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["AdaptiveTuningX"]["valid_values_scope"]["__max"]))
        elif (vabt_args["length"] == VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["AdaptiveTuningX"]["position"]):
            vabt_args["length"] += 1
            vabt_args["contents"].update(
                {VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["AdaptiveTuningX"][
                    "position"]: AdaptiveTuningX})
        else:
            raise IndexError("Index position message isn't coherent.")

        # AdaptiveTuningY:
        if (not isinstance(AdaptiveTuningY, float)):
            raise ValueError("AdaptiveTuningY must be an float.")
        # If AdaptiveTuningY is not a valid value:
        elif (AdaptiveTuningY > VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["AdaptiveTuningY"]["valid_values_scope"]["__max"] or
                AdaptiveTuningY < VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["AdaptiveTuningY"]["valid_values_scope"]["__min"]):
            raise ValueError(
                "AdaptiveTuningY value arg is not valid. Range [{} - {}].".format(
                    VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning[
                        "AdaptiveTuningY"]["valid_values_scope"]["__min"],
                    VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["AdaptiveTuningY"]["valid_values_scope"]["__max"]))
        elif (vabt_args["length"] == VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["AdaptiveTuningY"]["position"]):
            vabt_args["length"] += 1
            vabt_args["contents"].update(
                {VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["AdaptiveTuningY"][
                    "position"]: AdaptiveTuningY})
        else:
            raise IndexError("Index position message isn't coherent.")

        # AdaptiveTuningZ:
        if (not isinstance(AdaptiveTuningZ, float)):
            raise ValueError("AdaptiveTuningZ must be an float.")
        # If AdaptiveTuningZ is not a valid value:
        elif (AdaptiveTuningZ > VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["AdaptiveTuningZ"]["valid_values_scope"]["__max"] or
                AdaptiveTuningZ < VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["AdaptiveTuningZ"]["valid_values_scope"]["__min"]):
            raise ValueError(
                "AdaptiveTuningZ value arg is not valid. Range [{} - {}].".format(
                    VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning[
                        "AdaptiveTuningZ"]["valid_values_scope"]["__min"],
                    VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["AdaptiveTuningZ"]["valid_values_scope"]["__max"]))
        elif (vabt_args["length"] == VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["AdaptiveTuningZ"]["position"]):
            vabt_args["length"] += 1
            vabt_args["contents"].update(
                {VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["AdaptiveTuningZ"][
                    "position"]: AdaptiveTuningZ})
        else:
            raise IndexError("Index position message isn't coherent.")

        # AdaptiveFilteringX:
        if (not isinstance(AdaptiveFilteringX, float)):
            raise ValueError("AdaptiveFilteringX must be an float.")
        # If AdaptiveFilteringX is not a valid value:
        elif (AdaptiveFilteringX > VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["AdaptiveFilteringX"]["valid_values_scope"]["__max"] or
                AdaptiveFilteringX < VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["AdaptiveFilteringX"]["valid_values_scope"]["__min"]):
            raise ValueError(
                "AdaptiveFilteringX value arg is not valid. Range [{} - {}].".format(
                    VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning[
                        "AdaptiveFilteringX"]["valid_values_scope"]["__min"],
                    VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["AdaptiveFilteringX"]["valid_values_scope"]["__max"]))
        elif (vabt_args["length"] == VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["AdaptiveFilteringX"]["position"]):
            vabt_args["length"] += 1
            vabt_args["contents"].update(
                {VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["AdaptiveFilteringX"][
                    "position"]: AdaptiveFilteringX})
        else:
            raise IndexError("Index position message isn't coherent.")

        # AdaptiveFilteringY:
        if (not isinstance(AdaptiveFilteringY, float)):
            raise ValueError("AdaptiveFilteringY must be an float.")
        # If AdaptiveFilteringY is not a valid value:
        elif (AdaptiveFilteringY > VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["AdaptiveFilteringY"]["valid_values_scope"]["__max"] or
                AdaptiveFilteringY < VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["AdaptiveFilteringY"]["valid_values_scope"]["__min"]):
            raise ValueError(
                "AdaptiveFilteringY value arg is not valid. Range [{} - {}].".format(
                    VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning[
                        "AdaptiveFilteringY"]["valid_values_scope"]["__min"],
                    VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["AdaptiveFilteringY"]["valid_values_scope"]["__max"]))
        elif (vabt_args["length"] == VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["AdaptiveFilteringY"]["position"]):
            vabt_args["length"] += 1
            vabt_args["contents"].update(
                {VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["AdaptiveFilteringY"][
                    "position"]: AdaptiveFilteringY})
        else:
            raise IndexError("Index position message isn't coherent.")

        # AdaptiveFilteringZ:
        if (not isinstance(AdaptiveFilteringZ, float)):
            raise ValueError("AdaptiveFilteringZ must be an float.")
        # If AdaptiveFilteringZ is not a valid value:
        elif (AdaptiveFilteringZ > VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["AdaptiveFilteringZ"]["valid_values_scope"]["__max"] or
                AdaptiveFilteringZ < VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["AdaptiveFilteringZ"]["valid_values_scope"]["__min"]):
            raise ValueError(
                "AdaptiveFilteringZ value arg is not valid. Range [{} - {}].".format(
                    VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning[
                        "AdaptiveFilteringZ"]["valid_values_scope"]["__min"],
                    VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["AdaptiveFilteringZ"]["valid_values_scope"]["__max"]))
        elif (vabt_args["length"] == VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["AdaptiveFilteringZ"]["position"]):
            vabt_args["length"] += 1
            vabt_args["contents"].update(
                {VN100_Attitude_Subsystem.vpe_accelerometer_basic_tuning["AdaptiveFilteringZ"][
                    "position"]: AdaptiveFilteringZ})
        else:
            raise IndexError("Index position message isn't coherent.")

        return VN100_Attitude_Subsystem._write_register(38, vabt_args)

    @staticmethod
    def get_vpe_accelerometer_basic_tuning():
        '''Gets the "VPE accelerometer basic tuning" register content.
        See section 8.3.3 of VN-100 User Manual (pg. 107).'''
        return VN100_Attitude_Subsystem._read_register(38)
