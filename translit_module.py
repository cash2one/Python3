#!/usr/bin/env python
#coding=utf8

import sys
import subprocess
import argparse
import os


#Этот модуль планируется посвятить транслитерации

# TranslitBasic это базовый класс
class TranslitBasic(object):

    #Русский алфаваит в верхнем и нихнем регистре
    _rusAlphabet =  ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и','й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ч', 'ц', 'ш', 'щ', 'ь', 'ы', 'ъ','э', 'ю', 'я','А','Б','В','Г','Д','Е','Ё','Ж','З','И','Й','К','Л','М','Н','О','П','Р','С','Т','У','Ф','Х', 'Ч','Ц','Ш','Щ','Ь','Ы','Ъ','Э','Ю','Я',' ','(',')', 'nichego']
    #Транслит соотвертсвующий массиву с  русским алфавитом
    _transAlphabet = ['a', 'b', 'v', 'g', 'd', 'e', 'yo', 'zh', 'z', 'i', 'y', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'f', 'h', 'ch','ts', 'sh', 'shch', '\'', 'y', '\'', 'e', 'yu', 'ja','A','B','V','G','D','E','Yo','Zh','Z','I','Y','K','L','M','N','O','P','R','S','T','U','F','H','Ch', 'Ts','Sh','Shch','\'','Y','\'','E','Yu','Ja', '_', '!','!', 'nichego']

    #Сyrillic translit - BEGIN
    #Метод который преобразаует полученную строку в латынь, посредством транслитерации.
    def cyrillicTranslit(self,word):
        new_word=''
        i=0
        for symb in word:
            prev_res= False
            j=0
            for source in self._rusAlphabet:
                if source == symb:
                    new_word=new_word.strip() + self._transAlphabet[j]
                    prev_res= True
                elif (j+1) == 70 and prev_res != True :
                    new_word=new_word+symb
                j=j+1
            i=i+1

        return new_word

    #Сyrillic translit - END
     
# FileActions это подкласс сочетающий в себе функции работы над файлами.
class FileActions(TranslitBasic):

    def __init__(self):
#        Принятие аргументов из командной строки
        parser = argparse.ArgumentParser()
        parser.add_argument('--path', help='следует указать абсолютный путь к желаемому каталогу, с котрым нужно произвести действия ')
        args = parser.parse_args()
#       Уже все приняли, дальше пошел процесс создания списка файлов по переданному параметру        
        self.path = args.path

       

class Rename(FileActions):
    def __init__(self):
        super().__init__()
    #Метод транслитерирует имена файло рекурсивно, вдоль всего каталога    
    def renameFile(self):
        for iteration in os.walk(self.path): #Главый цикл, итерирует по глубине каталогов, постепенно опускаясь вниз
            dirName = iteration[0] # Первый кортеж с отображенем пути текущей папки
            if dirName[(len(dirName))-1] != '/': # Если конец пути папки без слеша, то добавим его
                dirName =  dirName + '/'
            files = iteration[2] # Третий кортеж со списком файлов внутри папки dirName
            for file in files:
                new_name=self.cyrillicTranslit(file)
                os.rename((dirName+file),(dirName+new_name))
    
    #Получает строку с абсолютным путём папки. Вырзает слеши в конце, если таковые имеются
    #Возвращает массив из двух элементов, вместе равняющихся абсолютному пути к папке
    #Второй элемент это имя самой папки, первый - остаток строки абсолютного пути.
    
    def getFolderName(self,dirName):
        length = len(dirName)
        if dirName[(length-1)] == '/': # Если конец пути папки без слеша, урежем его к едрени фени
            dirName =  dirName[0:(length-2)] 
        #Да найдем же последний слеш в строке!
        i=len(dirName) # У нас ведь могла перезаписаться длина dirName, так что проверим длину
        while True:
            i=i-1
            if dirName[i] == '/':
                break 
            
        print(dirName[(i+1):])
        return (dirName[:i+1],dirName[(i+1):])
            
    #Исполнительный метод, переименовывает папку и сразу возврщается на верхний уровень деерева каталогов.
    #По чуть-чуть переименовывает папки, каждый раз начиная сначала. Если папку переименовывать не надо - идет дальше, 
    #постепенно достигая конца файлового дерева. Если он достиг конца, то возвращает True
    def renameFolderExec(self):
        start_again = False
        for iteration in os.walk(self.path): #Главый цикл, итерирует по глубине каталогов, постепенно опускаясь вниз
            dirPath = iteration[0] # Первый кортеж с отображенем пути текущей папки
            print(dirPath)
            dirName=self.getFolderName(dirPath)
            tr_dirName=self.cyrillicTranslit(dirName[1])
            if tr_dirName != dirName[1]:
                os.rename(dirPath,(dirName[0]+tr_dirName))
                start_again = True
                break
        return start_again
    #Метод инициирующий цикл. До тех пор пока не достигнем конца файлового дерева, т.е. Переименовывать уже будет нечего, 
    #прийдет время оборвать цикл. До тех пор постоянно вызываем renameFolderExec 
    def renameFolder(self):
        is_end = True
        while is_end == True:
            is_end=self.renameFolderExec()
        

    
if __name__ == "__main__":   
    a = Rename()

    a.renameFolder()
    a.renameFile()