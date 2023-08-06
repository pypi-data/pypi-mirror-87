# VectorNav VN-100's IMU subsystem
# See section 7 of VN-100 User Manual (pg. 81).
# Document number: UM001 v2.05.
# Firmware version: 2.0.0.0.
# This is the Python 3 version.
# Author of this script: Andrés Eduardo Torres Hernández.


from .register_manager import VN100_Register_Manager
from .resources import C8bit_cksm
from .logger import init_logger


class VN100_IMU_Subsystem(VN100_Register_Manager):
    '''VectorNav VN-100's IMU subsystem
    See section 7 of VN-100 User Manual (pg. 81).
    Document number: UM001 v2.05.
    Firmware version: 2.0.0.0.'''
    # Register variables:
    measurements = {
        "MagX": {
            "position": 0,
            "data_type": "float",
            "unit": "Gauss",
            "valid_values_scope": {}
        },
        "MagY": {
            "position": 1,
            "data_type": "float",
            "unit": "Gauss",
            "valid_values_scope": {}
        },
        "MagZ": {
            "position": 2,
            "data_type": "float",
            "unit": "Gauss",
            "valid_values_scope": {}
        },
        "AccelX": {
            "position": 3,
            "data_type": "float",
            "unit": "m/s^2",
            "valid_values_scope": {}
        },
        "AccelY": {
            "position": 4,
            "data_type": "float",
            "unit": "m/s^2",
            "valid_values_scope": {}
        },
        "AccelZ": {
            "position": 5,
            "data_type": "float",
            "unit": "m/s^2",
            "valid_values_scope": {}
        },
        "GyroX": {
            "position": 6,
            "data_type": "float",
            "unit": "rad/s",
            "valid_values_scope": {}
        },
        "GyroY": {
            "position": 7,
            "data_type": "float",
            "unit": "rad/s",
            "valid_values_scope": {}
        },
        "GyroZ": {
            "position": 8,
            "data_type": "float",
            "unit": "rad/s",
            "valid_values_scope": {}
        },
        "Temp": {
            "position": 9,
            "data_type": "float",
            "unit": "°C",
            "valid_values_scope": {}
        },
        "Pressure": {
            "position": 10,
            "data_type": "float",
            "unit": "KPa",
            "valid_values_scope": {}
        },
    }

    delta_theta_delta_velocity = {
        "DeltaTime": {
            "position": 0,
            "data_type": "float",
            "unit": "sec",
            "valid_values_scope": {}
        },
        "DeltaThetaX": {
            "position": 1,
            "data_type": "float",
            "unit": "deg",
            "valid_values_scope": {}
        },
        "DeltaThetaY": {
            "position": 2,
            "data_type": "float",
            "unit": "deg",
            "valid_values_scope": {}
        },
        "DeltaThetaZ": {
            "position": 3,
            "data_type": "float",
            "unit": "deg",
            "valid_values_scope": {}
        },
        "DeltaVelocityX": {
            "position": 4,
            "data_type": "float",
            "unit": "m/s",
            "valid_values_scope": {}
        },
        "DeltaVelocityY": {
            "position": 5,
            "data_type": "float",
            "unit": "m/s",
            "valid_values_scope": {}
        },
        "DeltaVelocityZ": {
            "position": 6,
            "data_type": "float",
            "unit": "m/s",
            "valid_values_scope": {}
        },
    }

    magnetometer_compensation = {
        "C[0,0]": {
            "position": 0,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {}
        },
        "C[0,1]": {
            "position": 1,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {}
        },
        "C[0,2]": {
            "position": 2,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {}
        },
        "C[1,0]": {
            "position": 3,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {}
        },
        "C[1,1]": {
            "position": 4,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {}
        },
        "C[1,2]": {
            "position": 5,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {}
        },
        "C[2,0]": {
            "position": 6,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {}
        },
        "C[2,1]": {
            "position": 7,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {}
        },
        "C[2,2]": {
            "position": 8,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {}
        },
        "B[0]": {
            "position": 9,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {}
        },
        "B[1]": {
            "position": 10,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {}
        },
        "B[2]": {
            "position": 11,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {}
        }
    }

    acceleration_compensation = {
        "C[0,0]": {
            "position": 0,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {}
        },
        "C[0,1]": {
            "position": 1,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {}
        },
        "C[0,2]": {
            "position": 2,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {}
        },
        "C[1,0]": {
            "position": 3,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {}
        },
        "C[1,1]": {
            "position": 4,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {}
        },
        "C[1,2]": {
            "position": 5,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {}
        },
        "C[2,0]": {
            "position": 6,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {}
        },
        "C[2,1]": {
            "position": 7,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {}
        },
        "C[2,2]": {
            "position": 8,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {}
        },
        "B[0]": {
            "position": 9,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {}
        },
        "B[1]": {
            "position": 10,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {}
        },
        "B[2]": {
            "position": 11,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {}
        }
    }

    gyro_compensation = {
        "C[0,0]": {
            "position": 0,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {}
        },
        "C[0,1]": {
            "position": 1,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {}
        },
        "C[0,2]": {
            "position": 2,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {}
        },
        "C[1,0]": {
            "position": 3,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {}
        },
        "C[1,1]": {
            "position": 4,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {}
        },
        "C[1,2]": {
            "position": 5,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {}
        },
        "C[2,0]": {
            "position": 6,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {}
        },
        "C[2,1]": {
            "position": 7,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {}
        },
        "C[2,2]": {
            "position": 8,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {}
        },
        "B[0]": {
            "position": 9,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {}
        },
        "B[1]": {
            "position": 10,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {}
        },
        "B[2]": {
            "position": 11,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {}
        }
    }

    reference_frame_rotation = {
        "C[0,0]": {
            "position": 0,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {}
        },
        "C[0,1]": {
            "position": 1,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {}
        },
        "C[0,2]": {
            "position": 2,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {}
        },
        "C[1,0]": {
            "position": 3,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {}
        },
        "C[1,1]": {
            "position": 4,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {}
        },
        "C[1,2]": {
            "position": 5,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {}
        },
        "C[2,0]": {
            "position": 6,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {}
        },
        "C[2,1]": {
            "position": 7,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {}
        },
        "C[2,2]": {
            "position": 8,
            "data_type": "float",
            "unit": "-",
            "valid_values_scope": {}
        }
    }

    filter_modes = {
        "NULL": 0,
        "UNCOMPENSATED": 1,
        "COMPENSATED": 2,
        "BOTH": 3
    }

    filtering_configuration = {
        "MagWindowSize": {
            "position": 0,
            "data_type": "uint16",
            "unit": "-",
            "valid_values_scope": {
                "__min": 0,
                "__max": 8
            }
        },
        "AccelWindowSize": {
            "position": 1,
            "data_type": "uint16",
            "unit": "-",
            "valid_values_scope": {
                "__min": 0,
                "__max": 8
            }
        },
        "GyroWindowSize": {
            "position": 2,
            "data_type": "uint16",
            "unit": "-",
            "valid_values_scope": {
                "__min": 0,
                "__max": 8
            }
        },
        "TempWindowSize": {
            "position": 3,
            "data_type": "uint16",
            "unit": "-",
            "valid_values_scope": {
                "__min": 0,
                "__max": 8
            }
        },
        "PresWindowSize": {
            "position": 4,
            "data_type": "uint16",
            "unit": "-",
            "valid_values_scope": {
                "__min": 0,
                "__max": 8
            }
        },
        "MagFilterMode": {
            "position": 5,
            "data_type": "uint8",
            "unit": "-",
            "valid_values_scope": filter_modes
        },
        "AccelFilterMode": {
            "position": 6,
            "data_type": "uint8",
            "unit": "-",
            "valid_values_scope": filter_modes
        },
        "GyroFilterMode": {
            "position": 7,
            "data_type": "uint8",
            "unit": "-",
            "valid_values_scope": filter_modes
        },
        "TempFilterMode": {
            "position": 8,
            "data_type": "uint8",
            "unit": "-",
            "valid_values_scope": filter_modes
        },
        "PresFilterMode": {
            "position": 9,
            "data_type": "uint8",
            "unit": "-",
            "valid_values_scope": filter_modes
        }
    }

    delta_theta_delta_velocity_configuration = {
        "IntegrationFrame": {
            "position": 0,
            "data_type": "uint8",
            "unit": "-",
            "valid_values_scope": {
                    "BODY_FRAME": 0,
                    "NED_FRAME": 1
            }
        },
        "GyroCompensation": {
            "position": 1,
            "data_type": "uint8",
            "unit": "-",
            "valid_values_scope": {
                    "NONE": 0,
                    "BIAS": 1
            }
        },
        "AccelCompensation": {
            "position": 2,
            "data_type": "uint16",
            "unit": "-",
            "valid_values_scope": {
                    "NONE": 0,
                    "BIAS": 1
            }
        }
    }

    IMU_RATE = 800

    _logger = init_logger(__name__)

    # Methods:
    @staticmethod
    def get_measurements():
        '''Gets the "IMU measurements" register content.
        See section 7.1.1 of VN-100 User Manual (pg. 81).'''
        return VN100_IMU_Subsystem._read_register(54)

    @staticmethod
    def get_delta_theta_delta_velocity():
        '''Gets the "Delta theta and delta velocity" register content.
        This means that are the onboard coning and sculling algorithm output values.
        See section 7.1.2 of VN-100 User Manual (pg. 82).'''
        return VN100_IMU_Subsystem._read_register(80)

    @staticmethod
    def set_magnetometer_compensation():
        '''Sets the "Magnetometer compensation" register content.
        See section 7.2.1 of VN-100 User Manual (pg. 83).'''
        VN100_IMU_Subsystem._logger.warning(
            "This method isn't implemented yet.")

    @staticmethod
    def get_magnetometer_compensation():
        '''Gets the "Magnetometer compensation" register content.
        See section 7.2.1 of VN-100 User Manual (pg. 83).'''
        return VN100_IMU_Subsystem._read_register(23)

    @staticmethod
    def set_acceleration_compensation():
        '''Sets the "Acceleration compensation" register content.
        See section 7.2.2 of VN-100 User Manual (pg. 84).'''
        VN100_IMU_Subsystem._logger.warning(
            "This method isn't implemented yet.")

    @staticmethod
    def get_acceleration_compensation():
        '''Gets the "Magnetometer compensation" register content.
        See section 7.2.2 of VN-100 User Manual (pg. 84).'''
        return VN100_IMU_Subsystem._read_register(25)

    @staticmethod
    def set_gyro_compensation():
        '''Sets the "Acceleration compensation" register content.
        See section 7.2.3 of VN-100 User Manual (pg. 85).'''
        VN100_IMU_Subsystem._logger.warning(
            "This method isn't implemented yet.")

    @staticmethod
    def get_gyro_compensation():
        '''Gets the "Magnetometer compensation" register content.
        See section 7.2.3 of VN-100 User Manual (pg. 85).'''
        return VN100_IMU_Subsystem._read_register(84)

    @staticmethod
    def set_reference_frame_rotation():
        '''Sets the "Reference frame rotation" register content.
        See section 7.2.4 of VN-100 User Manual (pg. 86).'''
        VN100_IMU_Subsystem._logger.warning(
            "This method isn't implemented yet.")

    @staticmethod
    def get_reference_frame_rotation():
        '''Gets the "Reference frame rotation" register content.
        See section 7.2.4 of VN-100 User Manual (pg. 86).'''
        return VN100_IMU_Subsystem._read_register(26)

    @staticmethod
    def set_filtering_configuration(
            MagWindowSize,
            AccelWindowSize,
            GyroWindowSize,
            TempWindowSize,
            PresWindowSize,
            MagFilterMode,
            AccelFilterMode,
            GyroFilterMode,
            TempFilterMode,
            PresFilterMode):
        '''Sets the "IMU Filtering configuration" register content.
        args: (
            MagWindowSize: integer with window size value for magnetometer.
                For valid values consult on this class the filtering_configuration["MagWindowSize"]["valid_values_scope"] attribute.
            AccelWindowSize: integer with window size value for accelerometer.
                For valid values consult on this class the filtering_configuration["AccelWindowSize"]["valid_values_scope"] attribute.
            GyroWindowSize: integer with window size value for gyro.
                For valid values consult on this class the filtering_configuration["GyroWindowSize"]["valid_values_scope"] attribute.
            TempWindowSize: integer with window size value for thermometer.
                For valid values consult on this class the filtering_configuration["TempWindowSize"]["valid_values_scope"] attribute.
            PresWindowSize: integer with window size value for barometer.
                For valid values consult on this class the filtering_configuration["PresWindowSize"]["valid_values_scope"] attribute.
            MagFilterMode: string with the IMU filter mode for magnetometer.
                For valid values consult on this class the filtering_configuration["MagFilterMode"]["valid_values_scope"].keys(): attribute.
            AccelFilterMode: string with the IMU filter mode for accelerometer.
                For valid values consult on this class the filtering_configuration["AccelFilterMode"].keys(): attribute.
            GyroFilterMode: string with the IMU filter mode for gyro.
                For valid values consult on this class the filtering_configuration["GyroFilterMode"].keys(): attribute.
            TempFilterMode: string with the IMU filter mode for thermometer.
                For valid values consult on this class the filtering_configuration["TempFilterMode"].keys(): attribute.
            PresFilterMode: string with the IMU filter mode for barometer.
                For valid values consult on this class the filtering_configuration["PresFilterMode"].keys(): attribute.
        )
        See section 7.2.5 of VN-100 User Manual (pg. 87).'''
        # Datagram dictionary
        ifc_args = {
            "length": 0,
            "contents": {}
        }
        # MagWindowSize:
        if (not isinstance(MagWindowSize, int)):
            raise ValueError("MagWindowSize must be an integer.")
        # If MagWindowSize is not a valid value:
        elif (MagWindowSize > VN100_IMU_Subsystem.IMU_RATE or
                MagWindowSize < 0):
            raise ValueError(
                "MagWindowSize value arg is not valid. Range [0 - {}].".format(
                    VN100_IMU_Subsystem.IMU_RATE))
        else:
            ifc_args["length"] += 1
            ifc_args["contents"].update(
                {0: MagWindowSize})

        # AccelWindowSize:
        if (not isinstance(AccelWindowSize, int)):
            raise ValueError("AccelWindowSize must be an integer.")
        # If AccelWindowSize is not a valid value:
        elif (AccelWindowSize > VN100_IMU_Subsystem.IMU_RATE or
                AccelWindowSize < 0):
            raise ValueError(
                "AccelWindowSize value arg is not valid. Range [0 - {}].".format(
                    VN100_IMU_Subsystem.IMU_RATE
                ))
        else:
            ifc_args["length"] += 1
            ifc_args["contents"].update(
                {1: AccelWindowSize})

        # GyroWindowSize:
        if (not isinstance(GyroWindowSize, int)):
            raise ValueError("GyroWindowSize must be an integer.")
        # If GyroWindowSize is not a valid value:
        elif (GyroWindowSize > VN100_IMU_Subsystem.IMU_RATE or
                GyroWindowSize < 0):
            raise ValueError(
                "GyroWindowSize value arg is not valid. Range [0 - {}].".format(
                    VN100_IMU_Subsystem.IMU_RATE
                ))
        else:
            ifc_args["length"] += 1
            ifc_args["contents"].update(
                {2: GyroWindowSize})

        # TempWindowSize:
        if (not isinstance(TempWindowSize, int)):
            raise ValueError("TempWindowSize must be an integer.")
        # If TempWindowSize is not a valid value:
        elif (TempWindowSize > VN100_IMU_Subsystem.IMU_RATE or
                TempWindowSize < 0):
            raise ValueError(
                "TempWindowSize value arg is not valid. Range [0 - {}].".format(
                    VN100_IMU_Subsystem.IMU_RATE
                ))
        else:
            ifc_args["length"] += 1
            ifc_args["contents"].update(
                {3: TempWindowSize})

        # PresWindowSize:
        if (not isinstance(PresWindowSize, int)):
            raise ValueError("PresWindowSize must be an integer.")
        # If PresWindowSize is not a valid value:
        elif (PresWindowSize > VN100_IMU_Subsystem.IMU_RATE or
                PresWindowSize < 0):
            raise ValueError(
                "PresWindowSize value arg is not valid. Range [0 - {}].".format(
                    VN100_IMU_Subsystem.IMU_RATE
                ))
        else:
            ifc_args["length"] += 1
            ifc_args["contents"].update(
                {4: PresWindowSize})

        # MagFilterMode:
        if (not isinstance(MagFilterMode, str)):
            raise ValueError("MagFilterMode must be a string.")
        # If MagFilterMode is not a valid value:
        elif (MagFilterMode not in
                VN100_IMU_Subsystem.filtering_configuration["MagFilterMode"]["valid_values_scope"].keys()):
            raise ValueError(
                "MagFilterMode value arg is not valid. See table 39 from VN-100 User Manual at pg. 87 about valid values.")
        else:
            ifc_args["length"] += 1
            ifc_args["contents"].update(
                {5: VN100_IMU_Subsystem.filtering_configuration["MagFilterMode"]["valid_values_scope"][MagFilterMode]})

        # AccelFilterMode:
        if (not isinstance(AccelFilterMode, str)):
            raise ValueError("AccelFilterMode must be a string.")
        # If AccelFilterMode is not a valid value:
        elif (AccelFilterMode not in
                VN100_IMU_Subsystem.filtering_configuration["AccelFilterMode"]["valid_values_scope"].keys()):
            raise ValueError(
                "AccelFilterMode value arg is not valid. See table 39 from VN-100 User Manual at pg. 87 about valid values.")
        else:
            ifc_args["length"] += 1
            ifc_args["contents"].update(
                {6: VN100_IMU_Subsystem.filtering_configuration["AccelFilterMode"]["valid_values_scope"][AccelFilterMode]})

        # GyroFilterMode:
        if (not isinstance(GyroFilterMode, str)):
            raise ValueError("GyroFilterMode must be a string.")
        # If GyroFilterMode is not a valid value:
        elif (GyroFilterMode not in
                VN100_IMU_Subsystem.filtering_configuration["GyroFilterMode"]["valid_values_scope"].keys()):
            raise ValueError(
                "GyroFilterMode value arg is not valid. See table 39 from VN-100 User Manual at pg. 87 about valid values.")
        else:
            ifc_args["length"] += 1
            ifc_args["contents"].update(
                {7: VN100_IMU_Subsystem.filtering_configuration["GyroFilterMode"]["valid_values_scope"][GyroFilterMode]})

        # TempFilterMode:
        if (not isinstance(TempFilterMode, str)):
            raise ValueError("TempFilterMode must be a string.")
        # If TempFilterMode is not a valid value:
        elif (TempFilterMode not in
                VN100_IMU_Subsystem.filtering_configuration["TempFilterMode"]["valid_values_scope"].keys()):
            raise ValueError(
                "TempFilterMode value arg is not valid. See table 39 from VN-100 User Manual at pg. 87 about valid values.")
        else:
            ifc_args["length"] += 1
            ifc_args["contents"].update(
                {8: VN100_IMU_Subsystem.filtering_configuration["TempFilterMode"]["valid_values_scope"][TempFilterMode]})

        # PresFilterMode:
        if (not isinstance(PresFilterMode, str)):
            raise ValueError("PresFilterMode must be a string.")
        # If PresFilterMode is not a valid value:
        elif (PresFilterMode not in
                VN100_IMU_Subsystem.filtering_configuration["PresFilterMode"]["valid_values_scope"].keys()):
            raise ValueError(
                "PresFilterMode value arg is not valid. See table 39 from VN-100 User Manual at pg. 87 about valid values.")
        else:
            ifc_args["length"] += 1
            ifc_args["contents"].update(
                {9: VN100_IMU_Subsystem.filtering_configuration["PresFilterMode"]["valid_values_scope"][PresFilterMode]})

        return VN100_IMU_Subsystem._write_register(85, ifc_args)

    @staticmethod
    def get_filtering_configuration():
        '''Gets the "Reference frame rotation" register content.
        See section 7.2.5 of VN-100 User Manual (pg. 87).'''
        return VN100_IMU_Subsystem._read_register(85)

    @staticmethod
    def set_delta_theta_delta_velocity_configuration(
            IntegrationFrame,
            GyroCompensation,
            AccelCompensation):
        '''Sets the "Delta theta and delta velocity configuration" register content.
        args: (
            IntegrationFrame: string with the reference frame used for coning and sculling. NED_FRAME uses Kalman filter's attitude estimate.
                For valid values consult on this class the delta_theta_delta_velocity_configuration["IntegrationFrame"]["valid_values_scope"].keys()): attribute.
            GyroCompensation: string with the selected compensation for angular rate. BIAS uses Kalman filter's attitude estimate.
                For valid values consult on this class the delta_theta_delta_velocity_configuration["GyroCompensation"]["valid_values_scope"].keys()): attribute.
            AccelCompensation: string with the selected compensation for acceleration measurements. BIAS uses Kalman filter's attitude estimate.
                For valid values consult on this class the delta_theta_delta_velocity_configuration["AccelCompensation"]["valid_values_scope"].keys()): attribute.
        )
        See section 7.2.6 of VN-100 User Manual (pg. 88).'''
        # Datagram dictionary
        dtdvc_args = {
            "length": 0,
            "contents": {}
        }
        # IntegrationFrame:
        if (not isinstance(IntegrationFrame, str)):
            raise ValueError("IntegrationFrame must be a string.")
        # If IntegrationFrame is not a valid value:
        elif (IntegrationFrame not in
                VN100_IMU_Subsystem.delta_theta_delta_velocity_configuration["IntegrationFrame"]["valid_values_scope"].keys()):
            raise ValueError(
                "IntegrationFrame value arg is not valid. See table 40 from VN-100 User Manual at pg. 88 about valid values.")
        else:
            dtdvc_args["length"] += 1
            dtdvc_args["contents"].update(
                {0: VN100_IMU_Subsystem.delta_theta_delta_velocity_configuration["IntegrationFrame"]["valid_values_scope"][IntegrationFrame]})

        # GyroCompensation:
        if (not isinstance(GyroCompensation, str)):
            raise ValueError("GyroCompensation must be a string.")
        # If GyroCompensation is not a valid value:
        elif (GyroCompensation not in
                VN100_IMU_Subsystem.delta_theta_delta_velocity_configuration["GyroCompensation"]["valid_values_scope"].keys()):
            raise ValueError(
                "GyroCompensation value arg is not valid. See table 41 from VN-100 User Manual at pg. 88 about valid values.")
        else:
            dtdvc_args["length"] += 1
            dtdvc_args["contents"].update(
                {1: VN100_IMU_Subsystem.delta_theta_delta_velocity_configuration["GyroCompensation"]["valid_values_scope"][GyroCompensation]})

        # AccelCompensation:
        if (not isinstance(AccelCompensation, str)):
            raise ValueError("AccelCompensation must be a string.")
        # If AccelCompensation is not a valid value:
        elif (AccelCompensation not in
                VN100_IMU_Subsystem.delta_theta_delta_velocity_configuration["AccelCompensation"]["valid_values_scope"].keys()):
            raise ValueError(
                "AccelCompensation value arg is not valid. See table 44 from VN-100 User Manual at pg. 89 about valid values.")
        else:
            dtdvc_args["length"] += 1
            dtdvc_args["contents"].update(
                {2: VN100_IMU_Subsystem.delta_theta_delta_velocity_configuration["AccelCompensation"]["valid_values_scope"][AccelCompensation]})

        # Add two reserved fields:
        dtdvc_args["length"] += 2
        dtdvc_args["contents"].update(
            {3: 0,
             4: 0}
        )

        return VN100_IMU_Subsystem._write_register(82, dtdvc_args)

    @staticmethod
    def get_delta_theta_delta_velocity_configuration():
        '''Gets the "Delta theta and delta velocity configuration" register content.
        See section 7.2.6 of VN-100 User Manual (pg. 88):'''
        return VN100_IMU_Subsystem._read_register(82)
