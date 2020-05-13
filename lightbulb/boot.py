from network import WLAN
import machine
from machine import Pin
import urequests
import time
from pysense import Pysense
import pycom
import _thread
import json


ssid = 'Xrosby-Wifi'
wifi_pass = 'boguspass'
get_color_url = "http://klevang.dk:19409/getupdates"
init_url = "http://klevang.dk:19409/init"
board_id = ""
wlan = WLAN(mode=WLAN.STA)
OFF = 0x000000

pycom.heartbeat(False)


def connect(ssid, passw):
    if not wlan.isconnected():
        nets = wlan.scan()
        for net in nets:
            print(net.ssid)
            if net.ssid == ssid:
                print(ssid, ' found!')
                wlan.connect(net.ssid, auth=(net.sec, passw), timeout=5000)
                while not wlan.isconnected():
                    machine.idle() 
                print('WLAN connection to ', ssid,' succesful!')
                break

def post(body, url):
    print(body)
    res = urequests.post(url, headers={"Content-Type": "application/json","Accept": "application/json"}, json=body)
    result_body = res.text
    result_body = eval(result_body)
    res.close()   
    return result_body

def init():
    global board_id
    print("Initting board")
    body = {
        'name': "Stuen"
    }
    result = post(body, init_url)
    board_id = result["board_id"]
    print(board_id)


def recieve_input():
    global get_color_url
    global board_id
    body = {
        'board_id': board_id
    }
    res = urequests.post(get_color_url, json=body)
    if res.status_code == 200:
        result_dict = res.text
        result_dict = json.loads(result_dict)
        color_d = result_dict["color"]
        r,g,b = color_d['red'], color_d['green'], color_d['blue']
        auto_adjust_light = result_dict["auto_adjust_light"]
        set_point = result_dict["setpoint"]
        print(auto_adjust_light)
        print(set_point)
        hex_str = '0x%02x%02x%02x' % (r,g,b)
        hex_int = int(hex_str, 16)
        res.close()
        return hex_int
    res.close()
    return None
"""
def recieve_input():
    global get_color_url
    global board_id
    body = {
        'board_id': board_id
    }
    res = urequests.post(get_color_url, json=body)
    if res.status_code == 200:
        result_dict = res.text
        result_dict = eval(result_dict)
        color_d = result_dict["color"]
        r,g,b = color_d['red'], color_d['green'], color_d['blue']

        auto_adjust_light = result_dict["auto_adjust_light"]
        set_point = result_dict["setpoint"]

        print(auto_adjust_light)
        print(set_point)

        hex_str = '0x%02x%02x%02x' % (r,g,b)
        hex_int = int(hex_str, 16)
        res.close()
        return hex_int
    res.close()
    return None
"""
def main_loop():
    global wlan
    print("Starting main loop")
    while True:
        try: 
            color = recieve_input()
            if color is not None:
                pycom.rgbled(color)
            else:
                print("No color found")
        except Exception as e:
            print(e)
            if not wlan.isconnected():
                print("Lost connection. Attempting to reconnect.")
                connect()
            

def run():
    connect(ssid, wifi_pass)
    init()
    main_loop()
    #_thread.start_new_thread(main_loop, ())
 
run()
