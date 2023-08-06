# coding: utf-8
import os
import logging

from ubik.core import conf

def get_logger(log_file=conf.get('settings', 'log_file'), name='ubik', level=conf.get('logger', 'level')):
    """
    Ubik file logger
    """
    # Create log file if not exist
    if not os.path.exists(log_file):
        open(log_file, 'w').close()

    logger = logging.getLogger('ubik')
    # Create file handler which logs even debug messages
    fh = logging.FileHandler(log_file)
    # Create console handler with a higher log level
    ch = logging.StreamHandler()
    # Create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # Set logger level
    if level == "2":
        logger.setLevel(logging.ERROR)
        fh.setLevel(logging.ERROR)
    elif level == "3":
        logger.setLevel(logging.DEBUG)
        fh.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
        fh.setLevel(logging.INFO)
    ch.setLevel(logging.ERROR)

    # Add the handlers to logger
    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger

def get_stream_logger(name='ubik-cli'):
    """
    Cli (stream) logger
    """
    stream_logger = logging.getLogger(name)
    ch = logging.StreamHandler()
    stream_logger.setLevel(logging.INFO)
    ch.setLevel(logging.INFO)
    stream_logger.addHandler(ch)
    stream_logger.disabled = True
    return stream_logger

logger = get_logger()
stream_logger = get_stream_logger()
