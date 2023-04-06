# collect-data-envelope.py
# Python script for data collection in SIXT33N Speech version
#
# EE16B Spring 2016
# Emily Naviasky & Nathaniel Mailoa
#

import serial
import sys
import os
import re
import glob
import numpy as np
import datetime

samples = []

# Serial functions


def serial_ports():
    """Lists serial ports
    Raises:
    EnvironmentError:
        On unsupported or unknown platforms
    Returns:
        A list of available serial ports
    """

    if sys.platform.startswith('win'):
        ports = ['COM' + str(i + 1) for i in range(256)]

    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this is to exclude your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')

    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.usbmodem*')

    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return ports


def open_port(port, baud):
    """Open a serial port.
    Args:
    port (string): port to open, on Unix typically begin with '/dev/tty', on
        or 'COM#' on Windows.
    baud (int, optional): baud rate for serial communication
    Raises:
    SerialException: raised for errors from serial communication
    Returns:
      A pySerial object to communicate with the serial port.
    """
    ser = serial.Serial()
    try:
        ser = serial.Serial(port, baud, timeout=10)
        logger.info("Opened serial connection on port %s" % port)
        return ser
    except serial.SerialException:
        raise


def save_txt(buff, txtfile):
    text_file = open(txtfile, 'a')
    text_file.write(','.join([str(x) for x in buff]))
    text_file.write('\n')
    text_file.close()

def generate_filename(dir):
    # Get the current date
    now = datetime.datetime.now()
    day = now.strftime("%d")
    month = now.strftime("%m")

    # Get the number of CSV files in the directory that match the date format
    matching_files = [f for f in os.listdir(dir) if f.endswith('.csv') and f.startswith(f'{day}-{month}-')]
    number = len(matching_files) + 1

    # Generate the filename
    filename = f'{dir}/{month}-{day}-{number}.csv'
    return filename

def run(dir):
    if not os.path.isdir(dir):
        os.makedirs(dir)
    
    filename = generate_filename(dir)
    
    samples = []
    print("EE16B Front End Lab")

    ports = serial_ports()
    print("portrs:")
    print(ports)
    if ports:
        print("Available serial ports:")
        for (i, p) in enumerate(ports):
            print("%d) %s" % (i+1, p))
    else:
        print("No ports available. Check serial connection and try again.")
        print("Exiting...")
        return

    portNo = input("Select the port to use: ")
    ser = serial.Serial(ports[int(portNo)-1])
    ser.baudrate = 38400
    ser.timeout = 20
    # ser.readline()

    print('Collecting data... Please wait.')

    second = 0
    sample_rate = 125   # CHANGE THIS TO MATCH ARDUINO SAMPLE RATE

    while (second < 30):
        samples = []

        if second % 10 == 0:
            print("relax your grip...")
        if second % 10 == 5:
            print("SQUEEZE DA BOTTLE")

        for _ in range(sample_rate):
            sample = (float)(ser.readline().decode().rstrip('\n'))
            sample = abs(sample)
            samples.append(sample)
        save_txt(samples, filename)
        # print(f'{second+1}: Done writing to ' + filename)
        mean = np.mean(samples)
        print(f'{second}: {mean}')
        second += 1

    print(f"Data collection complete! Check {filename}")
    ser.close()


if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print("Usage: python collect-data.py <directory>")
        exit()
    run(sys.argv[1])
