import os
import os.path
import shutil
import struct
import tempfile
import time
import threading

import serial

from roktools import logger, rinex
from roktools.time import weektow_to_datetime

from . import helpers
from . import config as ublox_config
from . import core
from . import SERIAL_PORT_STR, BAUD_RATE_STR, DEFAULT_BAUD_RATE

def autodetect_serial_port():
    """
    Attempt to find a serial port in which the receiver is connected. 

    :return: If found, a string with the device specification. Otherwise, None
    """

    serial_port = None

    for port in serial.tools.list_ports.comports():
        if 'u-blox GNSS receiver' in port:
            serial_port = port.device
            break

    return serial_port

# ------------------------------------------------------------------------------

def autodetect_baud_rate(serial_port):
   
    BAUD_RATE_LIST = [9600, 19200, 38400, 57600, 115200, 230400, 460800, 921600]

    baudrate = None
    
    for baud_rate_candidate in BAUD_RATE_LIST:
        with serial.Serial(serial_port, baud_rate_candidate) as ser:
            if ser.isOpen(): ser.close()
            ser.open()
            doc = ser.read(1000)
            ser.close()
            logger.debug(f'Testing baud rate: {baud_rate_candidate}')

            if b'\xb5\x62' in doc:
                baudrate = baud_rate_candidate
                logger.debug(f'Baud rate detected: {baudrate}')
                break

    if baudrate is None:
        baudrate = DEFAULT_BAUD_RATE
        logger.debug(f'Default baud rate selected: {baudrate}')

    return baudrate

# ------------------------------------------------------------------------------

def reset(serial_port):

    serial_stream = serial.Serial(serial_port)
    layer = 3
    payload = struct.pack('<BBBBBBBBBBBBB', 255, 255, 0, 0, 0, 0, 0, 0, 255, 255, 0, 0, layer)
    core.send(core.PacketType.CFG_CFG, payload, serial_stream)

    core.wait_for_ack_nak(core.PacketType.CFG_CFG, serial_stream, timeout=core.TIMEOUT_DEF)
    serial_stream.close()

    logger.info(f'Device reset')

    return True

# ------------------------------------------------------------------------------

def submit_config(doc, serial_port=None, baudrate=None):
    """
    Submit a configuration (using the Receiver configuration standard in JSON
    format)
    """

    if not serial_port:
        serial_port = autodetect_serial_port()

    if not baudrate:
        baudrate = autodetect_baud_rate(serial_port)

    try:
        serial_stream = serial.Serial(serial_port, baudrate)
        ublox_config.set_from_dict(serial_stream, doc)
        serial_stream.close()
        
        return True
 
    except serial.SerialException:
        return False


# ------------------------------------------------------------------------------

def detect_config(serial_port=None, baudrate=None, messages=False):

    config = {}

    try:
        config = detect_connection(serial_port=serial_port, baudrate=baudrate)
        serial_port = config.pop(SERIAL_PORT_STR)
        baudrate = config.pop(BAUD_RATE_STR)
    except Exception as e:
        logger.critical('Could not detect connection: {}. Re-run command'.format(str(e)))
        return None

    with serial.Serial(serial_port, baudrate, **config) as serial_stream:

        try:
            config = ublox_config.get(serial_stream)
            config[SERIAL_PORT_STR] = serial_port
            config[BAUD_RATE_STR] = baudrate
        except Exception as e:
            logger.critical(f'Unable to get receiver parameters. Re-launch the command::{str(e)}')
            return None

        if messages:

            packet_types = set()

            try:
                t_start = time.time()

                for packet in core.ublox_packets(serial_stream, core.TIMEOUT_DEF):

                    elapsed_time = time.time() - t_start

                    ptype = packet[0:2]
                    if ptype not in packet_types:
                        packet_types.add(ptype)

                    if (elapsed_time > 10):
                        break
            except TimeoutError:
                pass

            config['messages'] = [core.PacketType(m).name for m in packet_types]

    return config

# ------------------------------------------------------------------------------


