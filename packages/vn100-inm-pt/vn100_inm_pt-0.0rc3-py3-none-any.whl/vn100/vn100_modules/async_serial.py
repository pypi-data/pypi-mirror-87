# Async serial
from serial import Serial, SerialException
import asyncio
from .logger import init_logger
import os
import pickle
from .health_watchdog import Health_Watchdog


class Async_Serial:
    def __init__(
            self,
            port,
            bit_rate,
            health_watchdog_configuration=None,
            health_diagnostics_callback=None,
            performance_settings=None):
        # Set logger:
        self._logger = init_logger(__name__)
        # Health watchdog:
        self.health_watchdog = Health_Watchdog(
            "Async_Serial",
            diagnostics_callback=health_diagnostics_callback,
            timers_configuration=health_watchdog_configuration
        )
        # Track the __init__ health:
        self.health_watchdog.begin_track("__init__")
        # Serial port configuration:
        self.port = port
        self.bit_rate = bit_rate
        if (performance_settings != None):
            self.timeout = performance_settings["Serial_Port_Object"]["blocking_times"]["read_timeout"]["value"]
        else:
            self.timeout = 0.1
        # Initialize serial port:
        self.serial_port = Serial(
            port=self.port,
            baudrate=self.bit_rate,
            timeout=self.timeout
        )
        # Input buffer:
        self.buffered_read = []  # list of bytes
        # // I/O configurations: //
        # Maximum read package length:
        if (performance_settings != None):
            self._MAX_READ_PACKAGE_LENGTH = performance_settings[
                "properties"]["MAX_READ_PACKAGE_LENGTH"]["value"]
        else:
            self._MAX_READ_PACKAGE_LENGTH = 128  # 128 bytes is default.
        # Maximum read input buffer length:
        if (performance_settings != None):
            self._MAX_BUFFERED_READ_LENGTH = int(performance_settings[
                "properties"]["MAX_READ_BUFFER_SIZE_RATIO"]["value"] * self._MAX_READ_PACKAGE_LENGTH)
        else:
            # 16384 is default (16 KiB).
            self._MAX_BUFFERED_READ_LENGTH = 16384

        # Asynchronous processes dead times:
        if (performance_settings != None):
            self.ASYNC_DEAD_TIMES = {
                "MAIN_LOOP": performance_settings["_reader"]["dead_times"]["main_loop"]["value"],
                "RETRY_RECONNECT_SERIAL_PORT": performance_settings["_reader"]["dead_times"]["retry_reconnect_serial_port"]["value"]
            }
        else:
            self.ASYNC_DEAD_TIMES = {
                "MAIN_LOOP": 0.1,
                "RETRY_RECONNECT_SERIAL_PORT": 0.1
            }

        # Port availability flag
        self.availability = True
        # Try to open this port:
        if (self.serial_port.is_open == False):
            try:
                self._logger.info(
                    "Trying to open the serial port {}...".format(port))
                self.serial_port.open()
            except SerialException as e:
                exception = "Serial port {} has been failed: {}".format(
                    port,
                    e
                )
                self._logger.error(exception)
                raise Exception(exception)
        # End the tracking of the __init__ health:
        self.health_watchdog.end_track("__init__")

    def send_msg(self, out_msg):
        if (self.serial_port.is_open):
            if (out_msg is None):
                self._logger.debug("Output message is none.")
                return
            #ps.parity = serial.PARITY_SPACE
            self.serial_port.write(out_msg)
            self._logger.debug("Write: {}".format(out_msg))
        else:
            exception = "The serial port is closed."
            self._logger.error(exception)
            raise Exception(exception)

    async def _reader(self):
        while (self.availability == True):
            self.health_watchdog.begin_track("reader")
            # self._logger.debug("Port {} is still available.".format(self.port))
            if (self.serial_port.is_open):
                # Read a byte array, and mark each byte for parser. For each byte (as uint8_character),
                # uint8_character[0] is the byte value and uint8_character[1] is the check value. Default is int(0),
                # that means no checked yet for any process since each was created:
                in_msg = [[uint8_character, int(0)] for uint8_character in list(self.serial_port.read(
                    self._MAX_READ_PACKAGE_LENGTH))]
                # self._logger.debug(
                #     "New incoming data: {}".format(in_msg))
                if ((len(pickle.dumps(self.buffered_read)) + len(in_msg)) >= self._MAX_BUFFERED_READ_LENGTH):
                    self._logger.warning("The serial port input buffer is full ({} bytes max). Earlier objects of data will be lost.".format(
                        self._MAX_BUFFERED_READ_LENGTH))
                    while ((len(pickle.dumps(self.buffered_read)) + len(in_msg)) >= self._MAX_BUFFERED_READ_LENGTH):
                        self.buffered_read.pop(0)
                # Store the new message in buffer queue:
                self.buffered_read.extend(in_msg)
                # a = str(in_msg)
                # print("Read: {}".format(a))
                self._logger.debug("buffered_read length: {} bytes from port, {} bytes on memory.".format(
                    len(self.buffered_read),
                    len(pickle.dumps(self.buffered_read))))
                await asyncio.sleep(self.ASYNC_DEAD_TIMES["MAIN_LOOP"])
            else:
                # Try to reconnect it:
                try:
                    self._logger.info(
                        "Trying to open the serial port {}...".format(self.port))
                    self.serial_port.open()
                    await asyncio.sleep(self.ASYNC_DEAD_TIMES["RETRY_RECONNECT_SERIAL_PORT"])
                except SerialException as e:
                    exception = "Serial port {} has been failed: {}".format(
                        self.port,
                        e
                    )
                    self._logger.error(exception)
                    await asyncio.sleep(self.ASYNC_DEAD_TIMES["RETRY_RECONNECT_SERIAL_PORT"])
        # If the main while loop is over, finish the watchdog tracking:
        self.health_watchdog.end_track("reader")

    async def serve(self):
        await asyncio.gather(
            asyncio.ensure_future(self._reader())
        )
    
    def shutdown(self):
        if (self.serial_port.is_open):
            self.serial_port.close()
        self.health_watchdog.shutdown()
