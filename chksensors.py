import serial
import struct
import time
import threading

class ReadThread(threading.Thread):
    def __init__(self, id, name, ser):
        threading.Thread.__init__(self)
        self.threadID = id
        self.name = name
        self.ser = ser

    def run(self, ser):
        while True:
            try:
                head = self.ser.read(1)
                if len(head) < 1 or head[0] != 0x55:
                    continue
                length = self.ser.read(1)
                package = self.ser.read(length[0])
                handlePackage(package)
                time.sleep(0.01)
            except:
                print("something is wrong in read thread, exit!")
                break

    def handlePackage(self, pac):
        if pac[0] == 1: # IMU
            orientation = struct.unpack('3f', pac[1:])
            print('Orientation, Yaw: %f, Pitch: %f, Roll: %f' % orientation)
        elif pac[0] == 2: # ultrasonic
            distance = struct.unpack('f', pac[1:])
            print('Distance: %f'%distance)
        elif pac[0] == 6: # battery info
            batinfo = struct.unpack('5fi', pac[1:])
            print('Battery, charge: %d, health: %.2f, full: %.2f, remain: %.2f, voltage: %.2f, current: %.2f'%batinfo)
        elif pac[0] == 7: # device info
            devinfo = struct.unpack('5I', pac[1:])
            print('Device, uid: %u, firmware version: %u.%u, hardware version: %u.%u'%devinfo)
        elif pac[0] == 10: # key event
            keyinfo = struck.unpack('2B', pac[1:])
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
        while True:
            try:
                self.ser.write(self.naxi)
                time.sleep(0.02)
                self.ser.write(self.range) 
                time.sleep(0.02)
            except:
                print('something is wrong in write thread, exit!')
                break
        
if __name__ == '__main__':
    try:
        vcom = serial.Serial('COM12', 115200)
    except Exception as e:
        print('Error: serial open faild')
    rthread = ReadThread(1, 'read_thread', vcom)                
    wthread = WriteThread(2, 'write_thread', vcom)
    rthread.start()
    wthread.start()
    rthread.join()
    wthread.join()
    print('Exit, Bye!')
