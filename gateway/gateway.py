""" This is the gateway script
    author: Saku Rautiainen
    saku.rautiainen@iki.fi
 """

#!/usr/bin/env python3
from time import gmtime, strftime
import serial
import requests
import socket
SERIAL_PORT = '/dev/ttyUSB0'
BAUDRATE = 9600
URL = 'localhost:3001/api/data'
N_FIELDS_IN_MSG = 11

def postToWebServer(query):
    query['hostname'] = socket.gethostname()
    print(query)
    try:
        res = requests.post(URL, data=query)
        print(res.text)
    except requests.exceptions.InvalidSchema as e:
        print(e)

def main():
    """ Main function """
    try:
        ser = serial.Serial(
            port=SERIAL_PORT,
            baudrate = 9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )
        print("Serial connection opened")
    except serial.serialutil.SerialException:
        ser = None
        query = {'error_msg' : "No device on serial port: {}".format(SERIAL_PORT),
        'time' : strftime("%Y-%m-%d %H:%M:%S", gmtime())
        }
        postToWebServer(query)


    data_array = []

    while 1 and ser:
        try:
            mesh_msg = str(ser.readline()).split(';')
        except serial.serialutil.SerialException:
            exit(2)
        print(mesh_msg)
        if len(mesh_msg) == N_FIELDS_IN_MSG and mesh_msg[1] == 'R':

            sensor_data = {}
            for i in range(len(mesh_msg)):
                if mesh_msg[i] == 'R':
                    sensor_data['node_id'] = mesh_msg[i+1]
                elif mesh_msg[i] == 'H':
                    sensor_data['humidity'] = mesh_msg[i+1]
                elif mesh_msg[i] == 'T':
                    sensor_data['temperature'] = mesh_msg[i+1]
            sensor_data['time'] = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            data_array.append(sensor_data)

        if len(data_array) > 10:
            query = {'data': data_array}
            postToWebServer(query)


if __name__ == "__main__":
    # execute only if run as a script
    main()
