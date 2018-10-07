#! /usr/bin/env python3.7
# -*- coding: utf-8 -*-

"""
Scrape the OBD2 commands webpage at

https://en.wikipedia.org/wiki/OBD-II_PIDs

for PIDs to submit to my engine.
"""

from typing import List, Generator
from contextlib import contextmanager

import serial

SERVICE_01 = 0xC4 # 196
IFACE = '/dev/ttyUSB0'
BAUDRATE = serial.Serial.BAUDRATES[14]


@contextmanager
def encodePIDs(pid_range: int) -> Generator[List[bytes], None, None]:
    """
    Encode an integer range ⊆ [0,255] as bytes.
    """
    try:
        if 0 > pid_range >= 0xFF:
            raise ValueError(f'Expected a value less than {0xFF}, received '
                             f'{pid_range}')

        yield list(map(lambda b: format(b, '02x').encode(), range(pid_range)))
    finally:
        pass


def main() -> None:
    """
    Create tables of PIDs.
    """

    # Generate
    with encodePIDs(SERVICE_01) as pids, \
         serial.Serial(IFACE, baudrate=BAUDRATE, bytesize=8, timeout=1) as ser:

        if not ser.writable():
            raise RuntimeError(f'Unable to write to serial bus {IFACE}')

        ser.write('AL'.encode())

        for pid in pids:
            ser.write(pid)
            response = ser.read()
            print(response)


if __name__ == '__main__':
    main()
