#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 19:51:31 2020

@author: pi
"""


import bluetooth as bt
import os
from urllib.request import urlopen
from urllib.error import URLError
import RPi.GPIO as GPIO
# from wireless import Wireless
import time

myssid=""
mypasswd=""

red = 11
green = 40
blue = 36
def receiveMsg():
    uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
    global myssid
    global mypasswd

    # RFCOMM Port communication prepare
    server_sock = bt.BluetoothSocket(bt.RFCOMM)
    server_sock.bind(('', bt.PORT_ANY))
    server_sock.listen(1)

    port = server_sock.getsockname()[1]

    # Advertise
    bt.advertise_service(server_sock, "BtChat", service_id = uuid, service_classes = [uuid, bt.SERIAL_PORT_CLASS], profiles = [bt.SERIAL_PORT_PROFILE])

    print("Waiting for connection : channel %d" % port)

    client_sock, client_info = server_sock.accept()
    print('accepted')
    while True:
        print("Accepted connection from ", client_info)
        try:
            data = client_sock.recv(1024)
            if len(data) == 0:
                break
            print("received [%s]"%data)
            print("send [%s]"%data)
            a = data.split()
            myssid = a[0]
            mypasswd = a[1]
            ssid = myssid.decode('utf-8')
            passwd = mypasswd.decode('utf-8')
            filename = "/etc/wpa_supplicant/wpa_supplicant.conf"
            #filename = "/home/pi/test.conf"
            f = open(filename, mode='at', encoding='utf-8')
            f.write("\nnetwork={\n")
            str = '\tssid="%s"\n'%(ssid)
            f.write(str)
            str = '\tpsk="%s"\n'%passwd
            f.write(str)
            f.write('\tkey_mgmt=WPA-PSK\n')
            f.write('}\n')
            f.close()

            print("myssid = {}".format(myssid))
            print("my password = {}".format(mypasswd))
            client_sock.send(data[::-1])
        except IOError:
            print("disconnected")
            client_sock.close()
            server_sock.close()
            print("all done")
            break;
        except KeyboardInterrupt:
            print("disconnected")
            client_sock.close()
            server_sock.close()
            print("all done")
            break;

    print("reboot")
    #os.system('sudo reboot')

def internet_on():
    global red
    global green
    global blue
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(red, GPIO.OUT, initial = GPIO.LOW)
    GPIO.setup(green, GPIO.OUT, initial = GPIO.LOW)
    GPIO.setup(blue, GPIO.OUT, initial = GPIO.LOW)
    time.sleep(5)
    try:
        urlopen('http://google.com', timeout = 10)
        print("Connected")
        GPIO.output(red, GPIO.LOW)
        GPIO.output(green, GPIO.LOW)
        GPIO.output(blue, GPIO.HIGH)
        time.sleep(2)
        return True
    except URLError as err:
        print("Not Connected")
        GPIO.output(red, GPIO.HIGH)
        GPIO.output(green, GPIO.LOW)
        GPIO.output(blue, GPIO.LOW)
        time.sleep(2)
        return False
    finally:
        GPIO.cleanup()

#ret = internet_on()
#if ret == False:
#    receiveMsg()
receiveMsg()