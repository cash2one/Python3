#!/usr/bin/env python
#coding=utf8

import sys
import subprocess



#Функция зкранирования пробелов
#-------------------------------------
def ekran_spaces(string):
    replaced_s=string.replace(' ','\ ')
    replaced_s=replaced_s.replace('  ','\ ')
    replaced_s=replaced_s.replace('   ','\ ')
    replaced_s=replaced_s.replace(')','\)')
    replaced_s=replaced_s.replace('(','\(')

    return replaced_s

#Функция экранирования пробелов закончилась
#-------------------------------------


#Расчитано на то, что в качестве передаваемого параметра будет $PWD
#Открываем файл источник
cyr_ls = open(sys.argv[1]+'/list_of_files.txt')
#Открываем файл на запись without spaces
withoutSP_ls = open (sys.argv[1]+'/list_of_filesWSP.txt','w')


#Пишем в новый файл экранирования строки из источника
for line in cyr_ls:
    withoutSP_ls.write((ekran_spaces(line)))

#Закрываем оба файла
cyr_ls.close()
withoutSP_ls.close()


#Открываем файл источник
withoutSP_ls = open(sys.argv[1]+'/list_of_filesWSP.txt')
#Открываем файл на запись without spaces
LAT_ls = open (sys.argv[1]+'/list_of_filesLAT.txt')
strinout = LAT_ls.readlines()
i=0
for name in withoutSP_ls.readlines():
#     subprocess.call("file "+sys.argv[1]+name.replace('\n',''), shell=True)
#     subprocess.call("file "+sys.argv[1]+ strinout[i].replace('\n',''), shell=True)
     subprocess.call("mv "+sys.argv[1]+"/"+name.replace('\n','')+" "+sys.argv[1]+"/"+strinout[i].replace('\n',''), shell=True)
#    print(name,strinout[i])
     i=i+1

