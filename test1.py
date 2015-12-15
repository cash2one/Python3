#! /usr/bin/python

#        Данный код посвящаеться автокликеру.
#        отступы табуляцией
#        by Luca Brasi, e-mail: andruha.sota@mail.ru


import pyautogui, time, pyxhook, threading, argparse


class MouseKeybEvents():
    def __init__(self):
        self.running=True
            
#       Принятие аргументов из командной строки
        parser = argparse.ArgumentParser()
        parser.add_argument('-w', '--write', action='store_true', help='режим записи')
        parser.add_argument('-r', '--read', action='store_true', help='режим чтения')
        args = parser.parse_args()
#       Уже все приняли, дальше пошел процесс создания списка файлов по переданному параметру        
        self.action = {'write':args. write, 'read': args.read}
        
#   Отслеживает положение курсора
    def traceCoursor(self):
        lastPos=pyautogui.position()
        
        while self.mustFinish == False:
            currPos=pyautogui.position()
            time.sleep(0.1)
            if lastPos == currPos and self.keyPressed == False:
                if self.timerLock == False:
                    self.timerStart()
                
            else:
#                import pdb;  pdb.set_trace()
                posTime=round(self.timerStop(),1)
                print(lastPos,posTime)
                #print('Хорошо не застрял на метке 21')
                timerLock=False
                self.resetTimer()
                #print('Хорошо не застрял на метке 22')
                self.event.clear()
                self.event.set()
                #print('Хорошо не застрял на метке 23')
                
                
            lastPos=currPos
    
#   Инициализирует метод OnKeyboardEvent
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
            #print(event.Key, event.Ascii)
            if event.Ascii == 32:
                self.running = False
                self.mustFinish = True
            elif event.Key == 'Control_L':
                try:
                    self.keyPressed=True
                    #print(self.event.is_set())
                    print(self.event.clear())
                    self.event.wait(1.0)
                    #print('Хорошо не застрял на метке 31')
                    print(pyautogui.position(), ' LClick')
                    self.event.clear()
                    self.keyPressed=False
                except Exception:
                    print('Гавно однако!')
                

#   Сей объект класса посвящен таймеру

class Timer(MouseKeybEvents):
    keyPressed=False
    startTime=0
    timerLock=False
    event=threading.Event()
    mustFinish=False
    
#    Ставит базовую точку времени с которой начинается отсчет
    def timerStart(self):
        self.timerLock=True
        self.resetTimer()
        self.keyPressed=False
        
#    Останавливает таймер, возвращает разницу времени в секундах между запуском
#    и остановкой
    def timerStop(self):
        self.timerLock=False
        timePassed=time.time() - self.startTime
        
        return timePassed
    
#    Сбрасывает таймер, выставляя значение таймера на 0
    def resetTimer(self):
        self.startTime=time.time()

class ThreadController(Timer):
    def createThreads(self):
        th1=threading.Thread(target=self.traceCoursor)
        th2=threading.Thread(target=self.catchKeyPress)
        th1.start()
        th2.start()

if __name__ == '__main__':
    a = ThreadController()
    if a.action['write']:
        a.createThreads()
       
            
    



