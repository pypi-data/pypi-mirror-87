# VN-100's parser.
# See VN-100 User Manual.
# Document number: UM001 v2.05.
# This is the Python 3 version.
# Author of this script: Andrés Eduardo Torres Hernández.

from .driver_db import VN100_DB
from .logger import init_logger
from .resources import CRC16_CCITT, C8bit_cksm
import struct


class VN100_Parser:
    """VN-100's parser.
    See VN-100 User Manual.
    Document number: UM001 v2.05."""

    def __init__(
            self,
            bytes_stream_list,
            reference_db_connection,
            performance_settings=None):
        # Set logger:
        self._logger = init_logger(__name__)
        # Set buffers:
        self.input_buffer = bytes_stream_list
        self.output = []
        # Set the reference database:
        self.reference_db = VN100_DB(reference_db_connection)
        # ////// Binary outputs /////////
        # Integrity sequence length:
        # CRC-16 bits have 2 bytes of length.
        self.INTEGRITY_SEQUENCE_LENGTH = 2
        # Sync byte have 1 byte (obviously):
        self.SYNC_BYTE_LENGTH = 1
        # Group header have 1 byte:
        self.GROUP_HEADER_LENGTH = 1
        # Group fields header have 2 bytes:
        self.GROUP_FIELDS_HEADER_LENGTH = 2
        # VN100 maximun length of an async binary message:
        if (performance_settings != None):
            self.BIN_MESSAGE_MAX_LENGTH = performance_settings[
                "properties"]["BIN_MESSAGE_MAX_LENGTH"]["value"]
        else:
            self.BIN_MESSAGE_MAX_LENGTH = 600
        # This value sets the input buffer overflow threshold
        # according to n times self.BIN_MESSAGE_MAX_LENGTH:
        if (performance_settings != None):
            self.BUFFER_OVERFLOW_THRESHOLD_RATIO = performance_settings[
                "properties"]["BUFFER_OVERFLOW_THRESHOLD_RATIO"]["value"]
        else:
            self.BUFFER_OVERFLOW_THRESHOLD_RATIO = 100
        # Current check status values of bytes:
        PARSER_BYTE_CHECK_STATUS_enum = enumerate([
            "UNCHECKED",
            "BINARY_CHECKED",
            "ALL_CHECKED"
        ])
        # Create a pair normal-inverted dictionary object for optimal searchs:
        normal_PARSER_BYTE_CHECK_STATUS_enum = dict(
            PARSER_BYTE_CHECK_STATUS_enum)
        inverted_PARSER_BYTE_CHECK_STATUS_enum = {
            y: x for x, y in normal_PARSER_BYTE_CHECK_STATUS_enum.items()}
        self.PARSER_BYTE_CHECK_STATUS = {
            "normal": normal_PARSER_BYTE_CHECK_STATUS_enum,
            "inverted": inverted_PARSER_BYTE_CHECK_STATUS_enum
        }

    def parse(self):
        """Yields a parsed data stream objects from a stream list of bytes"""
        # self._logger.debug("Begin parsing cycle...")
        # Clean the buffer of old and bad data:
        self._clean_buffer_of_old_and_bad_data()
        package = self._scan_for_a_package()
        if (package["message"] is not None):
            _msj = {
                "type": "",
                "content": None
            }
            if (package["type"] == "binary"):
                _msj["type"] = "binary"
                _msj["content"] = self._convert_binary_package_to_vn_objects(
                    package)
            elif (package["type"] == "string"):
                _msj["type"] = "string"
                _msj["content"] = package["message"]
            # Put the new message into buffer:
            if (_msj["content"] != None):
                self.output.append(_msj)

    def _clean_buffer_of_old_and_bad_data(self):
        '''Clean the input buffer of bad, old and unnecessary data.'''
        # Scan, from the end to beginning:
        current_input_buffer_length = len(self.input_buffer)
        for current_turing_machine_head_position in range((current_input_buffer_length - 1), -1, -1):
            #
            #
            # Case of "ALL_CHECKED" bytes marked:
            # If the item has "ALL_CKECKED" status value and the position is beyond to maximum
            # twice message length threshold, then delete it. The reason for do this is because it's normal that each
            # read frame from the Async_Serial _reader contains partial truly INM message frames:
            if ((self.input_buffer[current_turing_machine_head_position][1] == self.PARSER_BYTE_CHECK_STATUS[
                    "inverted"]["ALL_CHECKED"]) and
                    ((current_input_buffer_length - current_turing_machine_head_position) > (2 * self.BIN_MESSAGE_MAX_LENGTH))):
                self.input_buffer.pop(current_turing_machine_head_position)
            #
            #
            # Case of buffer queue overflow:
            # If the items are beyond to buffer overflow threshold, then delete them:
            if ((current_input_buffer_length - current_turing_machine_head_position) > (
                    self.BUFFER_OVERFLOW_THRESHOLD_RATIO * self.BIN_MESSAGE_MAX_LENGTH)):
                self._logger.debug("Cleaning old and bad input buffer...")
                self.input_buffer.pop(current_turing_machine_head_position)

    def _scan_for_a_package(self):
        """Return a VN-100's package if it is found."""
        # Result declaration:
        result = None
        data_structure = None
        result_type = "None"
        # Scan:
        for current_turing_machine_head_position in range(len(self.input_buffer)):
            # Look for a binary package:
            try:
                answer = self._scan_for_binary_package(
                    current_turing_machine_head_position=current_turing_machine_head_position)
            except TypeError as e:
                self._logger.debug(e)
                answer = {"result_code": "break"}
            # self._logger.debug(answer)
            if (answer["result_code"] == "continue"):
                pass
            elif (answer["result_code"] == "break"):
                pass
            else:
                result_type = answer["result_code"]
                result = answer["result"]
                data_structure = answer["data_structure"]
                break
            # Look for an ASCII-formatted string package:
            try:
                answer = self._scan_for_ascii_string_package(
                    current_turing_machine_head_position=current_turing_machine_head_position)
            except TypeError as e:
                self._logger.debug(e)
                answer = {"result_code": "break"}
            if (answer["result_code"] == "continue"):
                continue
            elif (answer["result_code"] == "break"):
                break
            else:
                result_type = answer["result_code"]
                result = answer["data_structure"]
                break
        if (data_structure is None):
            data_structure = {
                "structure": None}
        return {
            "type": result_type,
            "message": result,
            "message_structure": data_structure["structure"]
        }

    def _scan_for_binary_package(self, current_turing_machine_head_position):
        """Return a VN-100's binary package if it is found."""
        # Result declaration:
        result = None
        data_structure = None
        # Mark current buffer item at current_turing_machine_head_position as binary checked:
        self.input_buffer[current_turing_machine_head_position][1] = self.PARSER_BYTE_CHECK_STATUS[
            "inverted"]["BINARY_CHECKED"]
        # Scan:
        # Is it a sync byte?:
        if (self.input_buffer[current_turing_machine_head_position][0] == 0xFA):
            package_length = 0
            # self._logger.debug("0xFA sync byte detected!")
            # Add sync byte length:
            package_length += self.GROUP_HEADER_LENGTH
            # Then, try to determine the header:
            g_qty = 0
            # Determine the groups quantity:
            for j in range(8):
                if ((self.input_buffer[current_turing_machine_head_position + 1][0] >> j) & 1):
                    g_qty += 1
            # ///// Build the header: ///////
            header = [
                self.input_buffer[current_turing_machine_head_position + 1][0]]
            # Add group header length:
            package_length += 1
            _hdr = []
            for rel_pos in range(g_qty):
                # A group fields header has 2 bytes
                try:
                    _gfields = self.input_buffer[current_turing_machine_head_position + 1 + (rel_pos * 2) + 1][0] + ((
                        self.input_buffer[current_turing_machine_head_position + 1 + (rel_pos * 2) + 2][0]) << 8)
                except IndexError as e:
                    self._logger.debug(
                        "Invalid data structure. It will be setted as None. Because: {}".format(e))
                    data_structure = None
                    return {"result_code": "break"}
                _hdr.append(_gfields)
                # Add group fields header length:
                package_length += self.GROUP_FIELDS_HEADER_LENGTH
            header.extend(_hdr)
            # self._logger.debug(header)
            # Try to determine the package length and synthetize the structure:
            try:
                data_structure = self.reference_db.get_binary_data_structure(
                    header)
                # Add payload and integrity sequence lengths:
                package_length += (data_structure["payload"] +
                                   self.INTEGRITY_SEQUENCE_LENGTH)
            except Exception as e:
                self._logger.debug(
                    "Invalid suspected data structure. The for algorithm continues, because: {}".format(e))
                data_structure = None
                return {"result_code": "continue"}
            # self._logger.debug(
            #     "payload length: {}".format(data_structure["payload"]))
            # self._logger.debug("package length: {}".format(package_length))
            # Make a copy of the suspected package
            try:
                suspected_package = [self.input_buffer[index_suspected_package + current_turing_machine_head_position][0]
                                     for index_suspected_package in range(package_length)]
            except Exception as e:
                self._logger.debug("No enough data: {}".format(e))
                return {"result_code": "break"}
            # If the package integrity is good:
            if (CRC16_CCITT.check_vn_binary_data(bytes(suspected_package))):
                # Clean the package content from input buffer:
                for index_detected_package in range(package_length):
                    self.input_buffer.pop(current_turing_machine_head_position)
                result = suspected_package
                # End of scan:
                return {"result_code": "binary",
                        "result": result,
                        "data_structure": data_structure}
            # Suspected package is uncompleted or damaged:
            return {"result_code": "break"}
        else:
            return {"result_code": "continue"}

    def _convert_binary_package_to_vn_objects(self, package):
        """Returns a list of VN-100's variable objects from a binary package"""
        # self._logger.debug(package["message"])
        # self._logger.debug("groups: {}".format(
        #     package["message_structure"]))
        converted_package = {}
        # // Parse message:
        # Initial position for payload:
        current_position_payload = self.SYNC_BYTE_LENGTH + self.GROUP_HEADER_LENGTH + (
            (len(package["message_structure"])
             * self.GROUP_FIELDS_HEADER_LENGTH))
        for group in package["message_structure"].keys():
            for field in package["message_structure"][group].keys():
                for variable, structure_contents in package["message_structure"][group][field]["variables"].items():
                    # self._logger.debug("{}, {}".format(
                    #     variable, structure_contents))
                    _formatted_variable = self._format_from_binary_bytelist_variable(
                        bytelist=package["message"],
                        initial_position=current_position_payload,
                        format=structure_contents["resolution_type"]
                    )
                    current_position_payload += _formatted_variable["processed_byte_length"]
                    converted_package.update({
                        variable: {
                            "field": package["message_structure"][group][field]["field_name"],
                            "group": package["message_structure"][group][field]["group_name"],
                            "units": structure_contents["units"],
                            "value": _formatted_variable["formatted_variable"]
                        }
                    })
        # self._logger.debug("{}".format(converted_package))
        return converted_package

    def _format_from_binary_bytelist_variable(self, bytelist, initial_position, format):
        """Returns a dictionary with:
        1. A formatted byte list variable from the initial position given, to the format given.
        2. The processed byte length.
        """
        # Float case:
        if (format["name"] == "float"):
            # Read byte string:
            _value_variable = []
            _byte_length = int(format["bit_length"] / 8)
            for pos in range(_byte_length):
                _value_variable.append(
                    bytelist[pos + initial_position])
            # self._logger.debug("{}".format(_value_variable))
            # Convert bytelist to float:
            result = struct.unpack("<f", bytes(_value_variable))[0]
        return {"formatted_variable": result,
                "processed_byte_length": _byte_length}

    def _scan_for_ascii_string_package(self, current_turing_machine_head_position):
        """Return a VN-100's binary package if it is found."""
        # Result declaration:
        result = None
        data_structure = None
        # Mark current buffer item at current_turing_machine_head_position as binary checked:
        self.input_buffer[current_turing_machine_head_position][1] = self.PARSER_BYTE_CHECK_STATUS[
            "inverted"]["ALL_CHECKED"]
        # Scan:
        # Is it a "$" character?:
        if (self.input_buffer[current_turing_machine_head_position][0] == int.from_bytes("$".encode("ascii"), "big")):
            # Check if the next two characters are "VN":
            if (self.input_buffer[current_turing_machine_head_position + 1][0] == int.from_bytes("V".encode("ascii"), "big") and
                    self.input_buffer[current_turing_machine_head_position + 2][0] == int.from_bytes("N".encode("ascii"), "big")):
                # Look for an asterisk character:
                for asterisk_search_index in range(current_turing_machine_head_position, len(self.input_buffer)):
                    if (self.input_buffer[asterisk_search_index][0] == int.from_bytes("*".encode("ascii"), "big")):
                        # 1. Ensure suspected message:
                        try:
                            suspected_package = [self.input_buffer[index_suspected_package + current_turing_machine_head_position][0]
                                                 for index_suspected_package in range(
                                asterisk_search_index + (C8bit_cksm.CHECK_SEQUENCE_MESSAGE_LENGTH + 1) - current_turing_machine_head_position)]
                        except Exception as e:
                            self._logger.debug("No enough data: {}".format(e))
                            return {"result_code": "break"}
                        # self._logger.debug(
                        #         bytes(suspected_package))
                        # self._logger.debug(C8bit_cksm.check_data(bytes(suspected_package)))
                        # 2. Analize the suspected message integrity, via 8-bit checksum:
                        if (C8bit_cksm.check_data(bytes(suspected_package)) == True):
                            data_structure = self.reference_db.get_string_data_structure(
                                suspected_package)
                            # Clean the package content from input buffer:
                            for index_detected_package in range(len(suspected_package)):
                                self.input_buffer.pop(
                                    current_turing_machine_head_position)
                            # self._logger.debug("Rcvd_Msg: {}".format(data_structure))
                            # 3. Finish the search and return the data_structure:
                            return {"result_code": "string",
                                    "data_structure": data_structure}
                        # If the package is corrupted or non-coherent, continue:
                        return {"result_code": "continue"}
                return {"result_code": "continue"}
            return {"result_code": "continue"}
        return {"result_code": "continue"}

    def shutdown(self):
        self.reference_db.shutdown()
