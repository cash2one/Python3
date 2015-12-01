#! /usr/bin/python

#        Данный код посвящаеться автокликеру.
#        отступы табуляцией
#        by Luca Brasi, e-mail: andruha.sota@mail.ru


import pyautogui, time, pyxhook, threading

class Base():
    startTime=0
    timerLock=False

    def __init__(self):
        self.running=True
        

#   Основная функция
    def main(self):
        lastPos=pyautogui.position()
        
        while True:
            currPos=pyautogui.position()
            time.sleep(0.1)
            if lastPos == currPos:
                if self.timerLock == False:
                    self.timerStart()
            else:
#                import pdb;  pdb.set_trace()
                posTime=round(self.timerStop(),1)
                timerLock=False
                self.resetTimer()
                
                print(lastPos,posTime)
                
            lastPos=currPos
    
    
    def catchKeyPress(self):
            hm = pyxhook.HookManager()
            hm.KeyDown = self.OnKeyboardEvent
            hm.HookKeyboard()
            hm.start()
            while self.running:
                time.sleep(0.1)
            hm.cancel()
            
#    Метод опрелеябщий события нажатия кнопок клавиатуры
    def OnKeyboardEvent(self,event):
            print(event.Key, event.Ascii)
            if event.Ascii == 32:
                self.running = False
            elif event.Key == 'Control_L':
                print(pyautogui.position(), ' LClick')
                

#   Сей объект класса посвящен таймеру

class Timer(Base):
    
#    Ставит базовую точку времени с которой начинается отсчет
    def timerStart(self):
        self.timerLock=True
        self.resetTimer()
        
#    Останавливает таймер, возвращает разницу времени в секундах между запуском
#    и остановкой
    def timerStop(self):
        self.timerLock=False
        timePassed=time.time() - self.startTime
        
        return timePassed
    
#    Сбрасывает таймер, выставляя значение таймера на 0
    def resetTimer(self):
        self.startTime=time.time()




if __name__ == '__main__':
    a = Timer()
    a.catchKeyPress()
    



