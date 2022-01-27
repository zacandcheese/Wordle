import pyautogui
import ctypes
import time

def DetectClick(button, watchtime = 5):
    '''Waits watchtime seconds. Returns True on click, False otherwise'''
    if button in (1, '1', 'l', 'L', 'left', 'Left', 'LEFT'):
        bnum = 0x01
    elif button in (2, '2', 'r', 'R', 'right', 'Right', 'RIGHT'):
        bnum = 0x02

    start = time.time()
    while 1:
        if ctypes.windll.user32.GetKeyState(bnum) not in [0, 1]:
            # ^ this returns either 0 or 1 when button is not being held down
            return True
        elif time.time() - start >= watchtime:
            break
        time.sleep(0.001)
    return False

print(DetectClick('Right'))
