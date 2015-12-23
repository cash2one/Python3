#! /usr/bin/python

#        Данный код посвящаеться автокликеру.
#        отступы табуляцией
#        by Luca Brasi, e-mail: andruha.sota@mail.ru


import pyautogui, time, pyxhook, threading, argparse
import re

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
        
#   Отслеживает положение курсора. Начинает поток th1.
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
                
                self.writeToFile(str(lastPos)+' '+str(posTime)+' NC')
                timerLock=False
                self.resetTimer()
                self.clearTh()
                self.setTh()
                self.waitTh()
                
            lastPos=currPos
        global f
        f.close();print('Файл успешно закрыт')
        
#   Инициализирует метод OnKeyboardEvent. Начинает поток th2.
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
                self.keyPressed=True
                self.clearTh()
                print(self.resumeTh)
                self.waitTh()
                
                self.writeToFile(str(pyautogui.position())+'0.1 LC')
                self.clearTh()
                self.keyPressed=False


#   Сей объект класса посвящен таймеру
class Timer(MouseKeybEvents):
    keyPressed=False
    startTime=0
    timerLock=False
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

#Имитация стандартного класса событий, Threading.Events()       
class Locker(MouseKeybEvents):
    delayTh=0.07
    resumeTh=False
    #Заставляет текщий поток ждать пока не появиться флаг о продолжении
    def waitTh(self):
        while True:
            if self.resumeTh==False:
                time.sleep(self.delayTh)
            else:
                break
    #Поднимает флаг, поток возобновляет работу
    def setTh(self):
        self.resumeTh=True
    #Сбрасывает флаг
    def clearTh(self):
        self.resumeTh=False
           
class FileActions():
    strRecLimit=50 #Предел количества значений в одной строке
    strCounter = strRecLimit
    #Получает строку формата "x,y,время,кнопка мыши", парсит ее на составляющие.
    #Затем пишет в файл. По достижению strRecLimit каретка перескакивает на новую строку.
    def writeToFile(self,string):
        print (string)
        global f
        p = re.findall(r"(\w+\.+\w)|(\w+(?=,))|(\w+(?=\)))|(\w{2})",string)
        #x-кордината, y-кордината, время простоя курсора, кнопка мыши, соответственно
        x=(''.join(p[0])).strip();y=(''.join(p[1])).strip();time=(''.join(p[2])).strip();act=(''.join(p[3])).strip()
        print (x+','+y+','+time+','+act+'\n')
        if self.strCounter >0: 
            f.write(x+','+y+','+time+','+act+';')
            self.strCounter=self.strCounter-1
        else:
            f.write(x+','+y+','+time+','+act+';\n')
            self.strCounter=self.strRecLimit
            
        

class ThreadController(Timer,Locker,FileActions):
    def createThreads(self):
        global f
        f = open('cache.txt','w')
        th1=threading.Thread(target=self.traceCoursor)
        th2=threading.Thread(target=self.catchKeyPress)
        th1.start()
        th2.start()
        


if __name__ == '__main__':
    a = ThreadController()
    if a.action['write']:
        a.createThreads()

       