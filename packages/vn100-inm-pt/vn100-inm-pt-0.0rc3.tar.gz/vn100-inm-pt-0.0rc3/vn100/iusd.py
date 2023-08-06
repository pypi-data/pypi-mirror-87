inm_user_settings_descriptor = {
    "about": {
        "title": "V2.5 configuration",
        "description": "This is the configuration for the ADM v2.5. 0. No data strings outputs; 1. All neccesary binary data outputs; 2. Window size of accelerometer filter is 100 of 800 Hz, it means that the FIR low-pass filter cutoff frequency is 8 Hz."
    },
    "content": {
        "0": {
            "function": "SYSTEM_SET_ASYNC_DATA_OUTPUT_TYPE",
            "args": {
                "ADOR": "N/A",
                "SerialPort": "CURRENT"
            }
        },
        "1": {
            "function": "SYSTEM_SET_BINARY_OUTPUT_REGISTERS",
            "args": {
                "Binary_output_register_number": 1,
                "AsyncMode": "SERIAL_PORT_1",
                "RateDivisor": 80,
                "OutputGroup_fields": {
                    "GROUP_1": [
                        "MagPres",
                        "YawPitchRoll",
                        "Accel",
                        "AngularRate"
                    ]
                }
            }
        },
        "2": {
            "function": "IMU_SET_FILTERING_CONFIGURATION",
            "args": {
                "MagWindowSize": 0,
                "AccelWindowSize": 100,
                "GyroWindowSize": 4,
                "TempWindowSize": 4,
                "PresWindowSize": 0,
                "MagFilterMode": "NULL",
                "AccelFilterMode": "BOTH",
                "GyroFilterMode": "BOTH",
                "TempFilterMode": "BOTH",
                "PresFilterMode": "NULL"
            }
        }
    }
}
