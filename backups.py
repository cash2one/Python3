#!/usr/bin/env python
#coding=utf8
#Этот скрипт умело делает бэкапы файлов

##На одном файловом уровне со скриптом нужно сделать файл .inner_data
#Формат файла следующий, имя адрес_элемента путь_кудаложить. Например:
#"gedit /usr/bin/gedit ~/backup/"  Будет gedit будет положен в паку backup и сохранен под именем gedit
#Также это дело пишеться в лог my_log

import time
import subprocess

#Адрес куда хотелось бы писать лог
log="/var/log/andrew/my_backup.log"

f=open('/home/andrew/bin/.inner_data')
for string in f.readlines():
    spl_str=string.split(' ')
#   Имя зип файла
    zipname=spl_str[0]+time.strftime("__%d_%m_%Y") +".zip "
#   Путь к источнику
    path_source = spl_str[1]
#   Путь куда переместить
    path_afterMove = spl_str[2]
    subprocess.call("zip -9 -r -j "+ zipname + " " + path_source, shell=True)
    res=subprocess.call("mv "+zipname+" "+path_afterMove ,shell=True)
    if res == 0:
        subprocess.call("echo "+ time.strftime("%d-%m-%Y %H:%M:%S")+ "    Была сделана резервная копия файла___"+path_source+" >> "+log, shell=True)        

f.close()    




