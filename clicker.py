import time
import threading
import keyboard
import mouse

r = True
f = False

def r_():
    global r
    r = not r
    exit()

def f_():
    global f
    f = not f



def start():
    while r:
        while f:
            mouse.click("left")
            time.sleep(1.5)
        time.sleep(0.5)

keyboard.add_hotkey("1", r_)
keyboard.add_hotkey("2", f_)

threading.Thread(target=start).start()