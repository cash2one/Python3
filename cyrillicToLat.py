#!/usr/bin/env python
#coding=utf8

import sys
import subprocess


#Создадим ка мы list_of_files
subprocess.call("cd "+sys.argv[1]+"; ls -1 > "+sys.argv[1]+"/list_of_files.txt",shell=True)



#Функция которая преобразаует полученную строку в латынь, посредством транслитерации.
#-------------------------------------

def cyrillicTranslit(word):

    #Русский алфаваит в верхнем и нихнем регистре
    rus_alphabet =  ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и','й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ч', 'ц', 'ш', 'щ', 'ь', 'ы', 'ъ','э', 'ю', 'я','А','Б','В','Г','Д','Е','Ё','Ж','З','И','Й','К','Л','М','Н','О','П','Р','С','Т','У','Ф','Х', 'Ч','Ц','Ш','Щ','Ь','Ы','Ъ','Э','Ю','Я',' ','(',')', 'nichego']

    #Транслит соотвертсвующий массиву с  русским алфавитом
    trans_alphabet = ['a', 'b', 'v', 'g', 'd', 'e', 'yo', 'zh', 'z', 'i', 'y', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'f', 'h', 'ch','ts', 'sh', 'shch', '\'', 'y', '\'', 'e', 'yu', 'ja','A','B','V','G','D','E','Yo','Zh','Z','I','Y','K','L','M','N','O','P','R','S','T','U','F','H','Ch', 'Ts','Sh','Shch','\'','Y','\'','E','Yu','Ja', '_', '!','!', 'nichego']

    new_word=''
    i=0
    for symb in word:
        prev_res= False
        j=0
        for source in rus_alphabet:
            if source == symb:
                new_word=new_word.strip() + trans_alphabet[j]
                prev_res= True
            elif (j+1) == 70 and prev_res != True :
                new_word=new_word+symb
            j=j+1
        i=i+1

    return new_word

#Функция транслитерации закончилась
#-------------------------------------


#Расчитано на то, что в качестве передаваемого параметра будет $PWD
#Открываем файл источник
cyr_ls = open(sys.argv[1]+'/list_of_files.txt')

#Открываем файл на запись
lat_ls = open (sys.argv[1]+'/list_of_filesLAT.txt','w')

#Пишем в новый файл конвертнутые строки с источника
for line in cyr_ls:
    lat_ls.write((cyrillicTranslit(line)))

#Закрываем оба файла
cyr_ls.close()
lat_ls.close()

    
