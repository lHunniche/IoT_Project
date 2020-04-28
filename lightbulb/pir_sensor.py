import time
from network import WLAN
from machine import Pin

wl = WLAN(WLAN.STA)

hold_time_sec = 10
last_trigger = -10
present = False

pir = Pin('G4',mode=Pin.IN, pull=Pin.PULL_UP)


def init_pir():
    global last_trigger
    global hold_time_sec
    global present
    print("Starting PIR loop")
    while True:
        if pir() == 1:
            if time.time() - last_trigger > hold_time_sec:
                last_trigger = time.time()
                print("Presence detected")
                present = True
        else:
            last_trigger = 0
            print("No presence")
            present = False

        time.sleep_ms(500)

    print("Exited main loop")

def pir_presence():
    global present
    return present
