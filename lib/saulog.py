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

if __name__ == "__main__":
    pass
