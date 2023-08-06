# A generic UDP - serial HMI
from typing import (
    Callable,
    Any)
import asyncio
from .interface_server import VN_INM_Interface_Server
from threading import Thread
import time
from .config import (
    health_watchdog_configuration as hwc,
    main_performance_configuration as mpc,
    serial_port_settings as sps,
    udp_connection_settings as usc)
from .iusd import inm_user_settings_descriptor as inm_usd


def _init_controller(
        spsettings: dict = sps,
        hwconfig: dict = hwc,
        mpsettings: dict = mpc,
        onerror: Callable = None,
        db_connection: Any = None):
    from .controller import VN100_Controller
    # Create a VN100 controller
    return VN100_Controller(
        serial_port_settings=spsettings,
        vn100_descriptor_database_connection=db_connection,
        health_watchdog_configuration=hwconfig["VN100_Controller_class"],
        Async_Serial_health_watchdog_configuration=hwconfig["Async_Serial_class"],
        health_diagnostics_callback=onerror,
        performance_settings=mpsettings["VN100_Controller_class"])


def _init_rpcserver(
        connsettings: dict = usc):
    from .udp_server import UDP_Server
    # Create a UDP server for the hmi
    udp_server = UDP_Server(udp_connection_settings=connsettings)
    udp_server.start_server()
    return udp_server


def run(
        onerror: Callable = None,
        ondata: Callable = None,
        hwconfig: dict = hwc,
        mpconfig: dict = mpc,
        inm_config: dict = inm_usd,
        db_connection: str = None,
        spsettings: dict = sps,
        connsettings: dict = usc,
        hmi_inm_output_file=None):
    # Life status of this program for health watchdogs:
    this_is_alive = True
    try:
        # setup a controller
        inm_controller = _init_controller(
            spsettings=sps,
            hwconfig=hwc,
            mpsettings=mpc,
            onerror=onerror,
            db_connection=db_connection)
        # Create a UDP HMI to serial port output:
        hmi = VN_INM_Interface_Server(
            health_watchdog_configuration=hwconfig["VN_INM_Interface_Server"],
            health_diagnostics_callback=onerror,
            inm_output_callback=ondata,
            udp_server=_init_rpcserver(
                connsettings=usc),
            vn100_controller=inm_controller,
            inm_output_file=hmi_inm_output_file,
            user_settings_descriptor=inm_config,
            performance_settings=mpconfig["VN_INM_Interface_Server_class"])
        # Define the health watchdogs service:

        def health_watchdogs_service(
                sweep_period):
            while (this_is_alive == True):
                hmi.health_watchdog.serve()
                inm_controller.health_watchdog.serve()
                inm_controller.async_serial_device.health_watchdog.serve()
                time.sleep(sweep_period)
        # Create and throw the health_watchdogs_service thread:
        health_watchdogs_service_thread = Thread(
            group=None,
            target=health_watchdogs_service,
            args=[1])
        health_watchdogs_service_thread.start()

        # Execute services:
        asyncio.get_event_loop().run_until_complete(
            hmi.serve())
    except (KeyboardInterrupt, SystemExit) as e:
        hmi._logger.error(
            "The program has been stopped succesfully.")
        hmi.shutdown()
        # Finish the health watchdogs task:
        this_is_alive = False

    except Exception as e:
        hmi._logger.error(
            "Another kind of exception has been happened: {}".format(e))
        hmi.shutdown()
        # Finish the health watchdogs task:
        this_is_alive = False
