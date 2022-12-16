# importing time and threading
import time
import threading
from pynput.mouse import Button, Controller

# pynput.keyboard is used to watch events of
# keyboard for start and stop of auto-clicker
from pynput.keyboard import Listener, KeyCode


# four variables are created to
# control the auto-clicker
delay = 15
button = Button.left
start_stop_key = KeyCode(char='a')
stop_key = KeyCode(char='b')

# threading.Thread is used
# to control clicks
class ClickMouse(threading.Thread):
    button_loc=(0,0)

    
# delay and button is passed in class
# to check execution of auto-clicker
    def __init__(self, delay, button):
        super(ClickMouse, self).__init__()
        self.delay = delay
        self.button = button
        self.running = False
        self.program_running = True

    def start_clicking(self):
        self.running = True

    def stop_clicking(self):
        self.running = False

    def exit(self):
        self.stop_clicking()
        self.program_running = False

    # find "slowdownload on screen"
    def take_screenshot(self,file_name):
        import pyautogui
        import os
        if os.path.isfile(file_name):
            os.remove(file_name)
        screen_shot = pyautogui.screenshot()
        screen_shot.save(file_name)

    def move_mouse(self,x,y):
        import pyautogui
        pyautogui.moveTo(x,y)

    def get_slow_download_button(self):
        import cv2
        import numpy as np

        print('finding button...',end='\r')
        screenshot_name='screenshot.png'
        self.take_screenshot(screenshot_name)
        screenshot = cv2.imread(screenshot_name,0)
        template = cv2.imread('slow_download.png',0)
        result = cv2.matchTemplate(screenshot,template, cv2.TM_SQDIFF_NORMED)
        cv2.normalize( result, result, 0, 1, cv2.NORM_MINMAX, -1 )
        _, _, min_loc, _ = cv2.minMaxLoc(result,None)
            
        if min_loc is not None: 
            print('Done...                                                                                                   ',end='\r')
        if min_loc[0] != self.button_loc[0] or min_loc[1] != self.button_loc[1]:
            print(f"Button moved to {min_loc}")
            self.button_loc = min_loc
        return min_loc
        

    # method to check and run loop until
    # it is true another loop will check
    # if it is set to true or not,
    # for mouse click it set to button
    # and delay.
    def run(self):
        while self.program_running:
            while self.running:
                x,y = self.get_slow_download_button()
                self.move_mouse(x+15,y+10)
                mouse.click(self.button)
                i=0
                while i<self.delay:
                    time.sleep(1)
                    print(f'{i}...',end="",flush=True)
                    i+=1
            time.sleep(0.1)


# instance of mouse controller is created
mouse = Controller()
click_thread = ClickMouse(delay, button)
click_thread.start()


# on_press method takes
# key as argument
def on_press(key):
    
# start_stop_key will stop clicking
# if running flag is set to true
    if key == start_stop_key:
        if click_thread.running:
            click_thread.stop_clicking()
        else:
            click_thread.start_clicking()
            
    # here exit method is called and when
    # key is pressed it terminates auto clicker
    elif key == stop_key:
        click_thread.exit()
        listener.stop()


with Listener(on_press=on_press) as listener:
    listener.join()
