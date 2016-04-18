#!/usr/bin/python3
# -*- coding: utf-8 -*-

#        отступы табуляцией
#        by Andrew Sotnikov aka Luca Brasi,
#        e-mail: andruha.sota@mail.ru
#        --------------
import os,saulog, time, shutil, sys
from subprocess import call
user=''
passwd=''
domain=''

gmessage='Файлы с FTP скачаны успешно'
bmessage='Не удалось скачать файлы с FTP'

print(sys.getdefaultencoding())

file='/var/log/andrew/progreso_backup.log'

dest='/media/Maindata/Дело/progreso/{0}_progreso.tar.bz2'.format(
        time.strftime('%d.%m.%Y'))

os.chdir('/tmp/')
request='wget -c -q -t 10 -r -l 10 --retry-connrefused ftp://{0}:{1}@{2}'.format(
         user, passwd, domain)

wget=call(request, shell=True)

if wget == 0:
    log=saulog.WriteLog(file,gmessage)
    print('Все скачано!')

else:
    log=saulog.WriteLog(file,bmessage)

os.chdir('/tmp/{0}/domains/'.format(domain))
cr_ar=call("tar -C {0} -cvj -f {1} {2} {3} ".format(
'/tmp/ftp.progreso.com.ua/domains/', dest, 'progreso.com.ua', 'localhost.sql'),
shell=True)

if cr_ar == 0:
    saulog.WriteLog(file,'Архив создан!')

shutil.rmtree('/tmp/ftp.progreso.com.ua/')
