# VN-100's database driver.
# See VN-100 User Manual.
# Document number: UM001 v2.05.
# This is the Python 3 version.
# Author of this script: Andrés Eduardo Torres Hernández.


import sqlite3
from io import StringIO
from .logger import init_logger
import os


class VN100_DB:
    """VN-100's database driver.
    See VN-100 User Manual.
    Document number: UM001 v2.05."""

    def __init__(
            self,
            db_connection):
        # Set logger
        self._logger = init_logger(__name__)
        # Load the db in RAM:
        # Read database to tempfile
        self._logger.info("loading VN100 config database in RAM...")
        tempfile = StringIO()
        for line in db_connection.iterdump():
            tempfile.write('%s\n' % line)
        db_connection.close()
        tempfile.seek(0)

        # Create a database in memory and import from tempfile
        self.db = sqlite3.connect(":memory:")
        self.db.cursor().executescript(tempfile.read())
        self.db.commit()
        self.db.row_factory = sqlite3.Row
        self._logger.info("VN100 config database loaded in RAM succesfully.")

        # Make the workbench:
        self._make_workbench()

    def _make_workbench(self):
        # Database structural architecture configuration for binary messages:
        self.db_binary_structural_arch = {
            "binary_output_fields": {
                "table_fields": {
                    "id": 0,
                    "name": 1,
                    "group": 2,
                    "bit_offset": 3,
                    "payload_length": 4
                }
            },
            "binary_output_groups": {
                "table_fields": {
                    "id": 0,
                    "name": 1
                }
            },
            "binary_output_variables": {
                "table_fields": {
                    "id": 0,
                    "name": 1,
                    "resolution_type": 2,
                    "field": 3,
                    "units": 4
                }
            },
            "binary_output_variable_resolution_types": {
                "table_fields": {
                    "id": 0,
                    "name": 1,
                    "bit_length": 2
                }
            }
        }
        # Database structural architecture configuration for string messages:
        self.db_string_structural_arch = {
            "uart_command_responses": {
                "table_fields": {
                    "id": 0,
                    "name": 1,
                    "verbatim_name": 2
                }
            },
            "uart_commands_fields_relationships": {
                "table_fields": {
                    "id": 0,
                    "command": 1,
                    "field": 2,
                    "relative_order": 3
                }
            },
            "uart_command_fields": {
                "table_fields": {
                    "id": 0,
                    "name": 1
                }
            },
            "registers": {
                "table_fields": {
                    "id": 0,
                    "name": 1
                }
            },
            "register_fields": {
                "table_fields": {
                    "id": 0,
                    "field_name": 1,
                    "resolution_type": 2
                }
            },
            "registers_register_fields_relationships": {
                "table_fields": {
                    "id": 0,
                    "register": 1,
                    "register_field": 2,
                    "relative_order": 3,
                    "is_mandatory": 4
                }
            },
            "string_field_resolution_types": {
                "table_fields": {
                    "id": 0,
                    "name": 1
                }
            }
        }
        # Resolution type converter functions
        cursorObj = self.db.cursor()
        cursorObj.execute(
            'SELECT * FROM string_field_resolution_types')
        _sfrt = cursorObj.fetchall()
        sfrt = {rtype[self.db_string_structural_arch[
            'string_field_resolution_types']['table_fields']['id']]: rtype[
                self.db_string_structural_arch['string_field_resolution_types'][
                    'table_fields']['name']] for rtype in _sfrt}
        self._resolution_type_tools = {
            'functions': {
                "string": (lambda x: str(x)),
                "integer": (lambda x: str(int(x))),
                "float": (lambda x: str(float(x)))
            },
            'id_functions': sfrt
        }
        # self._logger.debug(self._resolution_type_tools)

    def get_binary_data_structure(self, header):
        """Returns the data structure and the calculated message payload according to the given header.
        args: (
            header: a list of integers with the header content of the message.
                The header format is according to the section 5.3 of VN-100 User Manual (pg. 40).
            )"""
        cursorObj = self.db.cursor()
        payload = 0
        # Detect enabled groups:
        groups_enabled = {}
        for i in range(8):
            if ((header[0] >> i) & 1):
                groups_enabled.update({(i + 1): {}})
        # Sort groups_enabled keys:
        groups_enabled = {
            k: groups_enabled[k] for k in sorted(groups_enabled)}
        # Detect enabled fields:
        ind_header = 1
        for group in groups_enabled.keys():
            for bit_offset in range(16):
                if ((header[ind_header] >> bit_offset) & 1):
                    _active_fields_information_from_db = self._get_active_fields_information_from_db(
                        group=group,
                        field_bit_offset=bit_offset,
                        cursorObj=cursorObj
                    )
                    groups_enabled[group].update(
                        _active_fields_information_from_db["field_info"])
                    payload += _active_fields_information_from_db["payload"]
            ind_header += 1
        # self._logger.debug("groups_enabled: {}".format(groups_enabled))
        return {
            "payload": payload,
            "structure": groups_enabled
        }

    def _get_active_fields_information_from_db(
            self,
            group,
            field_bit_offset,
            cursorObj):
        field_info = {
            field_bit_offset: {
                "field_id": 0,
                "payload": 0,
                "field_name": "Unknown",
                "group_name": "Unknown",
                "variables": {}
            }
        }
        # Get active fields information from db:
        cursorObj.execute(
            'SELECT * FROM binary_output_fields WHERE ("group" == {} and bit_offset == {})'.format(group, field_bit_offset))
        bof = cursorObj.fetchall()
        for field in bof:
            # Determine total payload length:
            payload = field[self.db_binary_structural_arch["binary_output_fields"]
                            ["table_fields"]["payload_length"]]
            # self._logger.debug(groups_enabled[field[self.db_binary_structural_arch["binary_output_fields"]
            #                                         ["table_fields"]["group"]]])
            # Set the field id:
            field_info[field[self.db_binary_structural_arch["binary_output_fields"]
                             ["table_fields"]["bit_offset"]]]["field_id"] = field[self.db_binary_structural_arch["binary_output_fields"]
                                                                                  ["table_fields"]["id"]]
            # Set the payload length of which field:
            field_info[field[self.db_binary_structural_arch["binary_output_fields"]
                             ["table_fields"]["bit_offset"]]]["payload"] = field[self.db_binary_structural_arch["binary_output_fields"]
                                                                                 ["table_fields"]["payload_length"]]
            # Set the field name of which field
            field_info[field[self.db_binary_structural_arch["binary_output_fields"]
                             ["table_fields"]["bit_offset"]]]["field_name"] = field[self.db_binary_structural_arch["binary_output_fields"]
                                                                                    ["table_fields"]["name"]]
            # Set the group name of which field
            # Get active group from db:
            cursorObj.execute(
                'SELECT * FROM binary_output_groups WHERE ("id" == {})'.format(field[self.db_binary_structural_arch["binary_output_fields"]
                                                                                     ["table_fields"]["group"]]))
            bog = cursorObj.fetchall()
            field_info[field[self.db_binary_structural_arch["binary_output_fields"]
                             ["table_fields"]["bit_offset"]]]["group_name"] = bog[0][
                self.db_binary_structural_arch["binary_output_groups"]["table_fields"][
                    "name"]]
            # Set the variables for which field
            field_info[field[self.db_binary_structural_arch["binary_output_fields"]
                             ["table_fields"]["bit_offset"]]]["variables"].update(
                                 self._get_field_variables_from_db(
                                     field_id=field_info[field[self.db_binary_structural_arch["binary_output_fields"]
                                                               ["table_fields"]["bit_offset"]]]["field_id"],
                                     cursorObj=cursorObj
                                 ))

            # Sort field_info keys:
            field_info = {
                k: field_info[k] for k in sorted(field_info)}
            return {
                "field_info": field_info,
                "payload": payload}

    def _get_field_variables_from_db(
            self,
            field_id,
            cursorObj):
        field_variables = {}
        # Set the variables index:
        cursorObj.execute(
            'SELECT * FROM binary_output_variables WHERE ("field" == {})'.format(field_id))
        bofv = cursorObj.fetchall()
        for variable in bofv:
            field_variables.update({variable[self.db_binary_structural_arch["binary_output_variables"]
                                             ["table_fields"]["name"]]: {
                "variable_id": variable[self.db_binary_structural_arch["binary_output_variables"]
                                        ["table_fields"]["id"]],
                "resolution_type": variable[self.db_binary_structural_arch["binary_output_variables"]
                                            ["table_fields"]["resolution_type"]],
                "units": variable[self.db_binary_structural_arch["binary_output_variables"]
                                  ["table_fields"]["units"]]
            }})
        # Set the resolution_type for which variable:
        for variable, variable_content in field_variables.items():
            cursorObj.execute(
                'SELECT * FROM binary_output_variable_resolution_types WHERE ("id" == {})'.format(variable_content["resolution_type"]))
            bofv_rt = cursorObj.fetchall()
            # self._logger.debug("variable: {}, resolution_type: {}, bit_length: {}".format(
            #     variable,
            #     bofv_rt[0][self.db_binary_structural_arch["binary_output_variable_resolution_types"]
            #                ["table_fields"]["name"]],
            #     bofv_rt[0][self.db_binary_structural_arch["binary_output_variable_resolution_types"]
            #                ["table_fields"]["bit_length"]]))
            variable_content["resolution_type"] = {
                "name": bofv_rt[0][self.db_binary_structural_arch["binary_output_variable_resolution_types"]
                                   ["table_fields"]["name"]],
                "bit_length": bofv_rt[0][self.db_binary_structural_arch["binary_output_variable_resolution_types"]
                                         ["table_fields"]["bit_length"]]
            }
        return field_variables

    def get_string_data_structure(self, list_formatted_package):
        """Returns the data structure to the given package.
        args: (
            list_formatted_package: a list of integers with the header content of the message.
                The string format is according to the section 3.6.1 of VN-100 User Manual (pg. 27).
            )"""
        cursorObj = self.db.cursor()
        # Build a list of words:
        package_words = []
        word = []
        for character in list_formatted_package:
            if (character == int.from_bytes("$".encode("ascii"), "big")):
                continue
            if (character == int.from_bytes(",".encode("ascii"), "big") or
                    character == int.from_bytes("*".encode("ascii"), "big")):
                package_words.append(str(bytes(word), encoding="ascii"))
                word = []
            else:
                word.append(character)
        # self._logger.debug(package_words)
        # //// Build the object: ////
        data_structure = {
            "command": {
                "id": 0,
                "name": "",
                "verbatim_name": ""
            },
            "content": None
        }
        # 1st word id the command code:
        cursorObj.execute(
            'SELECT * FROM uart_command_responses WHERE ("verbatim_name" == "{}")'.format(package_words.pop(0)))
        _answer_from_db = cursorObj.fetchone()
        data_structure["command"]["id"] = _answer_from_db[self.db_string_structural_arch[
            "uart_command_responses"]["table_fields"]["id"]]
        data_structure["command"]["name"] = _answer_from_db[self.db_string_structural_arch[
            "uart_command_responses"]["table_fields"]["name"]]
        data_structure["command"]["verbatim_name"] = _answer_from_db[self.db_string_structural_arch[
            "uart_command_responses"]["table_fields"]["verbatim_name"]]
        # self._logger.debug(data_structure)
        data_structure["content"] = self._synthetize_command_content_structure(
            command_id=data_structure["command"]["id"],
            command_verbatim_name=data_structure["command"]["verbatim_name"],
            package_words=package_words,
            cursorObj=cursorObj)
        # self._logger.debug(data_structure)
        return data_structure

    def _synthetize_command_content_structure(self,
                                              command_id,
                                              command_verbatim_name,
                                              package_words,
                                              cursorObj):
        # Contents declaration:
        contents = {}
        # Words popped counter declaration:
        words_popped_counter = 1
        # Determine the command relative fields:
        cursorObj.execute(
            'SELECT * FROM uart_commands_fields_relationships WHERE ("command" == {})'.format(command_id))
        # self._logger.debug(command_id)
        _answer_from_db = cursorObj.fetchall()
        for row in _answer_from_db:
            cursorObj.execute(
                'SELECT * FROM uart_command_fields WHERE ("id" == {})'.format(
                    row[self.db_string_structural_arch["uart_commands_fields_relationships"]["table_fields"]["field"]]))
            _field_answer_from_db = cursorObj.fetchone()
            # Register-associated commands:
            if (command_verbatim_name == "VNRRG" or
                    command_verbatim_name == "VNWRG"):
                register_words_popped_counter = 0
                # Ensure the relative order of the command words:
                if (words_popped_counter == row[
                        self.db_string_structural_arch["uart_commands_fields_relationships"]["table_fields"]["relative_order"]]):
                    # Fill the RegisterNumber field (1):
                    if (words_popped_counter == 1):
                        cursorObj.execute(
                            'SELECT * FROM registers WHERE ("id" == {})'.format(
                                package_words.pop(0)))
                        words_popped_counter += 1
                        _reg_answer_from_db = cursorObj.fetchone()
                        contents.update(
                            {_field_answer_from_db[self.db_string_structural_arch["uart_command_fields"]["table_fields"]["name"]]: {
                                "id": _reg_answer_from_db[self.db_string_structural_arch["registers"][
                                    "table_fields"]["id"]],
                                "name": _reg_answer_from_db[self.db_string_structural_arch["registers"][
                                    "table_fields"]["name"]]
                            }})
                    # Fill the RegisterContent field (2):
                    elif (words_popped_counter == 2):
                        # self._logger.debug(contents["RegisterNumber"]["id"])
                        cursorObj.execute(
                            'SELECT * FROM registers_register_fields_relationships WHERE ("register" == {})'.format(
                                contents["RegisterNumber"]["id"]))
                        _reg_fields_relationships_answer_from_db = cursorObj.fetchall()
                        # Fill the RegisterContent index with register field names:
                        _RegisterContent = {}
                        for reg_row in _reg_fields_relationships_answer_from_db:
                            cursorObj.execute(
                                'SELECT * FROM register_fields WHERE ("id" == {})'.format(reg_row[
                                    self.db_string_structural_arch["registers_register_fields_relationships"]["table_fields"]["register_field"]]))
                            _reg_field_answer_from_db = cursorObj.fetchone()
                            # self._logger.debug(
                            #     "package_words length: {}".format(len(package_words)))
                            # self._logger.debug("field: {}   is_mandatory: {}".format(
                            #     _reg_field_answer_from_db[self.db_string_structural_arch[
                            #         "register_fields"]["table_fields"]["field_name"]],
                            #     reg_row[
                            #         self.db_string_structural_arch["registers_register_fields_relationships"]["table_fields"]["is_mandatory"]]))
                            if (len(package_words) == 0 and
                                reg_row[self.db_string_structural_arch["registers_register_fields_relationships"][
                                    "table_fields"]["is_mandatory"]] == 0):
                                break
                            # OutputFields special case:
                            if (len(package_words) > 0 and _reg_field_answer_from_db[self.db_string_structural_arch[
                                    "register_fields"]["table_fields"]["field_name"]] == "OutputField"):
                                # Determine the number of iterations for OutputFields:
                                _output_fields_words = len(package_words)
                                for _output_field_current_index in range(_output_fields_words):
                                    _RegisterContent.update(
                                        {"_".join(["OutputField", str(_output_field_current_index)]): package_words.pop(0)})
                                    # self._logger.debug(_RegisterContent)
                                # Since the "OutputField" fields are the last on "async_data_output_type", when the for loop ends,
                                # breaks the reg_row for loop:
                                break
                            _RegisterContent.update({_reg_field_answer_from_db[self.db_string_structural_arch[
                                "register_fields"]["table_fields"]["field_name"]]: self._resolution_type_tools[
                                    'functions'][self._resolution_type_tools['id_functions'][
                                        _reg_field_answer_from_db[self.db_string_structural_arch[
                                "register_fields"]["table_fields"]["resolution_type"]]]](package_words.pop(0))})
                        contents.update({_field_answer_from_db[self.db_string_structural_arch["uart_command_fields"][
                            "table_fields"]["name"]]: _RegisterContent})
        # self._logger.debug(contents)
        return contents

    def shutdown(self):
        self.db.close()
