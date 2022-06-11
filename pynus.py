#!/usr/bin/env python3
"""
------------------------------------------------------------------------------
 NUS client for Nordic nRF based systems.
------------------------------------------------------------------------------
"""
import sys
import optparse
import tty, termios
import threading
import platform
import logging
import asyncio
from bleak import BleakClient
from bleak import BleakClient
from bleak import _logger as logger
from bleak.uuids import uuid16_dict


UART_TX_UUID = "6e400002-b5a3-f393-e0a9-e50e24dcca9e" #Nordic NUS characteristic for TX
UART_RX_UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e" #Nordic NUS characteristic for RX

class PyNUS:
    def __init__(self, address):
        self.address = address
        self.run = True
        self.input = b""

    def _notification_handler(self, sender, data):
        sys.stdout.write(data.decode())
        sys.stdout.flush()

    def _process_pc_terminal(self):
        # Setup terminal to raw mode
        old_settings = termios.tcgetattr(sys.stdin.fileno())
        try :
            tty.setraw(sys.stdin.fileno())
            while self.run :
                ch = bytes(sys.stdin.read(1), encoding='utf8')
                if (ch[0] == 0x3) :            # Ctrl+C
                    self.run = False
                self.input += ch[0:1]
        finally :
            # Restore teminal mode
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old_settings)

    async def client_run(self):
        async with BleakClient(self.address, loop=asyncio.get_event_loop()) as client:

            # Wait for BLE client to be connected
            x = client.connect()
            print("Connected: {0}".format(x))

            # Wait for data to be sent from client
            await client.start_notify(UART_RX_UUID, self._notification_handler)

            pc_terminal_thread = threading.Thread(target=self._process_pc_terminal)
            pc_terminal_thread.daemon = True
            pc_terminal_thread.start()

            while self.run :
                if len(self.input) > 0 :
                    await client.write_gatt_char(UART_TX_UUID,self.input)
                    self.input = b""

                #give some time to do other tasks
                await asyncio.sleep(0.1)

def main():
    try :
        parser = optparse.OptionParser(usage='%prog -a <mac_address>', version='1.0')

        parser.add_option('-a', '--address',
                  action='store',
                  dest="address",
                  type="string",
                  default=None,
                  help='target MAC address.'
                  )

        options, args = parser.parse_args()

    except Exception as e :
        print(e)
        print("For help use --help")
        sys.exit(2)

    if not options.address :
        parser.print_help()
        exit(2)

    pynus = PyNUS(options.address)
    asyncio.run(pynus.client_run())
    print("Disconnected.")

if __name__ == "__main__":
    main()
