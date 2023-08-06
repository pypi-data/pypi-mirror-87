# VectorNav VN-100's World Magnetic And Gravity Module.
# See section 11 of VN-100 User Manual (pg. 123).
# Document number: UM001 v2.05.
# Firmware version: 2.0.0.0.
# This is the Python 3 version.
# Author of this script: Andrés Eduardo Torres Hernández.


from .register_manager import VN100_Register_Manager
from .resources import C8bit_cksm
from .logger import init_logger


class VN100_World_Magnetic_Gravity_Module(VN100_Register_Manager):
    '''VectorNav VN-100's World Magnetic And Gravity Module.
    See section 11 of VN-100 User Manual (pg. 123).
    Document number: UM001 v2.05.
    Firmware version: 2.0.0.0.'''
    # Register variables:
    magnetic_gravity_reference_vectors = {
        "MagRefX": {
            "position": 0,
            "data_type": "float",
            "unit": "Gauss",
            "valid_values_scope": {
            }
        },
        "MagRefY": {
            "position": 1,
            "data_type": "float",
            "unit": "Gauss",
            "valid_values_scope": {
            }
        },
        "MagRefZ": {
            "position": 2,
            "data_type": "float",
            "unit": "Gauss",
            "valid_values_scope": {
            }
        },
        "AccRefX": {
            "position": 3,
            "data_type": "float",
            "unit": "m/s^2",
            "valid_values_scope": {
            }
        },
        "AccRefY": {
            "position": 4,
            "data_type": "float",
            "unit": "m/s^2",
            "valid_values_scope": {
            }
        },
        "AccRefZ": {
            "position": 5,
            "data_type": "float",
            "unit": "m/s^2",
            "valid_values_scope": {
            }
        }
    }

    reference_vector_configuration = {
        "UseMagModel": {
            "position": 0,
            "data_type": "uint8",
            "unit": "-",
            "valid_values_scope": {
                "DISABLE": 0,
                "ENABLE": 1
            }
        },
        "UseGravityModel": {
            "position": 1,
            "data_type": "uint8",
            "unit": "-",
            "valid_values_scope": {
                "DISABLE": 0,
                "ENABLE": 1
            }
        },
        "Resv1": {
            "position": 2,
            "data_type": "uint8",
            "unit": "-",
            "valid_values_scope": {
            }
        },
        "Resv2": {
            "position": 3,
            "data_type": "uint8",
            "unit": "-",
            "valid_values_scope": {
            }
        },
        "RecalcThreshold": {
            "position": 4,
            "data_type": "uint32",
            "unit": "-",
            "valid_values_scope": {
            }
        },
        "Year": {
            "position": 5,
            "data_type": "float",
            "unit": "year",
            "valid_values_scope": {
            }
        },
        "Latitude": {
            "position": 6,
            "data_type": "double",
            "unit": "deg",
            "valid_values_scope": {
            }
        },
        "Longitude": {
            "position": 7,
            "data_type": "double",
            "unit": "deg",
            "valid_values_scope": {
            }
        },
        "Altitude": {
            "position": 8,
            "data_type": "double",
            "unit": "m",
            "valid_values_scope": {
            }
        }
    }

    _logger = init_logger(__name__)

    # Methods:
    @staticmethod
    def set_magnetic_gravity_reference_vectors(
            MagRefX,
            MagRefY,
            MagRefZ,
            AccRefX,
            AccRefY,
            AccRefZ):
        '''Sets the "Magnetic and gravity reference vectors" register content.
        args: (
            MagRefX: float with the X-axis magnetic reference.
            MagRefY: float with the Y-axis magnetic reference.
            MagRefZ: float with the Z-axis magnetic reference.
            AccRefX: float with the X-axis gravity reference.
            AccRefY: float with the Y-axis gravity reference.
            AccRefZ: float with the Z-axis gravity reference.
        )
        See section 11.1.1 of VN-100 User Manual (pg. 123).'''
        # Datagram dictionary
        mgrv_args = {
            "length": 0,
            "contents": {}
        }
        # MagRefX:
        if (not isinstance(MagRefX, float)):
            raise ValueError("MagRefX must be an float.")
        elif (mgrv_args["length"] == VN100_World_Magnetic_Gravity_Module.magnetic_gravity_reference_vectors["MagRefX"]["position"]):
            mgrv_args["length"] += 1
            mgrv_args["contents"].update(
                {VN100_World_Magnetic_Gravity_Module.magnetic_gravity_reference_vectors["MagRefX"][
                    "position"]: MagRefX})
        else:
            raise IndexError("Index position message isn't coherent.")

        # MagRefY:
        if (not isinstance(MagRefY, float)):
            raise ValueError("MagRefY must be an float.")
        elif (mgrv_args["length"] == VN100_World_Magnetic_Gravity_Module.magnetic_gravity_reference_vectors["MagRefY"]["position"]):
            mgrv_args["length"] += 1
            mgrv_args["contents"].update(
                {VN100_World_Magnetic_Gravity_Module.magnetic_gravity_reference_vectors["MagRefY"][
                    "position"]: MagRefY})
        else:
            raise IndexError("Index position message isn't coherent.")

        # MagRefZ:
        if (not isinstance(MagRefZ, float)):
            raise ValueError("MagRefZ must be an float.")
        elif (mgrv_args["length"] == VN100_World_Magnetic_Gravity_Module.magnetic_gravity_reference_vectors["MagRefZ"]["position"]):
            mgrv_args["length"] += 1
            mgrv_args["contents"].update(
                {VN100_World_Magnetic_Gravity_Module.magnetic_gravity_reference_vectors["MagRefZ"][
                    "position"]: MagRefZ})
        else:
            raise IndexError("Index position message isn't coherent.")

        # AccRefX:
        if (not isinstance(AccRefX, float)):
            raise ValueError("AccRefX must be an float.")
        elif (mgrv_args["length"] == VN100_World_Magnetic_Gravity_Module.magnetic_gravity_reference_vectors["AccRefX"]["position"]):
            mgrv_args["length"] += 1
            mgrv_args["contents"].update(
                {VN100_World_Magnetic_Gravity_Module.magnetic_gravity_reference_vectors["AccRefX"][
                    "position"]: AccRefX})
        else:
            raise IndexError("Index position message isn't coherent.")

        # AccRefY:
        if (not isinstance(AccRefY, float)):
            raise ValueError("AccRefY must be an float.")
        elif (mgrv_args["length"] == VN100_World_Magnetic_Gravity_Module.magnetic_gravity_reference_vectors["AccRefY"]["position"]):
            mgrv_args["length"] += 1
            mgrv_args["contents"].update(
                {VN100_World_Magnetic_Gravity_Module.magnetic_gravity_reference_vectors["AccRefY"][
                    "position"]: AccRefY})
        else:
            raise IndexError("Index position message isn't coherent.")

        # AccRefZ:
        if (not isinstance(AccRefZ, float)):
            raise ValueError("AccRefZ must be an float.")
        elif (mgrv_args["length"] == VN100_World_Magnetic_Gravity_Module.magnetic_gravity_reference_vectors["AccRefZ"]["position"]):
            mgrv_args["length"] += 1
            mgrv_args["contents"].update(
                {VN100_World_Magnetic_Gravity_Module.magnetic_gravity_reference_vectors["AccRefZ"][
                    "position"]: AccRefZ})
        else:
            raise IndexError("Index position message isn't coherent.")

        return VN100_World_Magnetic_Gravity_Module._write_register(21, mgrv_args)

    @staticmethod
    def get_magnetic_gravity_reference_vectors():
        '''Gets the "Magnetic and gravity reference vectors" register content.
        See section 11.1.1 of VN-100 User Manual (pg. 123).'''
        return VN100_World_Magnetic_Gravity_Module._read_register(21)

    @staticmethod
    def set_reference_vector_configuration(
            UseMagModel,
            UseGravityModel,
            RecalcThreshold,
            Year,
            Latitude,
            Longitude,
            Altitude):
        '''Sets the "Reference vector configuration" register content.
        args: (
            UseMagModel: string with defines if the module use or not the world magnetic module
                For valid values consult on this class the reference_vector_configuration["UseMagModel"]["valid_values_scope"].keys()): attribute.
            UseGravityModel: string with defines if the module use or not the world gravity module
                For valid values consult on this class the reference_vector_configuration["UseGravityModel"]["valid_values_scope"].keys()): attribute.
            RecalcThreshold: 4-byte integer with the maximum distance traveled before magnetic and gravity models are recalculated for the new position.
            Year: float with the reference date expressed as a decimal year.
            Latitude: double precision float with the reference latitude position, in degrees.
            Longitude: double precision float with the reference longitude position, in degrees.
            Altitude: double precision float with the reference altitude above the reference ellipsoid, in meters.
        )
        See section 11.1.2 of VN-100 User Manual (pg. 124).'''
        # Datagram dictionary
        rvc_args = {
            "length": 0,
            "contents": {}
        }
        # UseMagModel:
        if (not isinstance(UseMagModel, str)):
            raise ValueError("UseMagModel must be a string.")
        # If UseMagModel is not a valid value:
        elif (UseMagModel not in
                VN100_World_Magnetic_Gravity_Module.reference_vector_configuration["UseMagModel"]["valid_values_scope"].keys()):
            raise ValueError(
                "UseMagModel value arg is not valid. See VN-100 User Manual at pg. 124 about valid values.")
        elif (rvc_args["length"] == VN100_World_Magnetic_Gravity_Module.reference_vector_configuration["UseMagModel"]["position"]):
            rvc_args["length"] += 1
            rvc_args["contents"].update(
                {VN100_World_Magnetic_Gravity_Module.reference_vector_configuration["UseMagModel"][
                    "position"]: VN100_World_Magnetic_Gravity_Module.reference_vector_configuration["UseMagModel"]["valid_values_scope"][UseMagModel]})
        else:
            raise IndexError("Index position message isn't coherent.")

        # UseGravityModel:
        if (not isinstance(UseGravityModel, str)):
            raise ValueError("UseGravityModel must be a string.")
        # If UseGravityModel is not a valid value:
        elif (UseGravityModel not in
                VN100_World_Magnetic_Gravity_Module.reference_vector_configuration["UseGravityModel"]["valid_values_scope"].keys()):
            raise ValueError(
                "UseGravityModel value arg is not valid. See VN-100 User Manual at pg. 124 about valid values.")
        elif (rvc_args["length"] == VN100_World_Magnetic_Gravity_Module.reference_vector_configuration["UseGravityModel"]["position"]):
            rvc_args["length"] += 1
            rvc_args["contents"].update(
                {VN100_World_Magnetic_Gravity_Module.reference_vector_configuration["UseGravityModel"][
                    "position"]: VN100_World_Magnetic_Gravity_Module.reference_vector_configuration["UseGravityModel"]["valid_values_scope"][UseGravityModel]})
        else:
            raise IndexError("Index position message isn't coherent.")

        # Add two reserved fields:
        rvc_args["length"] += 2
        rvc_args["contents"].update({
            VN100_World_Magnetic_Gravity_Module.reference_vector_configuration["Resv1"][
                    "position"]: 0,
            VN100_World_Magnetic_Gravity_Module.reference_vector_configuration["Resv2"][
                    "position"]: 0,
        })

        # RecalcThreshold:
        if (not isinstance(RecalcThreshold, int)):
            raise ValueError("RecalcThreshold must be an integer.")
        elif (rvc_args["length"] == VN100_World_Magnetic_Gravity_Module.reference_vector_configuration["RecalcThreshold"]["position"]):
            rvc_args["length"] += 1
            rvc_args["contents"].update(
                {VN100_World_Magnetic_Gravity_Module.reference_vector_configuration["RecalcThreshold"][
                    "position"]: RecalcThreshold})
        else:
            raise IndexError("Index position message isn't coherent.")

        # Year:
        if (not isinstance(Year, float)):
            raise ValueError("Year must be an float.")
        elif (rvc_args["length"] == VN100_World_Magnetic_Gravity_Module.reference_vector_configuration["Year"]["position"]):
            rvc_args["length"] += 1
            rvc_args["contents"].update(
                {VN100_World_Magnetic_Gravity_Module.reference_vector_configuration["Year"][
                    "position"]: Year})
        else:
            raise IndexError("Index position message isn't coherent.")

        # Latitude:
        if (not isinstance(Latitude, float)):
            raise ValueError("Latitude must be an float (double).")
        elif (rvc_args["length"] == VN100_World_Magnetic_Gravity_Module.reference_vector_configuration["Latitude"]["position"]):
            rvc_args["length"] += 1
            rvc_args["contents"].update(
                {VN100_World_Magnetic_Gravity_Module.reference_vector_configuration["Latitude"][
                    "position"]: Latitude})
        else:
            raise IndexError("Index position message isn't coherent.")

        # Longitude:
        if (not isinstance(Longitude, float)):
            raise ValueError("Longitude must be an float (double).")
        elif (rvc_args["length"] == VN100_World_Magnetic_Gravity_Module.reference_vector_configuration["Longitude"]["position"]):
            rvc_args["length"] += 1
            rvc_args["contents"].update(
                {VN100_World_Magnetic_Gravity_Module.reference_vector_configuration["Longitude"][
                    "position"]: Longitude})
        else:
            raise IndexError("Index position message isn't coherent.")

        # Altitude:
        if (not isinstance(Altitude, float)):
            raise ValueError("Altitude must be an float (double).")
        elif (rvc_args["length"] == VN100_World_Magnetic_Gravity_Module.reference_vector_configuration["Altitude"]["position"]):
            rvc_args["length"] += 1
            rvc_args["contents"].update(
                {VN100_World_Magnetic_Gravity_Module.reference_vector_configuration["Altitude"][
                    "position"]: Altitude})
        else:
            raise IndexError("Index position message isn't coherent.")

        return VN100_World_Magnetic_Gravity_Module._write_register(83, rvc_args)

    @staticmethod
    def get_reference_vector_configuration():
        '''Sets the "Reference vector configuration" register content.
        See section 11.1.2 of VN-100 User Manual (pg. 124).'''
        return VN100_World_Magnetic_Gravity_Module._read_register(83)