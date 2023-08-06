#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
import time
from .vn100_modules.logger import init_logger


class UDP_Server:
    def __init__(self, udp_connection_settings):
        self._socket_address = (
            udp_connection_settings["IP_address"],
            udp_connection_settings["port"])
        self._ensure_server_flag = False
        self.SOCKET_RECONNECTION_DEAD_TIME = 1

    def start_server(self):
        self._logger = init_logger(__name__)
        while (self._ensure_server_flag == 0):
            try:
                # Create a UDP/IP socket:
                self._logger.debug('Creating a UDP/IP socket...')
                self.socket = socket.socket(
                    family=socket.AF_INET, type=socket.SOCK_DGRAM)
                # Set socket as non-blocking mode:
                self.socket.setblocking(False)
                # Bind software socket to hardware socket:
                self._logger.debug(
                    'Binding software socket to hardware socket...')
                self.socket.bind(self._socket_address)
            except Exception as e:
                self._logger.error(
                    'The hardware socket is unavailable, because: {}'.format(e))
                time.sleep(self.SOCKET_RECONNECTION_DEAD_TIME)
                continue
            self._ensure_server_flag = True
            self._logger.info('Listening at: {}'.format(
                self._socket_address))
