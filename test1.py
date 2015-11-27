#! /usr/bin/python

#        Данный код посвящаеться автокликеру.
#        отступы табуляцией
#        by Luca Brasi, e-mail: andruha.sota@mail.ru


import pyautogui, time

class Base():
    startTime=0
    timerLock=False
    
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

class Timer(Base):
    
    def timerStart(self):
        
        self.timerLock=True
        self.resetTimer()
    
    def timerStop(self):
        self.timerLock=False
        timePassed=time.time() - self.startTime
        
        return timePassed
    
    def resetTimer(self):
        self.startTime=time.time()

if __name__ == '__main__':
    a = Timer()
    a.main()
    



