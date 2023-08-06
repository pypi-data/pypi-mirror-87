# VectorNav VN-100's Hard/Soft Iron Estimator subsystem
# See section 9 of VN-100 User Manual (pg. 95).
# Document number: UM001 v2.05.
# Firmware version: 2.0.0.0.
# This is the Python 3 version.
# Author of this script: Andrés Eduardo Torres Hernández.


from .register_manager import VN100_Register_Manager
from .resources import C8bit_cksm
from .logger import init_logger


class VN100_HSIE_Subsystem(VN100_Register_Manager):
    '''VectorNav VN-100's Hard/Soft Iron Estimator subsystem
    See section 9 of VN-100 User Manual (pg. 109).
    Document number: UM001 v2.05.
    Firmware version: 2.0.0.0.'''
    # Register variables:
    magnetometer_calibration_control = {
        "HSIMode": {
            "position": 0,
            "data_type": "uint8",
            "unit": "-",
            "valid_values_scope": {
                    "OFF": 0,
                    "RUN": 1,
                    "RESET": 2
            }
        },
        "HSIOutput": {
            "position": 1,
            "data_type": "uint8",
            "unit": "-",
            "valid_values_scope": {
                    "NO": 0,
                    "USE": 1
            }
        },
        "ConvergeRate": {
            "position": 2,
            "data_type": "uint8",
            "unit": "-",
            "valid_values_scope": {
                    "min": 1,
                    "max": 5
            }
        }
    }

    calculated_magnetometer_calibration = {
        "C[0,0]": {
            "position": 0,
            "data_type": "float",
            "unit": "-"
        },
        "C[0,1]": {
            "position": 1,
            "data_type": "float",
            "unit": "-"
        },
        "C[0,2]": {
            "position": 2,
            "data_type": "float",
            "unit": "-"
        },
        "C[1,0]": {
            "position": 3,
            "data_type": "float",
            "unit": "-"
        },
        "C[1,1]": {
            "position": 4,
            "data_type": "float",
            "unit": "-"
        },
        "C[1,2]": {
            "position": 5,
            "data_type": "float",
            "unit": "-"
        },
        "C[2,0]": {
            "position": 6,
            "data_type": "float",
            "unit": "-"
        },
        "C[2,1]": {
            "position": 7,
            "data_type": "float",
            "unit": "-"
        },
        "C[2,2]": {
            "position": 8,
            "data_type": "float",
            "unit": "-"
        },
        "B[0]": {
            "position": 9,
            "data_type": "float",
            "unit": "-"
        },
        "B[1]": {
            "position": 10,
            "data_type": "float",
            "unit": "-"
        },
        "B[2]": {
            "position": 11,
            "data_type": "float",
            "unit": "-"
        }
    }

    _logger = init_logger(__name__)

    # Methods:
    @staticmethod
    def set_magnetometer_calibration_control(
            HSIMode,
            HSIOutput,
            ConvergeRate):
        '''Sets the "Magnetometer calibration control" register content.
        args: (
            HSIMode: string with the operation mode od HSI estimator algorithm.
                For valid values consult on this class the magnetometer_calibration_control["HSIMode"]["valid_values_scope"].keys()): attribute.
            HSIOutput: string with if HSI estimator algorithm is applied to the magnetic measurements.
                For valid values consult on this class the magnetometer_calibration_control["HSIOutput"]["valid_values_scope"].keys()): attribute.
            ConvergeRate: integer with the relative accuracy convergency to new solutions from the HSI estimator. Range [1 - 5].
        )
        See section 9.1.1 of VN-100 User Manual (pg. 109).'''
        # Datagram dictionary
        mcc_args = {
            "length": 0,
            "contents": {}
        }
        # HSIMode:
        if (not isinstance(HSIMode, str)):
            raise ValueError("HSIMode must be a string.")
        # If HSIMode is not a valid value:
        elif (HSIMode not in
                VN100_HSIE_Subsystem.magnetometer_calibration_control["HSIMode"]["valid_values_scope"].keys()):
            raise ValueError(
                "HSIMode value arg is not valid. See table 47 from VN-100 User Manual at pg. 109 about valid values.")
        elif (mcc_args["length"] == VN100_HSIE_Subsystem.magnetometer_calibration_control["HSIMode"]["position"]):
            mcc_args["length"] += 1
            mcc_args["contents"].update(
                {VN100_HSIE_Subsystem.magnetometer_calibration_control["HSIMode"][
                    "position"]: VN100_HSIE_Subsystem.magnetometer_calibration_control["HSIMode"]["valid_values_scope"][HSIMode]})
        else:
            raise IndexError("Index position message isn't coherent.")

        # HSIOutput:
        if (not isinstance(HSIOutput, str)):
            raise ValueError("HSIOutput must be a string.")
        # If HSIOutput is not a valid value:
        elif (HSIOutput not in
                VN100_HSIE_Subsystem.magnetometer_calibration_control["HSIOutput"]["valid_values_scope"].keys()):
            raise ValueError(
                "HSIOutput value arg is not valid. See table 48 from VN-100 User Manual at pg. 109 about valid values.")
        elif (mcc_args["length"] == VN100_HSIE_Subsystem.magnetometer_calibration_control["HSIOutput"]["position"]):
            mcc_args["length"] += 1
            mcc_args["contents"].update(
                {VN100_HSIE_Subsystem.magnetometer_calibration_control["HSIOutput"][
                    "position"]: VN100_HSIE_Subsystem.magnetometer_calibration_control["HSIOutput"]["valid_values_scope"][HSIOutput]})
        else:
            raise IndexError("Index position message isn't coherent.")

        # ConvergeRate:
        if (not isinstance(ConvergeRate, int)):
            raise ValueError("ConvergeRate must be an integer.")
        # If ConvergeRate is not a valid value:
        elif (ConvergeRate > VN100_HSIE_Subsystem.magnetometer_calibration_control["ConvergeRate"]["valid_values_scope"]["max"] or
                ConvergeRate < VN100_HSIE_Subsystem.magnetometer_calibration_control["ConvergeRate"]["valid_values_scope"]["min"]):
            raise ValueError(
                "ConvergeRate value arg is not valid. Range [{} - {}].".format(
                    VN100_HSIE_Subsystem.magnetometer_calibration_control[
                        "ConvergeRate"]["valid_values_scope"]["min"],
                    VN100_HSIE_Subsystem.magnetometer_calibration_control["ConvergeRate"]["valid_values_scope"]["max"]))
        elif (mcc_args["length"] == VN100_HSIE_Subsystem.magnetometer_calibration_control["ConvergeRate"]["position"]):
            mcc_args["length"] += 1
            mcc_args["contents"].update(
                {VN100_HSIE_Subsystem.magnetometer_calibration_control["ConvergeRate"][
                    "position"]: ConvergeRate})
        else:
            raise IndexError("Index position message isn't coherent.")
        
        return VN100_HSIE_Subsystem._write_register(44, mcc_args)

    @staticmethod
    def get_magnetometer_calibration_control():
        '''Gets the "Magnetometer calibration control" register content.
        See section 9.1.1 of VN-100 User Manual (pg. 109).'''
        return VN100_HSIE_Subsystem._read_register(44)
    
    @staticmethod
    def get_calculated_magnetometer_calibration():
        '''Gets the "Calculated Magnetometer calibration" register content.
        See section 9.2.1 of VN-100 User Manual (pg. 110).'''
        return VN100_HSIE_Subsystem._read_register(47)