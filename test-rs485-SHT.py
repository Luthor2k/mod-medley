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
import tkinter
from tkinter import ttk

import sv_ttk


#polling timing for modbus devices in ms
polling_speed = 100


def poll():
    #update temperature / humidity readout
    readings = getSHT()
    temperatureReading.set(readings[0]/10)
    humidityReading.set(readings[1]/10)
    print(f"temperature: {temperatureReading.get()}")
    print(f"humidity: {humidityReading.get()}")

    #check for SSR command and update its status if there's a change
    print(ssrSetpoint.get())
    if ssrSetpoint.get() != ssrReading:
        print("switch!")
        SHTclient.close()
        time.sleep(0.1)
        SSRclient.connect()
        time.sleep(0.1)
        setSSR(ssrSetpoint.get())
        time.sleep(0.1)
        SSRclient.close()
        time.sleep(0.1)
        SHTclient.connect()
        time.sleep(0.1)


    root.after(polling_speed, poll)    # Schedule the poll() function

# create client object
SHTclient = ModbusSerialClient(
            "COM3",
            framer=ModbusRtuFramer,
            # timeout=10,
            # retries=3,
            # retry_on_empty=False,
            # close_comm_on_error=False,.
            # strict=True,
            baudrate=9600,
            bytesize=8,
            parity="N",
            stopbits=1,
            # handle_local_echo=False,
        )

SSRclient = ModbusSerialClient(
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


def getSHT():
    #read_input_registers(address: int, count: int = 1, slave: int = 0, **kwargs: Any)
    rr = SHTclient.read_input_registers(0x0001, 2, slave = 0x0001)
    #print(f"reg return: {rr}")
    #print(f"reg value: {rr.registers}")
    SHTraw = rr.registers
    return SHTraw

def getSSR():
    ssrSetpoint = 0
    ssrValue = SSRclient.read_coils(0x00, slave = 0x0004)
    ssrSetpoint = ssrValue.bits[0]
    print(f"ssr: {ssrSetpoint}")
    return ssrSetpoint


def setSSR(status):
    print(f"SSR applied setpoint: {status}")
    ssrSetSuccess = False
    SSRclient.write_coil(0x00, True, slave = 0x0004)
    return ssrSetSuccess

def main():
    global root
    global temperatureReading
    global humidityReading
    global SSRclient
    global SHTclient
    global ssrReading
    global ssrSetpoint

    root = tkinter.Tk()
    root.title("modbus test")
    sv_ttk.set_theme("light")

    #--------Tk Variables------
    temperatureReading = tkinter.DoubleVar()
    humidityReading = tkinter.DoubleVar()
    temperatureReading.set(99.9)
    humidityReading.set(99.9)
    ssrSetpoint = tkinter.BooleanVar()

    # create all of the frames
    mainFrame = ttk.LabelFrame(root, text="SHT20:")

    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)


    temperatureReadoutTitle = ttk.Label(mainFrame, text="Temperature:")
    temperatureReadoutTitle.grid(row=0, column=0, padx=5, pady=(10, 10), sticky="ew")
    temperatureReadout = ttk.Label(mainFrame, textvariable=temperatureReading)
    temperatureReadout.grid(row=0, column=1, padx=5, pady=(10, 10), sticky="ew")

    humidityReadoutTitle = ttk.Label(mainFrame, text="Humidity:")
    humidityReadoutTitle.grid(row=1, column=0, padx=5, pady=(10, 10), sticky="ew")
    humidityReadout = ttk.Label(mainFrame, textvariable=humidityReading)
    humidityReadout.grid(row=1, column=1, padx=5, pady=(10, 10), sticky="ew")

    ssrCheckbox = ttk.Checkbutton(mainFrame, text="SSR Control", variable=ssrSetpoint)
    ssrCheckbox.grid(row=2, column=0, sticky="w")

    mainFrame.pack()
    
    # connect to ssr, get it status, then disconnect
    SSRclient.connect()
    ssrReading = getSSR()
    ssrSetpoint.set(ssrReading)
    SSRclient.close()
    
    time.sleep(1)
    
    # connect to SHT and leave open for live readings
    SHTclient.connect()

    # Schedule the poll() function to be called periodically 
    root.after(polling_speed, poll)

    print("enter mainloop")
    root.mainloop() 

    # disconnect device
    SHTclient.close()



if __name__ == "__main__":
    main()