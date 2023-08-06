import sys
import traceback
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
import os


ENV = os.getenv('PY_ENV', 'test')
print("environment for logger: {}".format(ENV))
def get_logger(module):
    filename = "inm.log"
    # filename = "/logs/raspi_previa.log"
    print("log filename: {}".format(filename))
    logger = logging.getLogger(module)
    
    if ENV == "development":
        logger.setLevel(logging.DEBUG)
    elif ENV == "test":
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.WARNING)
    
    # file handler
    file_handler = RotatingFileHandler(
        filename=filename, 
        maxBytes=1024000, 
        backupCount=10)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - level: %(levelname)s - filename: %(filename)s - mod: %(module)s - func: %(funcName)s - line: %(lineno)d  - msg: %(message)s')
    
    file_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)

    if ENV == "development" or ENV == "test":
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
    return logger