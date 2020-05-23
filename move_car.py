import serial, sys, os, time
import argparse, struct

parser = argparse.ArgumentParser()
parser.add_argument("--left")
parser.add_argument("--right")

args=parser.parse_args()


def open_port(port_name, baud):
    try:
        port = serial.Serial(port_name, baudrate=baud, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, xonxoff=False, rtscts=False, stopbits=serial.STOPBITS_ONE, timeout=1, dsrdtr=True)
        return port
    except(OSError, serial.SerialException):
        print("unable to open port")
        pass
    return

def send_data(port, data):
    s ='S'
    #m = s.encode('utf-8')
    port.write(b'S')
    #print('\x45'.encode('UTF-8'))
    port.write(data)
    port.write(b'E')
    ack = port.read()
  #  port.flush()
    print(ack)
    return ack

def pack_data(data, pktFormat):
    pktData = struct.pack(pktFormat, data[0], data[1])

    return pktData

if (__name__ == "__main__"):
    data = (int(args.left), int(args.right))
    pk_data = pack_data(data, "<2i")
    port = open_port("/dev/ttyACM0", 115200)
    #send_data(port, data)

    ack = 'R'
    while(True):
        if(ack == 'R'):
            send_data(port, pk_data)
            #print ("data_sent")
            ack = port.read()
            print (ack)
