# By SL, Sept.2,2016
# Modifications by AW, Apr, 2017
# this module to be imported into main progarm
# TCP: Ethernet communication 

import socket  # Import socket module
import numpy as np

DEBUG = False


def s16(value):
    return -(value & 0x8000) | (value & 0x7fff)


def rms(y):  # calculate the rms value for the latest 100 elements in x if more than 100 elements
    if len(y) > 100:
        x = y[len(y) - 100:]  # x has the latest 100 elements
    else:
        x = y
    n = len(x)
    return np.sqrt(np.sum(np.square(x - np.mean(x))) / n)


class TCP(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.s = socket.socket()  # Create a socket object
        self.s.settimeout(5)  # timeout set to 1 second

        if self.s.connect((host, port)) != None:
            print "\nTCP_Error: couldn't connect to", host

    def __del__(self):
        self.s.close()

    def write_reg(self, com, data):
        if self.s.sendall(com + ' ' + str(data) + '\r\n') != None:
            print "\nTCP_Error: sending command failed !", com
            return False
        return True

    def read_reg(self, com):
        if self.s.sendall(com + '\r\n') != None:
            print "\nTCP_Error: sending command failed !", com
            return False
        try:
            recv_msg = self.s.recv(64)

        except socket.timeout:
            print "\nTCP_Error: receiving data timeout !", com

            return False

        int_str, EOL_str = recv_msg.split("\n\r")
        return int(int_str)

    def read_MBver(self):
        if self.s.sendall('FL:BUF:*IDN?\r\n') != None:
            print "\nTCP_Error: sending command failed !"
            return False
        try:
            recv_msg = self.s.recv(64)

        except socket.timeout:
            print "\nTCP_Error: receiving data timeout !"
            return False
        return recv_msg

    def read_buffer(self, com):  # read back 16 words (Unsigned 32bit) from hardware, 16 is defined in MB firmware
        try:
            if self.s.sendall(com + '\r\n') != None:
                print "\nTCP_Error: sending command failed !", com
                return False
        except socket.error:
            print "TCP_Error: socket closed!"
            return False
        try:
            recv_msg = self.s.recv(1024)
        except socket.timeout:
            print "\nTCP_Error: receiving data timeout !", com
            return False

        if DEBUG is True:
            print "received:", recv_msg
        int_list_str, EOL_str = recv_msg.split("\n\r")
        int_list = int_list_str.split(",")  # get a list of numbers
        data = []  # empty list
        for i in range(16):
            data.append(int(int_list.pop(0)))
        return data  # return a "list" of 16 numbers (32 bit unsigned)

    def read_ffifo_wd(self, which):  # read back fast fifo occupancy
        if which is 0:
            msg = 'ABFIFO:WD?\r\n'
        else:
            msg = 'CDFIFO:WD?\r\n'
        try:
            if self.s.sendall(msg) != None:
                print "\nTCP_Error: sending command failed !"
                return False
        except socket.error:
            print "TCP_Error: socket closed!"
            return False
        try:
            recv_msg = self.s.recv(64)
        except socket.timeout:
            print "\nTCP_Error: receiving data timeout !"
            return False
        int_str, EOL_str = recv_msg.split("\n\r")
        return int(int_str)

    def read_sfifo_wd(self):  # read back fast fifo occupancy
        msg = 'SFIFO:WD?\r\n'
        try:
            if self.s.sendall(msg) != None:
                print "\nTCP_Error: sending command failed !"
                return False
        except socket.error:
            print "TCP_Error: socket closed!"
            return False
        try:
            recv_msg = self.s.recv(64)
        except socket.timeout:
            print "\nTCP_Error: receiving data timeout !"
            return False
        int_str, EOL_str = recv_msg.split("\n\r")
        return int(int_str)

    def read_waveform(self, which, num):  # read back waveform from hardware, from channel A/B, or C/D
        if which is 0:
            msg = 'FFIFO:AB?'
        else:
            msg = 'FFIFO:CD?'

        waveform = []
        waveform.append([])
        waveform.append([])
        loop = num // 16;
        # print "read waveform loop:", loop
        for j in range(loop):
            data = self.read_buffer(msg)
            if data is False:
                print "read back failed!"
                return False
            for i in range(16):
                waveform[0].append(s16(data[i]))
                waveform[1].append(data[i] >> 16)
        return waveform  # return 2D list

    def destroy(self):
        self.s.close()
