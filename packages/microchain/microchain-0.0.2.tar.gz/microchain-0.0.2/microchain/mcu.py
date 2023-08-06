from . import firmware

import sh
import os
import sys
import logging

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

esptool = sh.Command('esptool.py')

def erase_flash(port='/dev/ttyUSB0', chip='auto'):
    esptool(
        '--port', port,
        '--chip', chip,
        'erase_flash',
        _fg=True)

def write_flash(filename='/tmp/microchain-firmware.bin', port='/dev/ttyUSB0', chip='auto', baud='921600'):
    if not os.path.isfile(filename):
        firmware.download(filename)

    esptool(
        '--port', port,
        '--chip', chip,
        '--baud', baud,
        'write_flash',
        '-z', '0x1000',
        filename,
        _fg=True)

def terminal(port='/dev/ttyUSB0', baud='115200'):
    sh.python('-m', 'serial.tools.miniterm', port, baud, _fg=True)

def shell(command, port='/dev/ttyUSB0', baud=115200):
    # sh.rshell(
    #     '--nocolor', '--timing',
    #     '--port', port,
    #     '--baud', baud,
    #     'ls',#*command.split(' '),
    #     _fg=True)
    sh.ampy(
        '--port', port,
        '--baud', baud,
        *command.split(' '),
        _fg=True)