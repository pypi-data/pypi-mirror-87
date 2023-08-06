import sys
import logging
import threading


class Logger(object):
    _instance_lock = threading.Lock()
    _logger = logging.getLogger("log")

    def __new__(cls, *args, **kwargs):
        if not hasattr(Logger, "_instance"):
            with Logger._instance_lock:
                if not hasattr(Logger, "_instance"):
                    log_level = logging.DEBUG
                    enable_console = True
                    enable_file = True
                    file_name = "oBIX.log"

                    cls._logger.setLevel(log_level)
                    log_format = "[%(levelname)-8s] %(asctime)s >> %(message)s"
                    date_format = "%Y-%m-%d %H:%M:%S"
                    formatter = logging.Formatter(log_format, date_format)
                    if enable_file:
                        file_handler = logging.FileHandler(file_name, encoding='utf-8')
                        file_handler.setLevel(log_level)
                        file_handler.setFormatter(formatter)
                        cls._logger.addHandler(file_handler)

                    if enable_console:
                        console_handler = logging.StreamHandler(sys.stdout)
                        console_handler.setLevel(log_level)
                        console_handler.setFormatter(formatter)
                        cls._logger.addHandler(console_handler)

                    Logger._instance = object.__new__(cls, *args, **kwargs)
        return Logger._instance

    @classmethod
    def instance(cls):
        return Logger()._logger
