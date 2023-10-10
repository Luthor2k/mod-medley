#!/usr/bin/env python


from pymodbus.client import ModbusSerialClient

from pymodbus.transaction import (
    #    ModbusAsciiFramer,
    #    ModbusBinaryFramer,
    ModbusRtuFramer,
    ModbusSocketFramer,
    ModbusTlsFramer,
)


import time

# create client object

client = ModbusSerialClient(
            "COM3",
            framer=ModbusRtuFramer,
            # timeout=10,
            # retries=3,
            # retry_on_empty=False,
            # close_comm_on_error=False,.
            # strict=True,
            baudrate=115200,
            bytesize=8,
            parity="N",
            stopbits=1,
            # handle_local_echo=False,
        )

# connect to device
client.connect()


#address of M5 SSR controller: 0x0004
#SSR coil 0x0000
#LED holding 0x0000 RGB565
#ver holding 0x0001
#addr holding 0x0002

'''
#cycle the SSR
#write_coil(address: int, value: bool, slave: int = 0, **kwargs: Any)
client.write_coil(0x00, 0, 0x0004)
time.sleep(0.5)

client.write_coil(0x00, 1, 0x0004)
time.sleep(0.5)

client.write_coil(0x00, 0, 0x0004)
'''


#write a colour to the RGB LED
#write_register(address: int, value: int, slave: int = 0, **kwargs: Any)

purple = 0x817c
orange = 0xfde0
red = 0xf800
black = 0x0000

#write purple to the LED
rr = client.write_register(0x0000, orange, slave = 0x0004)
print(f"wrote: {rr}")

#read_holding_registers(address: int, count: int = 1, slave: int = 0, **kwargs: Any)
rr = client.read_holding_registers(0x0000, 4, slave = 0x0004)
print(f"reg value: {rr.registers}")

rr = client.read_holding_registers(0x0001, 4, slave = 0x0004)
print(f"reg value: {rr.registers}")

rr = client.read_holding_registers(0x0002, 4, slave = 0x0004)
print(f"reg value: {rr.registers}")

#time.sleep(0.5)

'''
#write orange to the LED
rr = client.write_register(0x0000, orange, 0x0004)
print(f"wrote: {rr}")
time.sleep(0.5)

#write red to the LED
rr = client.write_register(0x0000, red, 0x0004)
print(f"wrote: {rr}")
time.sleep(0.5)

#write black to the LED
rr = client.write_register(0x0000, black, 0x0004)
print(f"wrote: {rr}")
'''


# disconnect device
client.close()