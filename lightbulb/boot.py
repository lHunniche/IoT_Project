from network import WLAN
import machine
from machine import Pin
import urequests
import time
from pysense import Pysense
import pycom
import _thread
import json
from LTR329ALS01 import LTR329ALS01


ssid = 'Xrosby-Wifi'
wifi_pass = 'boguspass'
get_color_url = "http://klevang.dk:19409/getupdates"
init_url = "http://klevang.dk:19409/init"
board_id = ""
wlan = WLAN(mode=WLAN.STA)
OFF = 0x000000
auto_adjust = False
setpoint = 500
py = Pysense()
lt = LTR329ALS01(py)

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


def send_light_level_for_auto_adjust():
    global auto_adjust
    global setpoint
    while auto_adjust:
        post_light_measure()
        time.sleep(10)

def post_light_measure():
    global board_id
    measured_light = lt.light()[0]
    post({
        'measured_light': measured_light,
        'board_id': board_id 
    }, "http://klevang.dk:19409/autolightupdate")


def recieve_input():
    global get_color_url
    global board_id
    global auto_adjust
    global setpoint
    light = lt.light()[0]
    body = {
        'board_id': board_id,
        'lux_in_room': light
    }
    res = urequests.post(get_color_url, json=body)
    print(res.status_code)
    if res.status_code == 200:
        result_dict = res.text
        result_dict = json.loads(result_dict)
        color_d = result_dict["color"]
        r,g,b = color_d['red'], color_d['green'], color_d['blue']
        auto_adjust_light_requested = result_dict["auto_adjust_light"]
        setpoint = result_dict["setpoint"]
        handle_auto_adjust(auto_adjust_light_requested)
        hex_str = '0x%02x%02x%02x' % (r,g,b)
        hex_int = int(hex_str, 16)
        res.close()
        return hex_int
    res.close()
    if res.status_code == 204:
        print("No updates found")
    return None

def handle_auto_adjust(auto_adjust_light_requested):
    global auto_adjust
    if auto_adjust_light_requested and not auto_adjust:
            auto_adjust = True
            init_auto_adjust()
    elif not auto_adjust_light_requested and auto_adjust:
        auto_adjust = False

def main_loop():
    global wlan
    print("Starting main loop")
    while True:
        try: 
            color = recieve_input()
            if color is not None:
                pycom.rgbled(color)
            else:
                print("No new color found")
        except Exception as e:
            print(e)
            if not wlan.isconnected():
                print("Lost connection. Attempting to reconnect.")
                connect()
            
def init_auto_adjust():
    _thread.start_new_thread(send_light_level_for_auto_adjust, ())



def run():
    connect(ssid, wifi_pass)
    init()
    main_loop()
 
run()
