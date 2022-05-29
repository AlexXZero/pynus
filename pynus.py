#!/usr/bin/env python3
"""
------------------------------------------------------------------------------
 NUS client for Nordic nRF based systems.
------------------------------------------------------------------------------
"""
import sys
import optparse
import tty, termios
import platform
import logging
import asyncio
from bleak import BleakClient
from bleak import BleakClient
from bleak import _logger as logger
from bleak.uuids import uuid16_dict


UART_TX_UUID = "6e400002-b5a3-f393-e0a9-e50e24dcca9e" #Nordic NUS characteristic for TX
UART_RX_UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e" #Nordic NUS characteristic for RX

def notification_handler(sender, data):
    print(data.decode(), end="")

async def main():
    try:
        parser = optparse.OptionParser(usage='%prog -a <mac_address>', version='1.0')

        parser.add_option('-a', '--address',
                  action='store',
                  dest="address",
                  type="string",
                  default=None,
                  help='target MAC address.'
                  )

        options, args = parser.parse_args()

    except Exception as e:
        print(e)
        print("For help use --help")
        sys.exit(2)

    if not options.address:
        parser.print_help()
        exit(2)

    async with BleakClient(options.address, loop=asyncio.get_event_loop()) as client:

        #wait for BLE client to be connected
        x = client.connect()
        print("Connected: {0}".format(x))

        #wait for data to be sent from client
        await client.start_notify(UART_RX_UUID, notification_handler)

        # Setup terminal to raw mode
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        tty.setraw(fd)

        while True : 
            ch = bytes(sys.stdin.read(1), encoding='utf8')
            if (ch[0] == 0x3) :            # Ctrl+C
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                print("Disconnect.")
                break
            await client.write_gatt_char(UART_TX_UUID,ch)

            #give some time to do other tasks
            await asyncio.sleep(0.1)

if __name__ == "__main__":
    asyncio.run(main())
