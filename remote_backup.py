#!/usr/bin/python3

#        отступы табуляцией
#        by Andrew Sotnikov aka Luca Brasi,
#        e-mail: andruha.sota@mail.ru
#        --------------
import os,saulog, time, shutil
from subprocess import call
user=''
passwd=''
domain=''

gmessage='Файлы успешно скачаны'
bmessage='Не удалось скачать файлы'
file='/var/log/andrew/progreso_backup.log'

dest='/media/Maindata/Дело/progreso/{0}_progreso.tar.bz2'.format(
        time.strftime('%d.%m.%Y'))

os.chdir('/tmp/')
request='wget -c -t 10 -r -l 10 --retry-connrefused ftp://{0}:{1}@{2}'.format(
         user, passwd, domain)

wget=call(request, shell=True)

if wget == 0:
    log=saulog.WriteLog(file,gmessage)
    print('Все скачано!')

else:
    log=saulog.WriteLog(file,bmessage)

os.chdir('/tmp/{0}/domains/'.format(domain))
cr_ar=call("tar -C {0} -cvj -f {1} {2} ".format('/tmp/ftp.progreso.com.ua/domains/',
                                      dest, 'progreso.com.ua'), shell=True)

if cr_ar == 0:
    saulog.WriteLog(file,'Архив записан!')

shutil.rmtree('/tmp/ftp.progreso.com.ua/')

