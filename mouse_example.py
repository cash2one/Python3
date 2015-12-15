#! /usr/bin/python

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import pyautogui, sys
__author__ = "andrew"
__date__ = "$18.11.2015 21:11:11$"

if __name__ == "__main__":
    
#    pyautogui.moveTo((1311, 76))
#    pyautogui.click(x=1311, y=76, button='left')
#    pyautogui.typewrite('Hello world!', interval=0.5)
    print('Press Ctrl-C to quit.')
    try:
        while True:
            x, y = pyautogui.position()
            positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
            print(positionStr, end='\n')
#            print('\b' * len(positionStr), end='', flush=True)
    except KeyboardInterrupt:
        print('\n')