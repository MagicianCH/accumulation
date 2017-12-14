import serial
import struct
import time
import threading
import argparse

class ReadThread(threading.Thread):
    def __init__(self, id, name, ser):
        threading.Thread.__init__(self)
        self.threadID = id
        self.name = name
        self.ser = ser

    def run(self):
        try:
            while True:
                head = self.ser.read(1)
                if len(head) < 1 or head[0] != 0x55:
                    continue
                length = self.ser.read(1)
                package = self.ser.read(length[0])
                self.handlePackage(package)
                time.sleep(0.01)
        except Exception as e:
            print("read thread exit!")

    def handlePackage(self, pac):
        if pac[0] == 1: # IMU
            orientation = struct.unpack('9f', pac[1:])
            print('Orientation, Yaw: %f, Pitch: %f, Roll: %f' % (orientation[3], orientation[4], orientation[5]))
        elif pac[0] == 2: # ultrasonic
            distance = struct.unpack('f', pac[1:])
            print('Distance: %.2f'%distance)
        elif pac[0] == 6: # battery info
            batinfo = struct.unpack('5fi', pac[1:])
            print('Battery, health: %.2f, full: %.2f, remain: %.2f, voltage: %.2f, current: %.2f, charge: %d'%batinfo)
        elif pac[0] == 7: # device info
            devinfo = struct.unpack('5I', pac[1:])
            print('Device, uid: %u, firmware version: %u.%u, hardware version: %u.%u'%devinfo)
        elif pac[0] == 10: # key event
            keyinfo = struct.unpack('2B', pac[1:])
            if keyinfo[1] == 1:
                print('key %d is pressed!'%keyinfo[0])
            else:
                print('key %d is released!'%keyinfo[0])
        else:
            print('unknown package')

class WriteThread(threading.Thread):
    def __init__(self, id, name, ser):
        threading.Thread.__init__(self)
        self.threadID = id
        self.name = name
        self.naxi = struct.pack('2B', 0x44, 0x01)
        self.range = struct.pack('2B', 0x44, 0x02)
        self.ser = ser

    def run(self):
        try:
            while True:
                self.ser.write(self.naxi)
                time.sleep(0.5)
                self.ser.write(self.range) 
                time.sleep(0.5)
        except:
            print('write thread exit!')
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('port', help='serial port')
    args = parser.parse_args()
    port = args.port
    vcom = serial.Serial(port, 115200)
    rthread = ReadThread(1, 'read_thread', vcom)                
    wthread = WriteThread(2, 'write_thread', vcom)
    rthread.setDaemon(True)
    wthread.setDaemon(True)
    rthread.start()
    wthread.start()
    try: 
        while rthread.is_alive() and wthread.is_alive():
            pass
    except KeyboardInterrupt as e:
        print('exit, bye')
