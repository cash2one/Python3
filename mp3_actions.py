#! /usr/bin/python3

#        отступы пробелами
#        by Andrew Sotnikov aka Luca Brasi,
#        e-mail: andrew.sotnikov@zoho.com
#        --------------
#        Переименовывает треки в соответствии с заданными параметрами
#        для успешной работы нужно поставить:

#              sudo apt-get install python3-taglib

import os, taglib, argparse

#        ПОЛУЧАЕМ АРГУМЕНТЫ ИЗ КОМАНДНОЙ СТРОКИ
# Принятие аргументов из командной строки
parser = argparse.ArgumentParser()
parser.add_argument('--path', help='this is absolute path to directory'
' where should make changes')
parser.add_argument('--artist', help='in every songs artist tag will'
' changed to that')
parser.add_argument('--album', help='in every song album tag will '
'changed like that')
parser.add_argument('--rename-file', help='rename file according to format like'
                                          ' show below: ARTIST_SONG', nargs='?',
                    const=True)
args = parser.parse_args()
#       Уже все приняли, дальше пошел процесс создания списка файлов по переданному параметру

# print(args)
walk = os.walk(args.path)
for root, dir, fnames in walk:
    for fname in fnames:
        song= taglib.File(root+'/'+fname)
        print(song.tags)











