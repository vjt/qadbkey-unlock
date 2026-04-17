#!/usr/bin/env python3
"""
File: qadbkey-unlock2.py
Modified by carp4 to allow AT+QADBKEY? to be entered directly and result displayed for RM5XX series modems.
Modified by iamromulan to remove the sudo reqirement and query the user to input the AT+QADBKEY? response from the modem.
Authors: hornetfighter515, FatherlyFox
Year: 2021
Version: 2.1
Credits: Original by igem, https://xnux.eu/devices/feature/qadbkey-unlock.c, https://xnux.eu/devices/feature/modem-pp.html
Description: Works to assist in unlocking ADB access for the PinePhone.
P.S. Thankyou for making a functional script hornetfighter515 ❤
"""
import logging
import sys

# Python 3.13 removed the stdlib `crypt` module. `legacycrypt` on PyPI
# ships the exact same C code, same API. Prefer it; fall back to the
# stdlib on Python <= 3.12.
try:
    from legacycrypt import crypt
except ImportError:
    try:
        from crypt import crypt
    except ImportError:
        sys.stderr.write(
            "error: neither `legacycrypt` nor stdlib `crypt` is available.\n"
            "       on Python >= 3.13 run: pip install legacycrypt\n"
        )
        sys.exit(1)


def generateUnlockKey(sn):
    """
    @param sn: the serial number to generate an unlock key for
    """
    salt = "$1${0}$".format(sn)
    c = crypt("SH_adb_quectel", salt)
    return c[12:27]


def main():
    if len(sys.argv) == 2:
        sn = sys.argv[1]
    else:
        sn = input("Enter the AT+QADBKEY? response: ").strip()
    print('AT+QADBKEY="{0}"'.format(generateUnlockKey(sn)))


if __name__ == "__main__":
    logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.ERROR)
    main()
