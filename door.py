import firebase_admin
import time
import threading
import RPi.GPIO as gpio

from enum import Enum
from firebase_admin import firestore
from firebase_admin import credentials

class Led:
    def __init__(self, pin):
        self.pin = pin
        gpio.setup(self.pin, gpio.OUT)
        gpio.output(self.pin, gpio.LOW)
    def set(self, state):
        gpio.output(self.pin, gpio.HIGH if state else gpio.LOW)
    def blink(self, hz):
        self.set(int(time.time() * hz) % 2 == 0)

class Door:
    def __init__(self, pin_open, pin_close):
        self.is_open = False
        self.pin_open = pin_open
        self.pin_close = pin_close
        gpio.setup(self.pin_open, gpio.OUT)
        gpio.setup(self.pin_close, gpio.OUT)
        gpio.output(self.pin_open, gpio.LOW)
        gpio.output(self.pin_close, gpio.LOW)

    def set_pin_for(self, pin_to_set, t_s):
        print(f' Wrote pin {pin_to_set} = HIGH.')
        gpio.output(pin_to_set, gpio.HIGH)
        time.sleep(t_s)
        print(f' Wrote pin {pin_to_set} = LOW.')
        gpio.output(pin_to_set, gpio.LOW)

    def open_pls(self):
        print('Opening door...')
        self.set_pin_for(self.pin_open, 5)
        self.is_open = True

    def close_pls(self):
        print('Closing door...')
        self.set_pin_for(self.pin_close, 5)
        self.is_open = False

class Net:
    def __init__(self, db):
        self.doc_ref = db.collection('req').document('req')
        self.doc_ref.on_snapshot(self.on_snapshot)
        self.last_ts = -1

    def on_snapshot(self, doc_snapshot, changes, read_time):
        for doc in doc_snapshot:
            if doc.id != "req": continue
            if self.last_ts == -1: #ignore the first time
                self.last_ts = 0
            else:
                self.last_ts = time.time()
                print(f'Open request recived at timestamp {self.last_ts}.')

if __name__ == '__main__':
    print('Initializing...')

    gpio.setmode(gpio.BCM)

    status = Led(16)
    status.set(True)

    state = Led(19)
    state.set(True)

    cred = credentials.Certificate("/home/door/door/auth.json")
    app = firebase_admin.initialize_app(cred)
    db = firestore.client()

    door = Door(23, 22)
    net = Net(db)
    
    time.sleep(5)
    print(' done.')

    state.set(False)

    while True:
        status.blink(5)

        pls_open = (time.time() - net.last_ts) < 15

        if door.is_open:
            state.blink(5)
            
        if pls_open and not door.is_open:
            state.set(True)
            door.open_pls()
            state.set(False)
        if not pls_open and door.is_open:
            state.set(True)
            door.close_pls()
            state.set(False)

        time.sleep(0.05)
