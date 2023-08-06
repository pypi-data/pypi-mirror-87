# ////// Program settings //////
# Main performance configuration:
main_performance_configuration = {
    "VN_INM_Interface_Server_class": {
        "autoconfig_buffers_flusher": {
            "dead_times": {
                "main_loop": {
                    "about": '''Value in seconds (s), This is the time that the flusher won't work .
                            The greater this value, the  smaller the workload, but more output buffer size must be needed.
                            Bear in mind that the worst case is when the INM sends binary data at maximum frequency (case VN-100 is 200 Hz),
                            each message with the full size (case VN-100 is 600 bytes), then each message is parsed and each object is naturally greater than each inm output message.
                            Recommended values should be between 0.01 s with 32 KiB min. of buffer size and 0.1 with 320 KiB min. of buffer size.
                            Default is 0.047 s.''',
                    "value": 0.5
                }
            }
        },
        "udp_rpc_listener": {
            "dead_times": {
                "retry_listen": {
                    "about": '''Value in seconds (s), This is the time to wait for next try to listen for UDP clients requests.
                            The greater this value, the  smaller the workload, but request will be slower,
                            The smaller this value, the greater the workload, thus it will come bad to system performance.
                            Recommended values should be between 0.1 s to 1 s.
                            Default is 0.17 s.''',
                    "value": 0.5
                }
            }
        },
        "inm_output_data_saver": {
            "dead_times": {
                "main_loop": {
                    "about": '''Value in seconds (s), This is the time to wait for save the next inm output message object from the
                            parser output buffer.
                            The greater this value, the smaller the workload, but it's worse if it's enoughly greater, because some information
                            will get lost. Nevertheless, the smaller this value, the greater the workload.
                            Bear in mind that the worst case is when the INM sends binary data at maximum frequency (case VN-100 is 200 Hz),
                            each message with the full size (case VN-100 is 600 bytes), then each message is parsed and each object is naturally greater than each inm output message.
                            Recommended values should be between 0.01 s with 32 KiB min. of buffer size and 0.1 with 320 KiB min. of buffer size.
                            Default is 0.047 s.''',
                    "value": 1
                },
                "set_inm_checker": {
                    "about": '''Value in seconds (s), This is the time to wait for retry to check if a correspondent answer of current writing rpc is
                            into the parser output buffer.
                            The greater this value, the smaller the workload, but answer detection speed will be slower.
                            Regardless of parser output messages rate, since the "autoconfig_buffers_flusher" task is running at the same time,
                            this value can be fairly high.
                            Recommended values should be between 0.1 s to 1 s.
                            Default is 0.5s.''',
                    "value": 0.5
                },
                "read_inm_checker": {
                    "about": '''Value in seconds (s), This is the time to wait for retry to check if a correspondent answer of current reading rpc is
                            into the parser output buffer.
                            The greater this value, the smaller the workload, but answer detection speed will be slower.
                            Regardless of parser output messages rate, since the "autoconfig_buffers_flusher" task is running at the same time,
                            this value can be fairly high.
                            Recommended values should be between 0.1 s to 1 s.
                            Default is 0.5s.''',
                    "value": 0.5
                },
                "next_requirement": {
                    "about": '''Value in seconds (s), This is the time to wait for check the next requirement from the settings descriptor.
                            The greater this value, the smaller the workload, but requirement dispatcher speed will be slower.
                            Regardless of parser output messages rate, since the "autoconfig_buffers_flusher" task is running at the same time,
                            The smaller this value, really is better.
                            Recommended values should be up to 0.5 s. Tip: this value should be near high than or equal to main_loop dead time value of the
                            inm_rpc_agent task.
                            Default is 0.2s.''',
                    "value": 0.2
                }
            },
            "properties": {
                "MINIMUM_OUTPUT_INM_DATA_OBJECTS_QUANTITY_TO_SAVE_THRESHOLD": {
                    "about": '''This value is the quantity of INM output data object messages needed to consider a group to save on memory
                            and/or make a callback to a saver server. The greater this value, the greater the RAM is needed, but the workload could be
                            setted for be lower. Be carefully choosing this value, because it depends on the message sending rate from the INM output.
                            Recommended values should be at least 5.
                            Default is 10.''',
                    "value": 10
                }
            }
        },
        "inm_rpc_agent": {
            "dead_times": {
                "retry_write_rpc": {
                    "about": '''Value in seconds (s). This is the time to wait to an INM response, according to the current
                            rpc.
                            The greater this value, the  smaller the workload, but answers will be slower;
                            The smaller this value, the greater the workload.
                            It's important bear in mind that smaller or greater values beyond the recommended values range,
                            more input buffer size of the INM controller serial port output and more output buffer size of the INM
                            controller parser output are required, in order to avoid data losses.
                            Recommended values should be between 0.15 s to 0.75 s.
                            Default is 0.2 s.''',
                    "value": 0.2
                },
                "main_loop": {
                    "about": '''Value in seconds (s). This is the time that the agent won't work.
                            The greater this value, the  smaller the workload, but the speed of dispatcher will be slower,
                            The smaller this value, the greater the workload, thus it will come bad to system performance.
                            Recommended values should be between 0.1 to 0.5 s. Tip: this value should be near higher than or
                            equal to "retry_listen" dead time value of the  "udp_rpc_listener" task.
                            Default is 0.18 s.''',
                    "value": 0.5
                }
            }
        }
    },
    "VN100_Controller_class": {
        "properties": {
            "VN100_Parser_class_object": {
                "properties": {
                    "BIN_MESSAGE_MAX_LENGTH": {
                        "about": '''Value in bytes (B). This is the maximum size of a any message from the INM.
                                The VectorNav's VN-100 INM sends messages up to 600 B.''',
                        "value": 600
                    },
                    "BUFFER_OVERFLOW_THRESHOLD_RATIO": {
                        "about": '''This value means the n times the "BIN_MESSAGE_MAX_LENGTH" for set
                                the input buffer overflow threshold. The greater this value, the greater the RAM usage and
                                the greater each parser sweep time, but the main_loop dead time of _parser method of the VN_100_Controller_class
                                can be greater. It's important to keep in mind that this value is strongly related with the latter mentioned of the
                                VN_100_Controller_class (this is inversely proportional); the BIN_MESSAGE_MAX_LENGTH of this class, the
                                MAX_READ_BUFFER_SIZE_RATIO and the MAX_READ_PACKAGE_LENGTH of the Async_Serial_class (all of three
                                are directly proportional and MAX_READ_PACKAGE_LENGTH * MAX_READ_BUFFER_SIZE_RATIO should be greater than
                                BUFFER_OVERFLOW_THRESHOLD_RATIO * BIN_MESSAGE_MAX_LENGTH); finally, the worst case of sending information
                                rate from the INM.
                                Recommended values should be like 270 when BIN_MESSAGE_MAX_LENGTH = 600, MAX_READ_PACKAGE_LENGTH = 16384,
                                MAX_READ_BUFFER_SIZE_RATIO = 10 and the main_loop dead time of _parser is set at 1 s, at the worst case of sending information
                                rate from the INM, it means that this value is 120 KB/s (600 B, 200 Hz).
                                Default value is 270.''',
                        "value": 270
                    }
                }
            },
            "MAX_OUTPUT_BUFFER_LENGTH": {
                "about": '''Value in bytes (B). This is the maximum output buffer size. The greater this value, the greater RAM used, but it will allow
                        to use bigger values for dead times when it sends callbacks to the end user, thus the workload could be smaller.
                        Bear in mind that this value is implicitly correlated with the INM output message rate, and the each message variables quantity; also the
                        each INM parsed object size. Let's do the following assumption: the worst INM output message rate is 200 Hz for the VectorNav's VN-100, if each
                        message with up to 600 B has up to 150 variables (each variable has 4 bytes in this case assumption), each variable has up to 100 bytes of information, and the
                        main_loop dead time of inm_output_data_saver of the VN_INM_Interface_Server_class is default at 0.047 s then
                        the output buffer fill rate is 200 * 150 * 100 * 0.047 = 141.000 B (138 KiB aprox).
                        Recommended values should keep the following ratio: 1.048.576 B (1 MiB) at 0.34 s.
                        Default is 1.048.576 B (1 MiB).
                        ''',
                "value": 1048576
            },
            "Async_Serial_class_object": {
                "Serial_Port_Object": {
                    "blocking_times": {
                        "read_timeout": {
                            "about": '''Value in seconds (s). This is the time that the read(package_size) function of Serial Port Object wait until try to fill  a package at "package_size".
                                    The greater this value, the greater the time that the whole asyncio-ed program will be blocked, thus it's not recommended.
                                    The smaller this value, the smaller the output packages, but it doesn't matter, thus it's better; nevertheless if this value is too small, data losses are possible to occur.
                                    Bear in mind that the worst case is when the INM sends smallest data packages at minimum frequency.
                                    Recommended values should be between 0.001 s (1 byte per sweep at 9.6 kb/s aprox.) to 0.05 s.
                                    Default is 0.047 s.''',
                            "value": 0.2
                        }
                    }
                },
                "properties": {
                    "MAX_READ_BUFFER_SIZE_RATIO": {
                        "about": '''Value is a 8 bit unsigned integer. This is the buffer size of input of this serial port, in terms of n times the MAX_READ_PACKAGE_LENGTH.
                                The greater this value, the  greater the RAM occupancy is needed, but it can improve performance because lower frequency sweep for check data will be needed.
                                Tip: this ratio is correlated with the dead time value of the user program main loop and the "read_timeout" of this class, when an instance of this class is implemented.
                                Thus, n times the MAX_READ_PACKAGE_LENGTH, gives the chance of raise n times such dead time value respect to the current "read_timeout", improving the whole
                                program performance.
                                default is 10 (160 KiB)''',
                        "value": 10
                    },
                    "MAX_READ_PACKAGE_LENGTH": {
                        "about": '''Value in bytes (B). This is the maximum length of a package from input of this serial port.
                                The greater this value, the  greater the ability to improve performance because lower frequency sweep will be needed.
                                Bear in mind that the worst case is when the INM sends binary data at maximum frequency (case VN-100 is 200 Hz),
                                each message with the full size (case VN-100 is 600 bytes), then each message is parsed and each object is naturally greater than each inm output message.
                                Recommended values should be, trying to keep a ratio of 16384 B (16 KiB) min. at 0.1 s of blocking read time. According to this, the
                                default is 16384 B (16 KiB, for a read_timeout default value = 0.047 s.)''',
                        "value": 16384
                    }
                },
                "_reader": {
                    "dead_times": {
                        "main_loop": {
                            "about": '''Value in seconds (s). This is the time that _reader won't work, while the serial port is opened.
                                    The greater this value, the  smaller the workload. Nevertheless, this value is fairly correlated with the serial port object "read_timeout".
                                    If the "read_timeout" is small, this main_loop dead time value must be small too. On the other hand, if the "read_timeout" is big, it's not neccesary that this
                                    main_loop dead time value must be big too. However, it's recommended that this value should be smaller than the "read_timeout".
                                    Recommended values should be between 0.001 s to 0.05 s.
                                    Default is 0.039 s.''',
                            "value": 1
                        },
                        "retry_reconnect_serial_port": {
                            "about": '''Value in seconds (s). This is the time that _reader won't work, while it retry to reconnect to serial port when the latter is closed or disconnected..
                                    Recommended values should be minimum 0.1 s.
                                    Default is 0.2 s.''',
                            "value": 1
                        }
                    }
                }
            }
        },
        "_parse": {
            "dead_times": {
                "main_loop": {
                    "about": '''Value in seconds (s). This is the time that the _parse won't work.
                            The greater this value, the  smaller the workload, but more input buffer size of parser must be needed.
                            Bear in mind that the worst case is when the INM sends binary data at maximum frequency (case VN-100 is 200 Hz),
                            each message with the full size (case VN-100 is 600 bytes), then each message is parsed and each object is naturally greater than each inm output message.
                            Recommended values should be between 0.01 s with 32 KiB min. of buffer size and 0.1 with 320 KiB min. of buffer size.
                            Default is 0.047 s.''',
                    "value": 1
                }
            }
        }
    }
}
# Health watchdogs configuration
health_watchdog_configuration = {
    "VN_INM_Interface_Server": {
        "__init__": {
            "warning_timer_value": 1,
            "error_timer_value": 2},
        "udp_rpc_listener": {
            "warning_timer_value": 2,
            "error_timer_value": 4},
        "inm_rpc_agent": {
            "warning_timer_value": 2,
            "error_timer_value": 4},
        "autoconfig_buffers_flusher": {
            "warning_timer_value": 2,
            "error_timer_value": 4},
        "set_user_inm_configuration": {
            "warning_timer_value": 45,
            "error_timer_value": 60},
        "inm_output_data_saver": {
            "warning_timer_value": 2,
            "error_timer_value": 4}
    },
    "VN100_Controller_class": {
        "__init__": {
            "warning_timer_value": 1,
            "error_timer_value": 2},
        "parse": {
            "warning_timer_value": 2,
            "error_timer_value": 4}
    },
    "Async_Serial_class": {
        "__init__": {
            "warning_timer_value": 1,
            "error_timer_value": 2},
        "reader": {
            "warning_timer_value": 2,
            "error_timer_value": 4},
    }
}

# VN100 Serial port settings:
serial_port_settings = {
    "port": "/dev/ttyUSB0",
    "bit_rate": 115200
}
# Human client UDP port settings:
udp_connection_settings = {
    "IP_address": "0.0.0.0",
    "port": 27800
}