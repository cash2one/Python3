#!/usr/bin/env python
#coding=utf8
#        Получает абсолютный путь к директории и переимновывает в ней файлы, 
#        вырезая из имени файла заданный кусок.
         
#        отступы табуляцией
#        by Luca Brasi, e-mail: andruha.sota@mail.ru
#        --------------



import os
import argparse, re

class FileActions():

    def __init__(self):
        #Принятие аргументов из командной строки
        parser = argparse.ArgumentParser()
        parser.add_argument('--path', help='следует указать абсолютный путь к желаемому каталогу, с котрым нужно произвести действия ')
        parser.add_argument('-f','--fpoint', help='Начальная точка обрезки')
        parser.add_argument('-s','--spoint', help='Конечная точка обрезки')
        args = parser.parse_args()
#       Уже все приняли, дальше пошел процесс создания списка файлов по переданному параметру        
        self.path = args.path
        self.fpoint=args.fpoint
        self.spoint=args.spoint
    
#    Принимает строку. Вырезает из не участки начинающиеся с fpoint 
#    и заканчивающиеся spoint. Возвращает обрезанную строку
    def strCutter(self,elem):
        cut_part=re.findall(r"(?<="+self.fpoint+").+?(?="+self.spoint+")", elem);cut_part=cut_part[0]
        cut_elem=elem.replace(cut_part,'')
        print('- - - - - -- - - - - -- - - - - -- - - - - -')
        print(elem)
        print(cut_elem)
        return cut_elem
    
    def getTut(self,elem):
        cut_part=re.findall(r"tutorial_\d{1,2}", elem);
        print('- - - - - -- - - - - -- - - - - -- - - - - -')
        try:
            cut_part=cut_part[0]
        except IndexError:
            print('Ну не вышло!')
#        print(cut_part)
        return cut_part
        
if __name__ == "__main__":
    p=FileActions()
    ls=os.listdir(p.path)
    for elem in ls:
        p.strCutter(elem)





    
