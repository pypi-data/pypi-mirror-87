# VectorNav VN-100's Velocity Aiding section.
# See section 10 of VN-100 User Manual (pg. 116).
# Document number: UM001 v2.05.
# Firmware version: 2.0.0.0.
# This is the Python 3 version.
# Author of this script: Andrés Eduardo Torres Hernández.


from .register_manager import VN100_Register_Manager
from .resources import C8bit_cksm
from .logger import init_logger


class VN100_Velocity_Aiding(VN100_Register_Manager):
    '''VectorNav VN-100's Velocity Aiding section.
    See section 10 of VN-100 User Manual (pg. 116).
    Document number: UM001 v2.05.
    Firmware version: 2.0.0.0.'''
    # Register variables:
    velocity_compensation_control = {
        "Mode": {
            "position": 0,
            "data_type": "uint8",
            "unit": "-",
            "valid_values_scope": {
                    "DISABLED": 0,
                    "BODY_MEASUREMENT": 1
            }
        },
        "VelocityTuning": {
            "position": 1,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {
                    "min": 0,
                    "max": 10
            }
        },
        "RateTuning": {
            "position": 2,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {
                    "min": 0,
                    "max": 10
            }
        }
    }

    velocity_compensation_measurement = {
        "VelocityX": {
            "position": 0,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {

            }
        },
        "VelocityY": {
            "position": 1,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {

            }
        },
        "VelocityZ": {
            "position": 2,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {

            }
        }
    }

    _logger = init_logger(__name__)

    
    # Methods:
    @staticmethod
    def set_velocity_compensation_control(
            Mode,
            VelocityTuning,
            RateTuning):
        '''Sets the "Velocity compensation control" register content.
        args: (
            Mode: string with the type of velocity compensation performed by the VPE.
                For valid values consult on this class the velocity_compensation_control["Mode"]["valid_values_scope"].keys()): attribute.
            VelocityTuning: float with the tuning parameter for the velocity measurement. Range [0 - 10].
            RateTuning: float with the tuning parameter for the angular rate measurement. Range [0 - 10].
        )
        See section 10.2.1 of VN-100 User Manual (pg. 120).'''
        # Datagram dictionary
        vcc_args = {
            "length": 0,
            "contents": {}
        }
        # Mode:
        if (not isinstance(Mode, str)):
            raise ValueError("Mode must be a string.")
        # If Mode is not a valid value:
        elif (Mode not in
                VN100_Velocity_Aiding.velocity_compensation_control["Mode"]["valid_values_scope"].keys()):
            raise ValueError(
                "Mode value arg is not valid. See table 49 from VN-100 User Manual at pg. 120 about valid values.")
        elif (vcc_args["length"] == VN100_Velocity_Aiding.velocity_compensation_control["Mode"]["position"]):
            vcc_args["length"] += 1
            vcc_args["contents"].update(
                {VN100_Velocity_Aiding.velocity_compensation_control["Mode"][
                    "position"]: VN100_Velocity_Aiding.velocity_compensation_control["Mode"]["valid_values_scope"][Mode]})
        else:
            raise IndexError("Index position message isn't coherent.")

        # VelocityTuning:
        if (not isinstance(VelocityTuning, float)):
            raise ValueError("VelocityTuning must be an float.")
        # If VelocityTuning is not a valid value:
        elif (VelocityTuning > VN100_Velocity_Aiding.velocity_compensation_control["VelocityTuning"]["valid_values_scope"]["max"] or
                VelocityTuning < VN100_Velocity_Aiding.velocity_compensation_control["VelocityTuning"]["valid_values_scope"]["min"]):
            raise ValueError(
                "VelocityTuning value arg is not valid. Range [{} - {}].".format(
                    VN100_Velocity_Aiding.velocity_compensation_control[
                        "VelocityTuning"]["valid_values_scope"]["min"],
                    VN100_Velocity_Aiding.velocity_compensation_control["VelocityTuning"]["valid_values_scope"]["max"]))
        elif (vcc_args["length"] == VN100_Velocity_Aiding.velocity_compensation_control["VelocityTuning"]["position"]):
            vcc_args["length"] += 1
            vcc_args["contents"].update(
                {VN100_Velocity_Aiding.velocity_compensation_control["VelocityTuning"][
                    "position"]: VelocityTuning})
        else:
            raise IndexError("Index position message isn't coherent.")

        # RateTuning:
        if (not isinstance(RateTuning, float)):
            raise ValueError("RateTuning must be an float.")
        # If RateTuning is not a valid value:
        elif (RateTuning > VN100_Velocity_Aiding.velocity_compensation_control["RateTuning"]["valid_values_scope"]["max"] or
                RateTuning < VN100_Velocity_Aiding.velocity_compensation_control["RateTuning"]["valid_values_scope"]["min"]):
            raise ValueError(
                "RateTuning value arg is not valid. Range [{} - {}].".format(
                    VN100_Velocity_Aiding.velocity_compensation_control[
                        "RateTuning"]["valid_values_scope"]["min"],
                    VN100_Velocity_Aiding.velocity_compensation_control["RateTuning"]["valid_values_scope"]["max"]))
        elif (vcc_args["length"] == VN100_Velocity_Aiding.velocity_compensation_control["RateTuning"]["position"]):
            vcc_args["length"] += 1
            vcc_args["contents"].update(
                {VN100_Velocity_Aiding.velocity_compensation_control["RateTuning"][
                    "position"]: RateTuning})
        else:
            raise IndexError("Index position message isn't coherent.")

        return VN100_Velocity_Aiding._write_register(51, vcc_args)

    @staticmethod
    def get_velocity_compensation_control():
        '''Gets the "Velocity compensation control" register content.
        See section 10.2.1 of VN-100 User Manual (pg. 120).'''
        return VN100_Velocity_Aiding._read_register(51)

    @staticmethod
    def set_velocity_compensation_measurement(
            VelocityX,
            VelocityY=0.0,
            VelocityZ=0.0):
        '''Sets the "Velocity compensation measurement" register content.
        args: (
            VelocityX: float with the velocity in the X-axis measured in the sensor frame.
            VelocityY: float with the velocity in the Y-axis measured in the sensor frame.
            VelocityZ: float with the velocity in the Z-axis measured in the sensor frame.
        )
        Note: if you have a scalar measurement, only set the VelocityX value.
        See section 10.3.1 of VN-100 User Manual (pg. 121).'''
        # Datagram dictionary
        vcm_args = {
            "length": 0,
            "contents": {}
        }

        # VelocityX:
        if (not isinstance(VelocityX, float)):
            raise ValueError("VelocityX must be a float.")
        elif (vcm_args["length"] == VN100_Velocity_Aiding.velocity_compensation_measurement["VelocityX"]["position"]):
            vcm_args["length"] += 1
            vcm_args["contents"].update(
                {VN100_Velocity_Aiding.velocity_compensation_measurement["VelocityX"][
                    "position"]: VelocityX})
        else:
            raise IndexError("Index position message isn't coherent.")

        # VelocityY:
        if (not isinstance(VelocityY, float)):
            raise ValueError("VelocityY must be an float.")
        elif (vcm_args["length"] == VN100_Velocity_Aiding.velocity_compensation_measurement["VelocityY"]["position"]):
            vcm_args["length"] += 1
            vcm_args["contents"].update(
                {VN100_Velocity_Aiding.velocity_compensation_measurement["VelocityY"][
                    "position"]: VelocityY})
        else:
            raise IndexError("Index position message isn't coherent.")

        # VelocityZ:
        if (not isinstance(VelocityZ, float)):
            raise ValueError("VelocityZ must be an float.")
        elif (vcm_args["length"] == VN100_Velocity_Aiding.velocity_compensation_measurement["VelocityZ"]["position"]):
            vcm_args["length"] += 1
            vcm_args["contents"].update(
                {VN100_Velocity_Aiding.velocity_compensation_measurement["VelocityZ"][
                    "position"]: VelocityZ})
        else:
            raise IndexError("Index position message isn't coherent.")

        return VN100_Velocity_Aiding._write_register(50, vcm_args)

    @staticmethod
    def get_velocity_compensation_measurement():
        '''Gets the "Velocity compensation measurement" register content.
        See section 10.3.1 of VN-100 User Manual (pg. 121).'''
        return VN100_Velocity_Aiding._read_register(50)