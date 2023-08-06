# Controller
import time
from .vn100_modules import (
    VN100_Parser,
    Async_Serial,
    Health_Watchdog
)
import asyncio
from .vn100_modules.logger import init_logger
import pickle


class VN100_Controller:
    def __init__(self,
                 serial_port_settings,
                 vn100_descriptor_database_connection,
                 health_watchdog_configuration=None,
                 Async_Serial_health_watchdog_configuration=None,
                 health_diagnostics_callback=None,
                 performance_settings=None):
        self._logger = init_logger(__name__)
        # Health watchdog:
        self.health_watchdog = Health_Watchdog(
            "VN100_Controller",
            diagnostics_callback=health_diagnostics_callback,
            timers_configuration=health_watchdog_configuration
        )
        # Track the __init__ health:
        self.health_watchdog.begin_track("__init__")
        # Check if vn100_descriptor_database_connection exists:
        if (vn100_descriptor_database_connection is None):
            error_msg = "There is not a database connection exists. The program stops now."
            self._logger.error(error_msg)
            raise ValueError(error_msg)
        # Create the serial port:
        try:
            if (performance_settings != None):
                self.async_serial_device = Async_Serial(
                    port=serial_port_settings["port"],
                    bit_rate=serial_port_settings["bit_rate"],
                    health_watchdog_configuration=Async_Serial_health_watchdog_configuration,
                    health_diagnostics_callback=health_diagnostics_callback,
                    performance_settings=performance_settings["properties"]["Async_Serial_class_object"]
                )
            else:
                self.async_serial_device = Async_Serial(
                    port=serial_port_settings["port"],
                    bit_rate=serial_port_settings["bit_rate"]
                )
        except Exception as e:
            print("It can't open the serial port '{}' 'because: {}".format(
                serial_port_settings["port"], e))
            pass
        # Create the VN100 parser:
        if (performance_settings != None):
            self.parser = VN100_Parser(
                bytes_stream_list=self.async_serial_device.buffered_read,
                reference_db_connection=vn100_descriptor_database_connection,
                performance_settings=performance_settings["properties"]["VN100_Parser_class_object"])
        else:
            self.parser = VN100_Parser(
                bytes_stream_list=self.async_serial_device.buffered_read,
                reference_db_connection=vn100_descriptor_database_connection)
        # Parser update time, in seconds:
        if (performance_settings != None):
            self.PARSING_UPDATE_TIME = performance_settings["_parse"]["dead_times"]["main_loop"]["value"]
        else:
            self.PARSING_UPDATE_TIME = 0.1
        # VN100 objects read output:
        self.output = self.parser.output
        # Maximum output buffer length:
        if (performance_settings != None):
            self.MAX_OUTPUT_LENGTH = performance_settings["properties"]["MAX_OUTPUT_BUFFER_LENGTH"]["value"]
        else:
            self.MAX_OUTPUT_LENGTH = 65536  # 65536 is default (64 KiB).
        # Minimum input serial port buffer for parsing, according to maximum vn100 binary message length:
        self.MIN_PARSE_INPUT_BUFFER_LENGTH = 2 * \
            (self.parser.BIN_MESSAGE_MAX_LENGTH + 1)
        # End the tracking of the __init__ health:
        self.health_watchdog.end_track("__init__")

    async def _parse(self):
        while (self.async_serial_device.availability == True):
            self.health_watchdog.begin_track("parse")
            # Parse the whole actually filled buffer:
            while (len(self.async_serial_device.buffered_read) > self.MIN_PARSE_INPUT_BUFFER_LENGTH):
                # Parse the input data (only one package):
                # self._logger.debug("self.async_serial_device.buffered_read length: {}".format(
                #     len(self.async_serial_device.buffered_read)
                # ))
                self.parser.parse()
            # Check output length:
            out_length = len(pickle.dumps(self.output))
            if (out_length > self.MAX_OUTPUT_LENGTH):
                self._logger.warning("The output buffer is full ({} bytes max). Earlier objects of data will be lost.".format(
                    self.MAX_OUTPUT_LENGTH))
                while (out_length > self.MAX_OUTPUT_LENGTH):
                    self.output.pop(0)
                    out_length = len(pickle.dumps(self.output))
            self._logger.debug(
                "vn100_object_output_length_len: {} packages, {} bytes on memory.".format(
                    len(self.output),
                    out_length))
            await asyncio.sleep(self.PARSING_UPDATE_TIME)
        # If the main while loop is over, finish the watchdog tracking:
        self.health_watchdog.end_track("parse")

    async def serve(self):
        # Future
        await asyncio.gather(
            asyncio.ensure_future(self._parse()),
            asyncio.ensure_future(self.async_serial_device.serve())
        )

    def write(self, output_message):
        self._logger.debug(output_message)
        self.async_serial_device.send_msg(out_msg=output_message)

    def shutdown(self):
        self.parser.shutdown()
        self.async_serial_device.shutdown()
