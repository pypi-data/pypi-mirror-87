# The interface for VectorNav INM.
# Author: Andrés Eduardo Torres Hernández.

from .vn100_modules import (
    VN100_System_module,
    VN100_IMU_Subsystem,
    VN100_Attitude_Subsystem,
    VN100_HSIE_Subsystem, VN100_Velocity_Aiding,
    VN100_World_Magnetic_Gravity_Module,
    Health_Watchdog
)

import asyncio
from .vn100_modules.logger import init_logger
import socket
import datetime
from .cksm import CksmFletcher16
from threading import Thread
import time
import json


class VN_INM_Interface_Server:
    def __init__(
            self,
            udp_server,
            vn100_controller,
            user_settings_descriptor,
            health_watchdog_configuration=None,
            health_diagnostics_callback=None,
            inm_output_file=None,
            inm_output_callback=None,
            performance_settings=None):
        self._logger = init_logger(__name__)
        # Health watchdog:
        self.health_watchdog = Health_Watchdog(
            "VN_INM_Interface_Server",
            diagnostics_callback=health_diagnostics_callback,
            timers_configuration=health_watchdog_configuration
        )
        # Track the __init__ health:
        self.health_watchdog.begin_track("__init__")
        # Create the rpc server and vn100 controller:
        self._udp_server = udp_server
        self._vn100_controller = vn100_controller
        # Begin functions dictionary
        self._functions_dict = {
            "SYSTEM_WRITE_SETTINGS": {"fx": VN100_System_module.write_settings,
                                      "response_criteria": {
                                          "command": "WRITE_SETTINGS"
                                      }
                                      },
            "SYSTEM_GET_MODEL_NUMBER": {"fx": VN100_System_module.get_model_number,
                                        "response_criteria": {
                                            "command": "READ_REGISTER",
                                            "register_name": "MODEL_NUMBER"
                                        }
                                        },
            "SYSTEM_GET_SERIAL_NUMBER": {"fx": VN100_System_module.get_serial_number,
                                         "response_criteria": {
                                             "command": "READ_REGISTER",
                                             "register_name": "SERIAL_NUMBER"
                                         }
                                         },
            "SYSTEM_GET_SERIAL_BAUD_RATE": {"fx": VN100_System_module.get_serial_baud_rate,
                                            "response_criteria": {
                                                "command": "READ_REGISTER",
                                                "register_name": "SERIAL_BAUD_RATE"
                                            }
                                            },
            "SYSTEM_SET_ASYNC_DATA_OUTPUT_TYPE": {"fx": VN100_System_module.set_async_data_output_type,
                                                  "response_criteria": {
                                                      "command": "WRITE_REGISTER",
                                                      "register_name": "ASYNC_DATA_OUTPUT_TYPE"
                                                  }
                                                  },
            "SYSTEM_GET_ASYNC_DATA_OUTPUT_TYPE": {"fx": VN100_System_module.get_async_data_output_type,
                                                  "response_criteria": {
                                                      "command": "READ_REGISTER",
                                                      "register_name": "ASYNC_DATA_OUTPUT_TYPE"
                                                  }
                                                  },
            "SYSTEM_GET_ASYNC_DATA_OUTPUT_FREQUENCY": {"fx": VN100_System_module.get_async_data_output_frequency,
                                                       "response_criteria": {
                                                           "command": "READ_REGISTER",
                                                           "register_name": "ASYNC_DATA_OUTPUT_FREQUENCY"
                                                       }
                                                       },
            "SYSTEM_GET_SYNCHRONIZATION_CONTROL": {"fx": VN100_System_module.get_synchronization_control,
                                                   "response_criteria": {
                                                       "command": "READ_REGISTER",
                                                       "register_name": "SYNCHRONIZATION_CONTROL"
                                                   }
                                                   },
            "SYSTEM_GET_COMMUNICATION_PROTOCOL_CONTROL": {"fx": VN100_System_module.get_communication_protocol_control,
                                                          "response_criteria": {
                                                              "command": "READ_REGISTER",
                                                              "register_name": "COMMUNICATION_PROTOCOL_CONTROL"
                                                          }
                                                          },
            "SYSTEM_SET_BINARY_OUTPUT_REGISTERS": {"fx": VN100_System_module.set_binary_output_registers,
                                                   "response_criteria": {
                                                       "command": "WRITE_REGISTER",
                                                       "register_name": "BINARY_OUTPUT_REGISTER_n"
                                                   }
                                                   },
            "SYSTEM_GET_BINARY_OUTPUT_REGISTERS": {"fx": VN100_System_module.get_binary_output_registers,
                                                   "response_criteria": {
                                                       "command": "READ_REGISTER",
                                                       "register_name": "BINARY_OUTPUT_REGISTER_n"
                                                   }
                                                   },
            "SYSTEM_GET_SYNCHRONIZATION_STATUS_COUNTERS": {"fx": VN100_System_module.get_synchronization_status_counters,
                                                           "response_criteria": {
                                                               "command": "READ_REGISTER",
                                                               "register_name": "SYNCHRONIZATION_STATUS"
                                                           }
                                                           },
            "IMU_GET_MEASUREMENTS": {"fx": VN100_IMU_Subsystem.get_measurements,
                                     "response_criteria": {
                                         "command": "READ_REGISTER",
                                         "register_name": "IMU_MEASUREMENTS"
                                     }
                                     },
            "IMU_GET_DELTA_THETA_DELTA_VELOCITY": {"fx": VN100_IMU_Subsystem.get_delta_theta_delta_velocity,
                                                   "response_criteria": {
                                                       "command": "READ_REGISTER",
                                                       "register_name": "DELTA_THETA_DELTA_VELOCITY"
                                                   }
                                                   },
            "IMU_SET_FILTERING_CONFIGURATION": {"fx": VN100_IMU_Subsystem.set_filtering_configuration,
                                                "response_criteria": {
                                                    "command": "WRITE_REGISTER",
                                                    "register_name": "IMU_FILTERING_CONFIGURATION"
                                                }
                                                },
            "IMU_GET_FILTERING_CONFIGURATION": {"fx": VN100_IMU_Subsystem.get_filtering_configuration,
                                                "response_criteria": {
                                                    "command": "READ_REGISTER",
                                                    "register_name": "IMU_FILTERING_CONFIGURATION"
                                                }
                                                },
            "IMU_SET_DELTA_THETA_DELTA_VELOCITY_CONFIGURATION": {"fx": VN100_IMU_Subsystem.set_delta_theta_delta_velocity_configuration,
                                                                 "response_criteria": {
                                                                     "command": "WRITE_REGISTER",
                                                                     "register_name": "DELTA_THETA_DELTA_VELOCITY_CONFIGURATION"
                                                                 }
                                                                 },
            "IMU_GET_DELTA_THETA_DELTA_VELOCITY_CONFIGURATION": {"fx": VN100_IMU_Subsystem.get_delta_theta_delta_velocity_configuration,
                                                                 "response_criteria": {
                                                                     "command": "READ_REGISTER",
                                                                     "register_name": "DELTA_THETA_DELTA_VELOCITY_CONFIGURATION"
                                                                 }
                                                                 },
            "ATTITUDE_GET_VPE_BASIC_CONTROL": {"fx": VN100_Attitude_Subsystem.get_vpe_basic_control,
                                               "response_criteria": {
                                                   "command": "READ_REGISTER",
                                                   "register_name": "VPE_BASIC_CONTROL"
                                               }
                                               },
            "ATTITUDE_SET_VPE_MAGNETOMETER_BASIC_TUNING": {"fx": VN100_Attitude_Subsystem.set_vpe_magnetometer_basic_tuning,
                                                           "response_criteria": {
                                                               "command": "WRITE_REGISTER",
                                                               "register_name": "VPE_MAGNETOMETER_BASIC_TUNING"
                                                           }
                                                           },
            "ATTITUDE_GET_VPE_MAGNETOMETER_BASIC_TUNING": {"fx": VN100_Attitude_Subsystem.get_vpe_magnetometer_basic_tuning,
                                                           "response_criteria": {
                                                               "command": "READ_REGISTER",
                                                               "register_name": "VPE_MAGNETOMETER_BASIC_TUNING"
                                                           }
                                                           },
            "ATTITUDE_SET_VPE_ACCELEROMETER_BASIC_TUNING": {"fx": VN100_Attitude_Subsystem.set_vpe_accelerometer_basic_tuning,
                                                            "response_criteria": {
                                                                "command": "WRITE_REGISTER",
                                                                "register_name": "VPE_ACCELEROMETER_BASIC_TUNING"
                                                            }
                                                            },
            "ATTITUDE_GET_VPE_ACCELEROMETER_BASIC_TUNING": {"fx": VN100_Attitude_Subsystem.get_vpe_accelerometer_basic_tuning,
                                                            "response_criteria": {
                                                                "command": "READ_REGISTER",
                                                                "register_name": "VPE_ACCELEROMETER_BASIC_TUNING"
                                                            }
                                                            },
            "HSIE_SET_MAGNETOMETER_CALIBRATION_CONTROL": {"fx": VN100_HSIE_Subsystem.set_magnetometer_calibration_control,
                                                          "response_criteria": {
                                                              "command": "WRITE_REGISTER",
                                                              "register_name": "MAGNETOMETER_CALIBRATION_CONTROL"
                                                          }
                                                          },
            "HSIE_GET_MAGNETOMETER_CALIBRATION_CONTROL": {"fx": VN100_HSIE_Subsystem.get_magnetometer_calibration_control,
                                                          "response_criteria": {
                                                              "command": "READ_REGISTER",
                                                              "register_name": "MAGNETOMETER_CALIBRATION_CONTROL"
                                                          }
                                                          },
            "HSIE_GET_CALCULATED_MAGNETOMETER_CALIBRATION": {"fx": VN100_HSIE_Subsystem.get_calculated_magnetometer_calibration,
                                                             "response_criteria": {
                                                                 "command": "READ_REGISTER",
                                                                 "register_name": "CALCULATED_MAGNETOMETER_CALIBRATION"
                                                             }
                                                             },
            "VELOCITY_AIDING_SET_VELOCITY_COMPENSATION_CONTROL": {"fx": VN100_Velocity_Aiding.set_velocity_compensation_control,
                                                                  "response_criteria": {
                                                                      "command": "WRITE_REGISTER",
                                                                      "register_name": "VELOCITY_COMPENSATION_CONTROL"
                                                                  }
                                                                  },
            "VELOCITY_AIDING_GET_VELOCITY_COMPENSATION_CONTROL": {"fx": VN100_Velocity_Aiding.get_velocity_compensation_control,
                                                                  "response_criteria": {
                                                                      "command": "READ_REGISTER",
                                                                      "register_name": "VELOCITY_COMPENSATION_CONTROL"
                                                                  }
                                                                  },
            "VELOCITY_AIDING_SET_VELOCITY_COMPENSATION_MEASUREMENT": {"fx": VN100_Velocity_Aiding.set_velocity_compensation_measurement,
                                                                      "response_criteria": {
                                                                          "command": "WRITE_REGISTER",
                                                                          "register_name": "VELOCITY_COMPENSATION_MEASUREMENT"
                                                                      }
                                                                      },
            "VELOCITY_AIDING_GET_VELOCITY_COMPENSATION_MEASUREMENT": {"fx": VN100_Velocity_Aiding.get_velocity_compensation_measurement,
                                                                      "response_criteria": {
                                                                          "command": "READ_REGISTER",
                                                                          "register_name": "VELOCITY_COMPENSATION_MEASUREMENT"
                                                                      }
                                                                      },
            "WORLD_MAGNETIC_GRAVITY_SET_MAGNETIC_GRAVITY_REFERENCE_VECTORS": {
                "fx": VN100_World_Magnetic_Gravity_Module.set_magnetic_gravity_reference_vectors,
                "response_criteria": {
                    "command": "WRITE_REGISTER",
                    "register_name": "MAGNETIC_GRAVITY_REFERENCE_VECTORS"
                }
            },
            "WORLD_MAGNETIC_GRAVITY_GET_MAGNETIC_GRAVITY_REFERENCE_VECTORS": {
                "fx": VN100_World_Magnetic_Gravity_Module.get_magnetic_gravity_reference_vectors,
                "response_criteria": {
                    "command": "READ_REGISTER",
                    "register_name": "MAGNETIC_GRAVITY_REFERENCE_VECTORS"
                }
            },
            "WORLD_MAGNETIC_GRAVITY_SET_REFERENCE_VECTOR_CONFIGURATION": {
                "fx": VN100_World_Magnetic_Gravity_Module.set_reference_vector_configuration,
                "response_criteria": {
                    "command": "WRITE_REGISTER",
                    "register_name": "REFERENCE_VECTOR_CONFIGURATION"
                }
            },
            "WORLD_MAGNETIC_GRAVITY_GET_REFERENCE_VECTOR_CONFIGURATION": {
                "fx": VN100_World_Magnetic_Gravity_Module.get_reference_vector_configuration,
                "response_criteria": {
                    "command": "READ_REGISTER",
                    "register_name": "REFERENCE_VECTOR_CONFIGURATION"
                }
            }
        }
        # server's variables
        self._udp_rpc_buffer_size = 1024
        self._read_counter = 0
        self._pack_counter = 0
        # Output ways:
        if (inm_output_file is None and
                inm_output_callback is None):
            error_msg = "There is not exist an output data way. Since the fact that run this service doesn't make sense, it's going to stop now."
            self._logger.error(error_msg)
            raise Exception(error_msg)
        # Declare and init the self._inm_output_file variable:
        self._inm_output_file = None
        if (inm_output_file != None):
            self._inm_output_file = open(inm_output_file, "a+")
        self._inm_output_callback = inm_output_callback
        # HMI client questions queue
        self._hmi_questions_queue = []
        # INM user settings descriptor file
        self._user_settings_descriptor = user_settings_descriptor
        # INM user settings rpc responses queue
        self._user_settings_rpc_responses_queue = []
        # Autoconfiguration status. flag. It's used at beginning of this program.
        self._is_autoconfiguring = True
        # Futures loop sleep timers
        if (performance_settings != None):
            self._FUTURES_LOOP_SLEEP_TIMERS = {
                "REMOTE_CONTROL_SERVER_RETRY_LISTEN_TIME": performance_settings[
                    "udp_rpc_listener"]["dead_times"]["retry_listen"]["value"],
                "INM_RETRYING_WRITE_RPC_PERIOD": performance_settings[
                    "inm_rpc_agent"]["dead_times"]["retry_write_rpc"]["value"],
                "INM_ANSWER_AGENT_MAIN_LOOP_PERIOD": performance_settings[
                    "inm_rpc_agent"]["dead_times"]["main_loop"]["value"],
                "AUTOCONFIG_BUFFERS_FLUSHER_MAIN_LOOP_PERIOD": performance_settings[
                    "autoconfig_buffers_flusher"]["dead_times"]["main_loop"]["value"],
                "SAVE_INM_OUTPUT_ON_FILE_MAIN_LOOP_PERIOD": performance_settings[
                    "inm_output_data_saver"]["dead_times"]["main_loop"]["value"],
                "RPC_TO_SET_INM_CHECKER_LOOP_PERIOD": performance_settings[
                    "inm_output_data_saver"]["dead_times"]["set_inm_checker"]["value"],
                "RPC_TO_READ_INM_CHECKER_LOOP_PERIOD": performance_settings[
                    "inm_output_data_saver"]["dead_times"]["read_inm_checker"]["value"],
                "NEXT_REQUIREMENT_LOOP_PERIOD": performance_settings[
                    "inm_output_data_saver"]["dead_times"]["next_requirement"]["value"]
            }
        else:
            self._FUTURES_LOOP_SLEEP_TIMERS = {
                "REMOTE_CONTROL_SERVER_RETRY_LISTEN_TIME": 0.1,
                "INM_RETRYING_WRITE_RPC_PERIOD": 0.2,
                "INM_ANSWER_AGENT_MAIN_LOOP_PERIOD": 0.1,
                "AUTOCONFIG_BUFFERS_FLUSHER_MAIN_LOOP_PERIOD": 0.01,
                "SAVE_INM_OUTPUT_ON_FILE_MAIN_LOOP_PERIOD": 0.01,
                "RPC_TO_SET_INM_CHECKER_LOOP_PERIOD": 0.5,
                "RPC_TO_READ_INM_CHECKER_LOOP_PERIOD": 0.5,
                "NEXT_REQUIREMENT_LOOP_PERIOD": 0.2,
            }
        # Minimum output INM data objects to save threshold
        if (performance_settings != None):
            self.MINIMUM_OUTPUT_INM_DATA_OBJECTS_QUANTITY_TO_SAVE_THRESHOLD = 10
        else:
            self.MINIMUM_OUTPUT_INM_DATA_OBJECTS_QUANTITY_TO_SAVE_THRESHOLD = performance_settings[
                "inm_output_data_saver"]["properties"][
                    "MINIMUM_OUTPUT_INM_DATA_OBJECTS_QUANTITY_TO_SAVE_THRESHOLD"]["value"]
        # inm_output_data_saver flag for keep it activate:
        self._INM_OUTPUT_DATA_SAVER_ON_FLAG = False
        # End the tracking of the __init__ health:
        self.health_watchdog.end_track("__init__")

    async def _udp_rpc_listener(self):
        '''Read asynchronously the UDP server incoming data'''
        while (1):
            self.health_watchdog.begin_track("udp_rpc_listener")
            # Try listen human client requests
            try:
                # Cache suspected requests
                # print("a")
                data_dir_tuple = self._udp_server.socket.recvfrom(
                    self._udp_rpc_buffer_size)
                # print("b")
                self.rcvd_data = data_dir_tuple[0]
                self.client_sock_addr = data_dir_tuple[1]
                # If listening fails, doesn't matter, the script continues:
            except socket.timeout:
                self._logger.error("Connection timeout.")
                await asyncio.sleep(self._FUTURES_LOOP_SLEEP_TIMERS["REMOTE_CONTROL_SERVER_RETRY_LISTEN_TIME"])
                self.rcvd_data = [0]
                continue
            except BlockingIOError as e:
                await asyncio.sleep(self._FUTURES_LOOP_SLEEP_TIMERS["REMOTE_CONTROL_SERVER_RETRY_LISTEN_TIME"])
                self.rcvd_data = [0]
                continue
            except Exception as e:
                self._logger.error('{}'.format(e))
                await asyncio.sleep(self._FUTURES_LOOP_SLEEP_TIMERS["REMOTE_CONTROL_SERVER_RETRY_LISTEN_TIME"])
                self.rcvd_data = [0]
                continue

            # If no data received:
            if (len(self.rcvd_data) < 2):
                self.rcvd_data = None
            # Requests monitor:
            if (self._read_counter > 1000):
                self._pack_counter += 1000
                self._logger.debug('Message received from client at {}, at {}. Received packages: {}'.format(
                    self.client_sock_addr,
                    datetime.datetime.now(),
                    self._pack_counter))
                self._read_counter = 0
            self._read_counter += 1

            # If no data received, do it:
            if (self.rcvd_data == None):
                self._logger.error('No data received.')
                await asyncio.sleep(self._FUTURES_LOOP_SLEEP_TIMERS["REMOTE_CONTROL_SERVER_RETRY_LISTEN_TIME"])
                continue

            # Check the received data size:
            elif (len(self.rcvd_data) < 3 or len(self.rcvd_data) > self._udp_rpc_buffer_size):
                self._logger.error("Package has an invalid size.")
                await asyncio.sleep(self._FUTURES_LOOP_SLEEP_TIMERS["REMOTE_CONTROL_SERVER_RETRY_LISTEN_TIME"])
                continue

            # If package is good:
            elif CksmFletcher16.evaluarDatagrama(self.rcvd_data):
                question_obj = self._parse_raw_message_to_rpc(
                    raw_message=self.rcvd_data)
                self._hmi_questions_queue.append(question_obj)
            # self._logger.debug(self.rcvd_data)

            await asyncio.sleep(self._FUTURES_LOOP_SLEEP_TIMERS["REMOTE_CONTROL_SERVER_RETRY_LISTEN_TIME"])

    async def _inm_rpc_agent(self):
        """This function answer the hmi client rpc and via INM objects according to
        INM responses."""
        current_question = {"question": None,
                            "is_already_answered": True}
        while (1):
            self.health_watchdog.begin_track("inm_rpc_agent")
            if (current_question["is_already_answered"] == True):
                # Next question:
                if (len(self._hmi_questions_queue) > 0):
                    # Process questions one by one:
                    current_question[
                        "question"] = self._hmi_questions_queue.pop(0)
                    self._vn100_controller.write(
                        self._format_question_object_to_inm_ascii_string(current_question["question"]))
                    current_question["is_already_answered"] = False
            else:
                # // Try to listen the INM current question answer //
                # Check if the answer is in the output buffer:
                if (current_question["question"] != None):
                    for current_turing_machine_head_position in range(len(self._vn100_controller.output)):
                        vn100_output_object = self._vn100_controller.output[
                            current_turing_machine_head_position]
                        # Search into "string" INM objects only:
                        if (vn100_output_object["type"] == "string"):
                            # Command response is found:
                            # Next "mistake" sucks my dick, cz it works well:
                            if (vn100_output_object["content"]["command"]["name"] == self._functions_dict[current_question[
                                    "question"]["function"]]["response_criteria"]["command"]):
                                # Validate according to rpc type:
                                # Case read a register only:
                                if (vn100_output_object["content"]["command"]["name"] == "READ_REGISTER"):
                                    # Ensure the rpc args vs. response content:
                                    current_question[
                                        "is_already_answered"] = self._check_answer_validity_of_read_register(
                                        response_command_content=vn100_output_object,
                                        current_question=current_question)
                                    # Remove the INM object from the buffer:
                                    self._vn100_controller.output.pop(
                                        current_turing_machine_head_position)
                                    # If rpc is from user settings descriptor:
                                    if (current_question["is_already_answered"] == True and
                                            "user_settings_order" in current_question["question"].keys()):
                                        _response = {
                                            "user_settings_order": current_question["question"]["user_settings_order"],
                                            "content": vn100_output_object
                                        }
                                        self._user_settings_rpc_responses_queue.append(
                                            _response)
                                    # Break the for loop to avoid index error:
                                    break
                                # Case write a register
                                elif (vn100_output_object["content"]["command"]["name"] == "WRITE_REGISTER"):
                                    # Ensure the rpc args vs. response content:
                                    current_question[
                                        "is_already_answered"] = self._check_answer_validity_of_written_register(
                                        response_command_content=vn100_output_object,
                                        current_question=current_question)
                                    # Remove the INM object from the buffer:
                                    self._vn100_controller.output.pop(
                                        current_turing_machine_head_position)
                                    # If rpc is from user settings descriptor:
                                    if (current_question["is_already_answered"] == True and
                                            "user_settings_order" in current_question["question"].keys()):
                                        _response = {
                                            "user_settings_order": current_question["question"]["user_settings_order"],
                                            "content": vn100_output_object
                                        }
                                        self._user_settings_rpc_responses_queue.append(
                                            _response)
                                    # Break the for loop to avoid index error:
                                    break
                                    # Case write settings into static memory:
                                elif (vn100_output_object["content"]["command"]["name"] == "WRITE_SETTINGS"):
                                    current_question["is_already_answered"] = True
                                    # Remove the INM object from the buffer:
                                    self._vn100_controller.output.pop(
                                        current_turing_machine_head_position)
                                    # If rpc is from user settings descriptor:
                                    if (current_question["is_already_answered"] == True and
                                            "user_settings_order" in current_question["question"].keys()):
                                        _response = {
                                            "user_settings_order": current_question["question"]["user_settings_order"],
                                            "content": vn100_output_object
                                        }
                                        self._user_settings_rpc_responses_queue.append(
                                            _response)
                                    # Break the for loop to avoid index error:
                                    break
                                else:
                                    # RPC unavailable yet:
                                    self._logger.error("The RPC named {} is unavailable but it is in the INM. You must develop this feature.".format(
                                        vn100_output_object["content"]["command"]["name"]
                                    ))
                                    current_question["is_already_answered"] == True
                                    break
                    if (current_question["is_already_answered"] == False):
                        # Try to resend rpc to INM:
                        self._vn100_controller.write(
                            self._format_question_object_to_inm_ascii_string(current_question["question"]))
                        self._logger.debug("Rewriting question: {}".format(
                            current_question["question"]))
                        await asyncio.sleep(self._FUTURES_LOOP_SLEEP_TIMERS["INM_RETRYING_WRITE_RPC_PERIOD"])
            await asyncio.sleep(self._FUTURES_LOOP_SLEEP_TIMERS["INM_ANSWER_AGENT_MAIN_LOOP_PERIOD"])

    def _check_answer_validity_of_read_register(self,
                                                response_command_content,
                                                current_question):
        # Convert the question in an INM ASCII-formatted string, then use the reference parser
        # db to parse it:
        _inm_question_response_criteria_register_name = self._functions_dict[
            current_question["question"]["function"]]["response_criteria"]["register_name"]
        # self._logger.debug(current_question["question"])
        # self._logger.debug(_inm_question_response_criteria_register_name)
        # self._logger.debug(
        #     response_command_content["content"]["content"])
        # SYSTEM_GET_BINARY_OUTPUT_REGISTERS case:
        if (_inm_question_response_criteria_register_name == "BINARY_OUTPUT_REGISTER_n"):
            _inm_question_response_criteria_register_name = _inm_question_response_criteria_register_name.replace(
                "n",
                str(current_question["question"]["args"]["Binary_output_register_number"]))
        # self._logger.debug(_inm_question_response_criteria_register_name)
        # Check if both objects have equal register name:
        if (_inm_question_response_criteria_register_name == response_command_content[
                "content"]["content"]["RegisterNumber"]["name"]):
            self._logger.debug("Reading register RPC was executed succesfully.")
            self._logger.debug(
                current_question["question"]["function"])
            self._logger.debug(response_command_content["content"]["content"])
            return True
        self._logger.debug("Answer is not coincident according to the rpc.")
        self._logger.debug(
            current_question["question"]["function"])
        self._logger.debug(response_command_content["content"]["content"])
        return False

    def _check_answer_validity_of_written_register(self,
                                                   response_command_content,
                                                   current_question):
        # Convert the question in an INM ASCII-formatted string, then use the reference parser
        # db to parse it:
        _inm_question = self._format_question_object_to_inm_ascii_string(
            current_question["question"])
        # Convert it on a inm response object:
        _inm_question = self._vn100_controller.parser.reference_db.get_string_data_structure(
            list(_inm_question))
        # Check if both objects have equal key:value pairs contents:
        if (_inm_question["content"] == response_command_content["content"]["content"]):
            self._logger.debug("Writing register RPC was executed succesfully.")
            self._logger.debug(_inm_question["content"])
            self._logger.debug(response_command_content["content"]["content"])
            return True
        self._logger.debug("Answer is not coincident according to the rpc.")
        self._logger.debug(_inm_question["content"])
        self._logger.debug(response_command_content["content"]["content"])
        return False

    def _format_question_object_to_inm_ascii_string(self, question_obj):
        response = None
        if (question_obj is not None):
            # Execute the rpc:
            try:
                if (len(question_obj["args"]) == 0):
                    response = self._functions_dict[question_obj["function"]]["fx"](
                    )
                else:
                    response = self._functions_dict[question_obj["function"]]["fx"](
                        **question_obj["args"])
            except Exception as e:
                self._logger.error(
                    "The RPC function is not valid: {}".format(e))
        return response

    async def _autoconfig_buffers_flusher(self):
        '''This task runs at beginning. While the "_set_user_inm_configuration" is trying to set the INM,
        It's possible that the INM is sending asynchronous binary and ASCII-formatted string data. Then, this task
        will be cleaning the I/O buffers of unnecesary data to avoid overflow them.'''
        while (self._is_autoconfiguring == True):
            self.health_watchdog.begin_track("autoconfig_buffers_flusher")
            if (len(self._vn100_controller.output) > 0):
                for current_turing_machine_head_position in range(len(self._vn100_controller.output)):
                    vn100_output_object = self._vn100_controller.output[
                        current_turing_machine_head_position]
                    # Binary INM objects only:
                    if (vn100_output_object["type"] == "binary"):
                        # self._logger.debug(vn100_output_object)
                        # Remove the INM object from the buffer:
                        self._vn100_controller.output.pop(
                            current_turing_machine_head_position)
                        # Break the for loop to avoid index error:
                        break
                    # ASCII formatted string INM objects:
                    if (vn100_output_object["type"] == "string"):
                        command_name = vn100_output_object["content"]["command"]["name"]
                        if (command_name != "READ_REGISTER" or
                            command_name != "WRITE_REGISTER" or
                            command_name != "WRITE_SETTINGS" or
                            command_name != "RESTORE_FACTORY_SETTINGS" or
                                command_name != "ERROR"):
                            # self._logger.debug(vn100_output_object)
                            # Remove the INM object from the buffer:
                            self._vn100_controller.output.pop(
                                current_turing_machine_head_position)
                        del command_name
                        # Break the for loop to avoid index error:
                        break
            await asyncio.sleep(self._FUTURES_LOOP_SLEEP_TIMERS["AUTOCONFIG_BUFFERS_FLUSHER_MAIN_LOOP_PERIOD"])
        # If the while loop is over, finish the watchdog tracking:
        self.health_watchdog.end_track("autoconfig_buffers_flusher")

    async def _inm_output_data_agent(self):
        self.health_watchdog.begin_track("set_user_inm_configuration")
        # Check the INM configuration
        if (await self._set_user_inm_configuration() == True):
            self.health_watchdog.end_track("set_user_inm_configuration")
            # End the _autoconfig_buffers_flusher task:
            self._is_autoconfiguring = False
            self._logger.info(
                "INM configuration is already setted succesfully. Saving data...")
            # self._breakpoint()
            # Throw a dedicated thread for the following task:
            self._INM_OUTPUT_DATA_SAVER_ON_FLAG = True
            data_saver_thread = Thread(
                group=None,
                target=self._inm_output_data_saver,
                args=[])
            data_saver_thread.start()
        else:
            error_msg = "INM settings can't be setted. INM data output won't be saved. Finally, this program ends now."
            self._logger.error(error_msg)
            raise Exception(error_msg)

    def _inm_output_data_saver(self):
        # This process must be executed into a dedicated thread or processor core, depending on the
        # OS and/or hardware ability.
        while (self._INM_OUTPUT_DATA_SAVER_ON_FLAG == True):
            self.health_watchdog.begin_track("inm_output_data_saver")
            while (len(self._vn100_controller.output) > self.MINIMUM_OUTPUT_INM_DATA_OBJECTS_QUANTITY_TO_SAVE_THRESHOLD):
                # self._logger.debug("{} inm output data objects to save.".format(
                #     len(self._vn100_controller.output)))
                for current_turing_machine_head_position in range(len(self._vn100_controller.output)):
                    vn100_output_object = self._vn100_controller.output[
                        current_turing_machine_head_position]
                    # Binary INM objects only:
                    if (vn100_output_object["type"] == "binary"):
                        # self._logger.debug(vn100_output_object)
                        # Save data on file:
                        if (self._inm_output_file != None):
                            self._inm_output_file.write(
                                self._csv_line_formatter(vn100_output_object["content"]))
                        if (self._inm_output_callback != None):
                            if callable(self._inm_output_callback) == True:
                                self._inm_output_callback(
                                    vn100_output_object)
                        # Remove the INM object from the buffer:
                        self._vn100_controller.output.pop(
                            current_turing_machine_head_position)
                        # Break the for loop to avoid index error:
                        break
            time.sleep(
                self._FUTURES_LOOP_SLEEP_TIMERS["SAVE_INM_OUTPUT_ON_FILE_MAIN_LOOP_PERIOD"])
        # If the while loop is over, finish the watchdog tracking:
        self.health_watchdog.end_track("inm_output_data_saver")

    def _csv_line_formatter(self, vn100_output_object):
        return "{},{},{},{},{},{},{},{}\r\n".format(
            vn100_output_object["temp"]["value"],
            vn100_output_object["pres"]["value"],
            vn100_output_object["yaw"]["value"],
            vn100_output_object["pitch"]["value"],
            vn100_output_object["roll"]["value"],
            vn100_output_object["accel[0]"]["value"],
            vn100_output_object["accel[1]"]["value"],
            vn100_output_object["accel[2]"]["value"]
        )

    async def serve(self):
        await asyncio.gather(
            asyncio.ensure_future(self._autoconfig_buffers_flusher()),
            asyncio.ensure_future(self._vn100_controller.serve()),
            asyncio.ensure_future(self._udp_rpc_listener()),
            asyncio.ensure_future(self._inm_output_data_agent()),
            asyncio.ensure_future(self._inm_rpc_agent()))

    def _parse_raw_message_to_rpc(self, raw_message):
        '''Returns an rpc object from the raw message given.'''
        # quitar el checksum
        lMsjRecibido = list(raw_message)
        for i in range(0, 2):
            lMsjRecibido.pop(0)
        raw_message = bytearray(lMsjRecibido)
        # Decode message:
        message = raw_message.decode("utf-8", "strict")
        self._logger.debug(message)
        # Convert json message to rpc object message:
        message = json.loads(message)
        self._logger.debug("rpc: {}".format(message['function']))
        return message

    def shutdown(self):
        # End the _inm_output_data_saver process thread:
        self._INM_OUTPUT_DATA_SAVER_ON_FLAG = False
        # Close files and other asynchronous resources:
        self._inm_output_file.close()
        self._vn100_controller.shutdown()
        self.health_watchdog.shutdown()

    async def _set_user_inm_configuration(self):
        """On this task it will check the current INM settings, if isn't corresponding,
        it will try to set the INM ensuring according to user's settings descriptor."""
        # Read and compare from user's settings descriptor to current INM settings:
        # Task result declaration
        task_result = 1
        # Read requirements:
        for requirement in self._user_settings_descriptor["content"].items():
            # Try to read first:
            read_requirement = self._get_instead_of_set_first_rpc_converter(
                requirement=requirement)
            self._hmi_questions_queue.append(read_requirement)
            # Declaration of validity of this task is already made:
            this_requirement_is_checked = False
            while (this_requirement_is_checked == False):
                # Look for answer, with the user settings order:
                if (len(self._user_settings_rpc_responses_queue) > 0):
                    for suspected_answer in self._user_settings_rpc_responses_queue:
                        if ((int(suspected_answer["user_settings_order"]) == int(requirement[0])) and
                            ((suspected_answer["content"]["content"]
                              ["command"]["name"] == "READ_REGISTER"))):
                            if (self._user_settings_check_answer_validity_of_rw_register(
                                response_command_content=suspected_answer["content"],
                                    current_requirement=requirement[1]) == False):
                                self._logger.debug(suspected_answer)
                                # Try to set the INM:
                                self._logger.info(
                                    "Trying to set the INM...")
                                write_requirement = self._get_write_requirement(
                                    requirement=requirement)
                                self._hmi_questions_queue.append(
                                    requirement[1])
                                # Declaration of validity of this requirement is already setted:
                                this_requirement_is_setted = False
                                while (this_requirement_is_setted == False):
                                    # Look for answer, with the user settings order:
                                    if (len(self._user_settings_rpc_responses_queue) > 0):
                                        for suspected_answer in self._user_settings_rpc_responses_queue:
                                            if ((int(suspected_answer["user_settings_order"]) == int(requirement[0])) and
                                                (suspected_answer["content"]["content"]
                                                         ["command"]["name"] == "WRITE_REGISTER")
                                                ):
                                                if (self._user_settings_check_answer_validity_of_rw_register(
                                                    response_command_content=suspected_answer["content"],
                                                        current_requirement=requirement[1]) == False):
                                                    task_result *= 0
                                                else:
                                                    task_result *= 1
                                                # End the set while loop:
                                                this_requirement_is_setted = True
                                                # Next requirement:
                                                this_requirement_is_checked = True
                                                # End the set for loop:
                                                break
                                        # Yield worker thread to other future on this event loop, of this checker while loop:
                                        await asyncio.sleep(self._FUTURES_LOOP_SLEEP_TIMERS["RPC_TO_SET_INM_CHECKER_LOOP_PERIOD"])
                            else:
                                task_result *= 1
                            # Next requirement:
                            this_requirement_is_checked = True
                            # End the for loop that look for response:
                            break
                # Since it doesn't make sense continue when a bad task result occurs,
                # end checker while loop:
                if (bool(task_result) == False):
                    break
                # Yield worker thread to other future on this event loop, of this checker while loop:
                await asyncio.sleep(self._FUTURES_LOOP_SLEEP_TIMERS["RPC_TO_READ_INM_CHECKER_LOOP_PERIOD"])
            # Since it doesn't make sense continue when a bad task result occurs,
            # end requirement reader for loop too:
            if (bool(task_result) == False):
                break
            # Yield worker thread to other future on this event loop, of this requirement reader for loop:
            await asyncio.sleep(self._FUTURES_LOOP_SLEEP_TIMERS["NEXT_REQUIREMENT_LOOP_PERIOD"])
        return bool(task_result)

    def _breakpoint(self):
        """Only debug purposes."""
        while (1):
            pass

    def _user_settings_check_answer_validity_of_rw_register(self,
                                                            response_command_content,
                                                            current_requirement):
        # Convert the question in an INM ASCII-formatted string, then use the reference parser
        # db to parse it:
        _inm_question = self._format_question_object_to_inm_ascii_string(
            current_requirement)
        # Convert it on a inm response object:
        _inm_question = self._vn100_controller.parser.reference_db.get_string_data_structure(
            list(_inm_question))
        # Check if both objects have equal key:value pairs contents:
        if (_inm_question["content"] == response_command_content["content"]["content"]):
            self._logger.info(
                "User setting register RPC was executed succesfully.")
            self._logger.info(_inm_question["content"])
            self._logger.info(response_command_content["content"]["content"])
            return True
        self._logger.warning("Answer is not coincident according to the rpc {}.".format(
            current_requirement["function"]))
        self._logger.warning(
            "Setting values should be: {}".format(_inm_question["content"]))
        self._logger.warning("Current setting values: {}".format(
            response_command_content["content"]["content"]))
        return False

    def _get_instead_of_set_first_rpc_converter(self,
                                                requirement):
        read_function = requirement[1]["function"].replace("_SET_", "_GET_")
        read_msg = {}
        # self._logger.debug(requirement[0])
        # Binary output register case:
        if (read_function == "SYSTEM_GET_BINARY_OUTPUT_REGISTERS"):
            read_msg.update({
                'function': read_function,
                'args': {"Binary_output_register_number": int(requirement[1][
                    "args"]["Binary_output_register_number"])},
                'user_settings_order': int(requirement[0])})
        # Otherwise:
        else:
            read_msg.update({
                'function': read_function,
                'args': {},
                'user_settings_order': int(requirement[0])})
        # self._logger.debug(read_msg)
        return read_msg

    def _get_write_requirement(self,
                               requirement):
        _msg = requirement[1]
        _msg.update({
            'user_settings_order': int(requirement[0])})
        # self._logger.debug(_msg)
        return _msg
