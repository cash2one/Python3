#! /usr/bin/python

#        отступы табуляцией
#        by Andrew Sotniokv aka Luca Brasi, 
#        e-mail: andruha.sota@mail.ru
#        --------------
    
#    Внешний стартер. Хорош тем что запускает приложения которые имеют X Window.
    

import subprocess, time

class Launch():
#    Интервал в секундах между запсуками приложения
    run_interval=3600
#    Интервал между проверкой для наступления времени инициализации 
#    запускаемого скрипта, который указываеться в списке tasks
    check_interval=600
    start=18
    end=24
    
#   Возвращает значение текущего времени. Нужно передать аргументы формата
#   hm, h, m
    def getTime(self,format):
        if format == 'hm':
            t=time.strftime("%H:%M")
            print(t)
            return int(t)
        elif format == 'h':
            t=time.strftime("%H")
            print(t)
            return int(t)
        elif format == 'm':
            t=time.strftime("%M")
            print(t)
            return int(t)


if __name__ == "__main__":
    time.sleep(240)    
#   Пути указывать в абсолюном формате
    tasks=['/home/andrew/bin/play_eng.py']
    lanch=Launch()
    t=lanch.getTime('h')
    while t <= lanch.end:
        if t < lanch.start:
            print('Еще не вечер...')
            time.sleep(lanch.check_interval)
            continue
        subprocess.call('python3 '+tasks[0], shell=True)
        time.sleep(lanch.run_interval)
