import datetime
import json
import os.path
import sys
import serial
import signal
import time
import queue

from roktools import logger, rinex

from .ublox import config as ublox_config
from .ublox import core as ublox_core
from .ublox import constants
from .ublox import helpers
from .ublox import receiver
from .ublox import SERIAL_PORT_STR, BAUD_RATE_STR
from . import OUTPUT_DIR_STR, NAME_STR, FILE_STR, JSON_STR, RATE_STR, MESSAGES_STR

# ------------------------------------------------------------------------------

_record_thread = None

# ------------------------------------------------------------------------------

def config(**kwargs):

    serial_port = kwargs.get(SERIAL_PORT_STR, None)
    conn_config = receiver.detect_connection(serial_port=serial_port)

    serial_port = conn_config[SERIAL_PORT_STR]
    baudrate = conn_config[BAUD_RATE_STR]

    logger.info(f'Attempting to configure device in serial port [ {serial_port},{baudrate} ]')

    with serial.Serial(serial_port, baudrate) as stream:
        
        config_file = kwargs.get(FILE_STR, None)
        json_file = kwargs.get(JSON_STR, None)
        if config_file:
            logger.info(f'Configuring device from file [ {config_file} ]')
            with open(config_file, 'r') as fh:
                ublox_config.set_from_ucenter_file(stream, fh)

        elif json_file:
            logger.info(f'Configuring device from JSON file [ {json_file} ]')
            with open(json_file, 'r') as fh:
                ublox_config.set_from_json_file(stream, fh) 

        else:
            config_dict = {}

            if RATE_STR in kwargs:
                config_dict[constants.RATE_STR] = {
                    constants.MEASUREMENTS_STR : kwargs[RATE_STR],
                    constants.SOLUTION_STR : kwargs[RATE_STR] * 5
                }

            logger.info(f'Configuring device from command line options: {config_dict}')
            ublox_config.set_from_dict(stream, config_dict)



# ------------------------------------------------------------------------------

def detect(serial_port=None, baudrate=None, messages=False):

    config = receiver.detect_config(serial_port=serial_port, baudrate=baudrate, messages=messages)

    if not config:
        return False

    json.dump(config, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write('\n')
    return True



# ------------------------------------------------------------------------------

def reset(**kwargs):

    serial_port = kwargs.get(SERIAL_PORT_STR, None)
    if not serial_port:
        logger.critical('Need to specify the port to be reset')
        return False
    else:
        logger.info(f'Resetting device in [ {serial_port} ]')
        receiver.reset(serial_port)
        return True

# ------------------------------------------------------------------------------

def record(**kwargs):

    logger.debug('Record arguments ' + str(kwargs))

    slice_period = kwargs.get('slice', rinex.FilePeriod.DAILY)
    file_rotation = rinex.FilePeriod.from_string(slice_period)
    recorder_config = {
        'serial_port': kwargs.get(SERIAL_PORT_STR, None),
        'baudrate': kwargs.get(BAUD_RATE_STR, None),
        'file_rotation': file_rotation,
        'output_dir': kwargs.get(OUTPUT_DIR_STR, '.'),
        'receiver_name': kwargs.get(NAME_STR, 'UBLX')
    }

    global _record_thread
    _record_thread = receiver.Recorder(**recorder_config)

    _record_thread.start()


# ------------------------------------------------------------------------------

def interruption_handler(sig, frame):
    logger.info('You pressed Ctrl+C, gracefully closing files and serial streams')

    global _record_thread
    _record_thread.stop()

    sys.exit(0)

signal.signal(signal.SIGINT, interruption_handler)
