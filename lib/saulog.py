#! /usr/bin/python3
# -*- coding: utf-8 -*-

#        отступы табуляцией
#        by Andrew Sotnikov aka Luca Brasi,
#        e-mail: andruha.sota@mail.ru
#        --------------

import time

# Открывет файл и пишет туда лог
class WriteLog:

    def __init__(self,log_file,text):

    #   Текст сообщения который будет записан в лог
        message=(time.strftime("%d-%m-%Y %H:%M:%S    {0}\n")).format(text)
        f=open(log_file, 'a')
        f.write(message)
        print('Лог записан!')
        f.close()
        self.logfile = log_file
        
        
#    проверяет насколько файл лога являеться старым. Если он создан не сегодня
#    то он удляеться
    
    def getRidOfOldLog(self):

        # проверить старый ли файл лога. Если старый то молча удаляем
        f_time = os.path.getmtime(self.logfile)
        fcreated_day = time.localtime(f_time).tm_mday
        cur_day = time.localtime(time.time()).tm_mday

        if fcreated_day != cur_day:
            os.remove(self.logfile)
            f = open(self.logfile,'w')
            f.write('{0:#<120}\n{1:#^120}\n{2:#<120}\n\n\n'.format('',
            time.strftime('           %A           '),''))
            f.close()

if __name__ == "__main__":
    pass