def detect_connection(serial_port=None, baudrate=None):

    if not serial_port:
        logger.debug('No serial port specified, attempting to find one')
        serial_port = autodetect_serial_port()

    if not baudrate:
        logger.debug('No baud rate specified, attempting to find one')
        baudrate = autodetect_baud_rate(serial_port)

    stream = serial.Serial(serial_port, baudrate=baudrate, timeout=core.TIMEOUT_DEF)
    logger.debug(f'Opened connection [ {serial_port} ] --> [ {stream} ]')

    config = {
        SERIAL_PORT_STR: serial_port,
        BAUD_RATE_STR: baudrate
    }

    KEY_IDS = [core.KeyId.CFG_UART1_BAUDRATE, core.KeyId.CFG_UART1_STOPBITS, 
                core.KeyId.CFG_UART1_PARITY, core.KeyId.CFG_UART1_DATABITS]

    key_values = core.submit_valget_packet(KEY_IDS, stream)

    key_id = core.KeyId.CFG_UART1_BAUDRATE
    if key_id in key_values:
        value = key_values[key_id]
        config[BAUD_RATE_STR] = core.parse_key_id_value(key_id, value)

    key_id = core.KeyId.CFG_UART1_STOPBITS
    if key_id in key_values:
        value = key_values[key_id]
        stopbits = core.parse_key_id_value(key_id, value)
        if stopbits == 1:
            config['stopbits'] = serial.STOPBITS_ONE
        elif stopbits == 2:
            config['stopbits'] = serial.STOPBITS_ONE_POINT_FIVE
        elif stopbits == 3:
            config['stopbits'] = serial.STOPBITS_TWO
        else:
            raise ValueError('Half bit not supported by pyserial')

    key_id = core.KeyId.CFG_UART1_PARITY
    if key_id in key_values:
        value = key_values[key_id]
        parity = core.parse_key_id_value(key_id, value)
        if parity == 0:
            config['parity'] = serial.PARITY_NONE
        elif parity == 1:
            config['parity'] = serial.PARITY_ODD
        elif parity == 2:
            config['parity'] = serial.PARITY_EVEN

    key_id = core.KeyId.CFG_UART1_DATABITS
    if key_id in key_values:
        value = key_values[key_id]
        bytesize = core.parse_key_id_value(key_id, value)
        if bytesize == 0:
            config['bytesize'] = serial.EIGHTBITS
        elif bytesize == 1:
            config['bytesize'] = serial.SEVENBITS
    
    logger.debug(f'Serial connection configuration {config}')

    stream.close()

    return config

# ------------------------------------------------------------------------------

class Recorder(threading.Thread):


    def __init__(self, serial_port=None, baudrate=None, file_rotation=rinex.FilePeriod.DAILY,
                 output_dir=".", receiver_name="UBLX"):
        threading.Thread.__init__(self)

        self.slice = file_rotation

        self.output_dir = os.path.abspath(output_dir)
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        self.serial_port = serial_port
        self.baudrate = None
        if not self.serial_port:
            logger.info('Serial port not defined, autodetecting')
            connection_config = detect_connection()
            self.serial_port = connection_config.pop(SERIAL_PORT_STR)
            self.baudrate = connection_config.pop(BAUD_RATE_STR)

        if baudrate:
            self.baudrate = baudrate
        if not self.baudrate:
            self.baudrate = autodetect_baud_rate(self.serial_port)

        self.serial_stream = serial.Serial(self.serial_port, self.baudrate)

        if not self.serial_stream.is_open:
            logger.critical(f'Could not open serial stream [ {self.serial_port} ]')

        self.receiver_name = receiver_name

        self.tempdir = tempfile.mkdtemp(prefix="pyublox_")

        self.current_epoch_suffix = None

        self.fout = None

        logger.info("Writing ubx data from _serial_stream [ {} ] for receiver [ {} ] to files "
                    "in folder [ {} ], with [ {} ] periodicity".format(
                           self.serial_port, self.receiver_name, self.output_dir, self.slice.name))

        logger.debug('Partial files will be written in this temporary folder [ {} ]'.format(self.tempdir))

    # ---

    def run(self):

        logger.debug('Starting recording thread')

        incoming_epoch_suffix = None
        num_packets = 0
        for packet in core.ublox_packets(self.serial_stream, core.TIMEOUT_DEF):

            try:
                packet_type, parsed_packet = core.parse(packet)
            except Exception as e:
                #logger.debug("Could not parse packet: {}".format(e))
                continue
            
            if packet_type == core.PacketType.RXM_RAWX:
                tow = parsed_packet.rcvTow
                week = parsed_packet.week
                epoch = weektow_to_datetime(tow, week)
                num_packets += 1
                incoming_epoch_suffix = self.slice.build_rinex3_epoch(epoch)
                if num_packets % 100 == 0:
                    logger.debug("U-blox RXM_RAWX packet found! Epoch suffix {} , num_packets = {}".format(incoming_epoch_suffix, num_packets))

            if not incoming_epoch_suffix:
                continue

            if not self.current_epoch_suffix or self.current_epoch_suffix != incoming_epoch_suffix:

                self.__close_and_save_partial_file__()

                self.current_epoch_suffix = incoming_epoch_suffix

                filename = os.path.join(self.tempdir,'{}_{}.ubx'.format(self.receiver_name, self.current_epoch_suffix))
                self.fout = open(filename, 'wb')
                logger.info("Created new data file [ {} ]".format(os.path.basename(filename)))

            self.fout.write(core.PREAMBLE)
            self.fout.write(packet)

    # ---

    def stop(self):

        if self.serial_stream:
            self.serial_stream.close()
            logger.info('Closed serial stream from [ {} ]'.format(self.serial_port))

        self.__close_and_save_partial_file__()

        if self.tempdir:
            shutil.rmtree(self.tempdir)

    # ---

    def __close_and_save_partial_file__(self):

        if self.fout:
            filename = self.fout.name

            self.fout.close()

            src = filename
            dst = os.path.join(self.output_dir, os.path.basename(filename))

            logger.debug('Moving [ {} ] -> [ {} ]'.format(src, dst))

            shutil.move(src, dst)
