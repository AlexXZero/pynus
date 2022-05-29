# pynus
NUS client for Nordic nRF based systems

Example of cross platform data transmission between Nordic UART Service (NUS) and Python using the Bleak Project and Adafruit nrf52 Libraries

#### Overview

This program establish connection with nRF micro using BLE NUS protocol then you can send data between your PC and the board like normal terminal.

This program was tested using pinewatch as nRF micro and arch linux + python 3.10 on PC side.
Pinewatch was flashed using ztime (https://github.com/AlexXZero/ztime) firmware. On the python side, the Bluetooth Low Energy platform Agnostic Klient for Python (Bleak) project is used for Cross Platform Support.

#### Usage

During this test keys Shift+D were pressed three times. ztime should answered using line "D:NI\r\n" since 'D' character accepted:

ztime test code:
```
static ssize_t ble_nus_write_handler(struct bt_conn *conn, const struct bt_gatt_attr *attr,
                                     const void *buf, uint16_t len, uint16_t offset, uint8_t flags)
{
  for (uint16_t i = 0; i < len; i++) {
    switch (buf[i]) {
    case 'D':
      ble_nus_write("D:NI\r\b", 6);
      break;
    default:
      // TODO
      break;
    }
  }
  return len;
}
```

PC Output:
```
$ ./pynus.py -a C4:AB:AD:F1:CC:33
Connected: <coroutine object BleakClientBlueZDBus.connect at 0x7fd6f42ee810>
D:NI
D:NI
D:NI
Disconnect.
/usr/lib/python3.10/asyncio/events.py:80: RuntimeWarning: coroutine 'BleakClientBlueZDBus.connect' was never awaited
  self._context.run(self._callback, *self._args)
RuntimeWarning: Enable tracemalloc to get the object allocation traceback
```

# Note: This software is not intended for use on the territory of the Russian Federation and the Republic of Belarus. Any problems, up to and including damage to the device on which this software is running, are the responsibility of the user of this device.
