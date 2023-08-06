# Health Watchdog is a scrpit health supervisor .
# Author: Andrés Eduardo Torres Hernández
import time
from .logger import init_logger


class Health_Watchdog:
    def __init__(
            self,
            target_class_name,
            diagnostics_callback=None,
            timers_configuration=None):
        self._logger = init_logger(__name__)
        self._target_class_name = target_class_name
        # Begin a dictionary of timers:
        if (timers_configuration != None):
            try:
                self.TIMERS = {timer_name: {
                    "warning_timer_value": float(timer_config["warning_timer_value"]),
                    "error_timer_value": float(timer_config["error_timer_value"]),
                    "_tracker": {
                        "beginning_time": float(0),
                        "on_flag": False
                    }
                } for timer_name, timer_config in timers_configuration.items()}
            except Exception as e:
                self._logger.error(
                    "The timers configuration descriptor is invalid: {}".format(e))
                raise Exception
        else:
            self.TIMERS = None
        # Diagnostics callback
        if (diagnostics_callback != None and
                callable(diagnostics_callback) == True):
            self._diagnostics_callback = diagnostics_callback
        else:
            self._diagnostics_callback = None
            self._logger.info("There is not a diagnostics callback function on the class {}. The health watchdog will report issues to the default logger instead.".format(
                self._target_class_name
            ))

    def begin_track(self, timer):
        if (self.TIMERS != None):
            # self._logger.debug("Checking the {} watchdog timer...".format(timer))
            self.TIMERS[timer]["_tracker"]["beginning_time"] = time.time()
            self.TIMERS[timer]["_tracker"]["on_flag"] = True
        else:
            pass

    def end_track(self, timer):
        if (self.TIMERS != None):
            # self._logger.debug("Finish the check the {} watchdog timer...".format(timer))
            self.TIMERS[timer]["_tracker"]["on_flag"] = False
        else:
            pass

    def serve(self):
        # This function on all instances that contains it, must be throw into a dedicated thread or process.
        if (self.TIMERS != None):
            for timer_name, timer_config in self.TIMERS.items():
                if (timer_config["_tracker"]["on_flag"] == True):
                    if ((time.time() - timer_config["_tracker"]["beginning_time"]) > timer_config["error_timer_value"]):
                        self._throw_error_message(timer_name)
                    elif ((time.time() - timer_config["_tracker"]["beginning_time"]) > timer_config["warning_timer_value"]):
                        self._throw_warning_message(timer_name)
            return
        self._logger.info("There is not any health watchdogs setted on an instance of the class {}.".format(
            self._target_class_name))

    def shutdown(self):
        self.TIMERS = None

    def _throw_error_message(self, timer_name):
        msg = "UNHEALTHY: {}::{}".format(
            self._target_class_name,
            timer_name)
        if (self._diagnostics_callback != None):
            self._diagnostics_callback(msg)
            self._logger.debug(msg)
        else:
            self._logger.error(msg)

    def _throw_warning_message(self, timer_name):
        msg = "DELAYED: {}::{}".format(
            self._target_class_name,
            timer_name)
        if (self._diagnostics_callback != None):
            self._diagnostics_callback(msg)
            self._logger.debug(msg)
        else:
            self._logger.warning(msg)
