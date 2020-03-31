from network import WLAN
import machine
from machine import Pin
import urequests
import time
from pysense import Pysense
import pycom


ssid = 'Xrosby-Wifi'
wifi_pass = 'boguspass'
get_color_url = "http://klevang.dk:19409/getcolor"
init_url = "http://klevang.dk:19409/init"
board_id = ""


pycom.heartbeat(False)

def connect(ssid, passw):
    wlan = WLAN(mode=WLAN.STA)
    if not wlan.isconnected():
        nets = wlan.scan()
        for net in nets:
            print(net.ssid)
            if net.ssid == ssid:
                print(ssid, ' found!')
                wlan.connect(net.ssid, auth=(net.sec, passw), timeout=5000)
                while not wlan.isconnected():
                    machine.idle() # save power while waiting
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
        color_d = res.text
        color_d = eval(color_d)
        r,g,b = color_d['red'], color_d['green'], color_d['blue']
        hex_str = '0x%02x%02x%02x' % (r,g,b)
        hex_int = int(hex_str, 16)
        return hex_int
    return None



def run():
    connect(ssid, wifi_pass)
    init()
    while True:
        color = recieve_input()
        if color is not None:
            pycom.rgbled(color)


while True:   
    try:
        run()
    except Exception as e:
        time.sleep(2)
        pass
