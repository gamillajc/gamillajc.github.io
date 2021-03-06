# Created by Janssen Gamilla on 1/1/2021
import time
import board
import neopixel
from digitalio import DigitalInOut
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

def handleColors(cur_index, pixels):
    """Changes the neopixel LED on the board to reflect which profile is currently active"""
    if cur_index == 1:
        pixels.fill((255, 20 , 0))  # red = profile 1
    elif cur_index == 2:
        pixels.fill((0, 255, 0))  # green = profile 2
    elif cur_index == 3:
        pixels.fill((0, 0, 255))  # blue = profile 3

def handleButtons(cur_index, macro, b_2, b_3, b_4, b_5, k, kl):
    """Outputs desired character or string depending on the cur_index and button pressed"""
    if not b_2.value:
        decideOutput(macro, cur_index, 0, k, kl)
        time.sleep(0.3)
    if not b_3.value:
        decideOutput(macro, cur_index, 1, k, kl)
        time.sleep(0.3)
    if not b_4.value:
        decideOutput(macro, cur_index, 2, k, kl)
        time.sleep(0.3)
    if not b_5.value:
        decideOutput(macro, cur_index, 3, k, kl)
        time.sleep(0.3)

def profileChange(but_1):
    """Increments the cur_index and resets to profile 1 if cur_index > 3"""
    if not but_1.value:
        global cur_index
        cur_index = cur_index + 1
        time.sleep(0.3)
        if cur_index > 3:
            cur_index = 1
        print("Current profile: %d" % (cur_index))

def decideOutput(macro, cur_index, NumButton, k, kl):
    """Decides whether a string/character or Keycode will be outputted"""
    if type((macro[cur_index-1][NumButton])) is str:
        kl.write(macro[cur_index-1][NumButton])
    else:
        k.send(macro[cur_index-1][NumButton])
    
if __name__ == "__main__":
    # assign buttons to pins
    b_1 = DigitalInOut(board.D5)
    b_2 = DigitalInOut(board.D6)
    b_3 = DigitalInOut(board.D9)
    b_4 = DigitalInOut(board.D11)
    b_5 = DigitalInOut(board.D12)
    k = Keyboard(usb_hid.devices)
    kl = KeyboardLayoutUS(k)
    pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.1)
    # customize macros below
    # max of 4 elements per macro index
    macro = [[Keycode.UP_ARROW, Keycode.DOWN_ARROW , Keycode.LEFT_ARROW, Keycode.RIGHT_ARROW], ["hello", "world", "!", Keycode.SPACE], ["You can output long strings like this ", "or just a character ", "a", "b"]]
    cur_index = 1
    print("Current profile: %d" % (cur_index))
    while True:
        handleColors(cur_index, pixels)
        profileChange(b_1)
        handleButtons(cur_index, macro, b_2, b_3, b_4, b_5, k, kl)