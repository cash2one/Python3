#! /usr/bin/python

#        отступы табуляцией
#        by Andrew Sotnikov aka Luca Brasi,
#        e-mail: andruha.sota@mail.ru
#        --------------
from urllib.request import urlopen
import re, time, subprocess, os

# ---------------------------------------------------------------------------------------------------------
#
#     Скрипт заточен под скачку подкастов "English We Speak" с сайта BBC.
#     Работает по след принципу. Сначала формирует список ссылок (первого уровня), затем по этим ссылка переходит
#     и формирует ссылки второго уровня по который можно качать подкасты. Сразу после формирования ссылок - качает
#     подкасты.
#
# ---------------------------------------------------------------------------------------------------------

# Класс предназначен для скачки объектов первого уровня.
# То есть для генерации базовых ссылок.
class Parser1():

    path='/media/Maindata/Дело/English/BBC/English_we_speak/'

    def __init__(self,url,pattern):
        self.url=url
        self.pattern=pattern
        prog = re.compile(self.pattern)
        print('--------------')
        # print(self.url)
        f = urlopen(self.url)
        myfile = str(f.read())
        self.links=prog.findall(myfile)

    # Перебирает self.links, добавляя каждой ссылке в начало префикс.
    # Чтобы обеспечить поноценность ссылки.
    def appendSuf(self):
        temp=[]
        for elem in self.links:
            temp.append('http://www.bbc.co.uk'+elem)
        self.links=temp


    #Делает из ссылок множество, таким образом избавившись от повторений
    def delSame(self):
        self.links=set(self.links)

    # Печатает результаы для наглядности
    def printRes(self):
        i=0
        for x in self.links:
            i=i+1
            print ('{0:<3} {2:<4} http://www.bbc.co.uk{1}'.format(i,x,len(x)))

    # Получает список ссылок из файла .list_of_URL. Если файла нету - создает его.
    # Сравнивает ссылки имеющиеся ссылки с текущими ссылками на сайте. Разницу ссылок пишет в self.links.
    # Возвращет длину атрибут self.links.
    def getLinks(self):
        path=self.path+'.list_of_URL'

        try:
            f=open(path,'r')
            self.lastUrl=set(f)
            f.close()

        except FileNotFoundError:
            f=open(path,'w')
            for x in (set(self.links)):
                f.write(x+'\n')
            f.close()
            self.lastUrl=set([''])

        finally:
            temp=[]
            for x in self.links:
                if len(x) >= 100:
                    continue
                temp.append(x+'\n')
            self.currUrl=set(temp)
            self.links=self.currUrl-self.lastUrl
            print(self.links, sep='\n')
            print('Величина множества равно {0}'.format(len(self.links)))
            return len(self.links)

    # Обновляет список файлов.Удаляет старый список файлов, затем создает новый список и
    # пишет в него realtime ссылки.

    def updateLinks(self):
        path=self.path+'.list_of_URL'
        os.remove(path)
        f=open(path,'w')
        for x in (set(self.currUrl)):
            f.write(x)
        f.close()
        print('Файл со ссылками сначаоа удален, а затем обновлен')


    def writeLog(self):
        #Путь к log файлу
        self.log_file='/var/log/andrew/play_eng.log'
        result= self.getLinks()
        message=['Список ссылок свежий, ничего не было записано','Было записано {0} ссылок'.format(len(self.links))]
        if result == 0:
            info=message[0]
        else:
            info=message[1]
    #   Просто открывает файл и пишет туда сообщения
    #   Текст сообщения который будет записан в лог
        self.message=('{0}   {1} \n'.format(time.strftime("%d-%m-%Y %H:%M:%S"),info))
        print(self.message)

        f=open(self.log_file, 'a')
        f.write(self.message)
        print('Лог записан!')
        f.close()

# Класс предназначен для скачки объектов второго уровня.
# То есть mp3 и pdf

class Parser2(Parser1):
    def printRes(self):

        print(self.links[0])
        return self.links[0]

if __name__ == "__main__":


    url='http://www.bbc.co.uk/learningenglish/english/features/the-english-we-speak'
    pattern1=r'(?<=href\=\")(.*?ep-\d{6})'

    # Получение ссылок первого уровня
    P1=Parser1(url,pattern1)
    P1.appendSuf()
    P1.delSame()
    P1.writeLog()
    P1.printRes()
    P1.updateLinks()
    # Получение ссылок второго уровня
    pattern2=r'(?<=<a class=\"download bbcle-download-extension-mp3\" href\=\")(.*?[.]mp3)'
    pattern3=r'(?<=<a class=\"download bbcle-download-extension-pdf\" href\=\")(.*?[.]pdf)'
    for elem in P1.links:
        try:
            time.sleep(8)
            os.chdir(P1.path)
            P2=Parser2(elem,pattern2)
            P2.printRes()

            # Качаем MP3
            subprocess.call('wget {0}'.format(P2.printRes()),shell=True)
            time.sleep(6)

            P3=Parser2(elem,pattern3)
            P3.printRes()

            # Качаем PDF
            subprocess.call('wget {0}'.format(P3.printRes()),shell=True)
        except Exception:
            print('Блеать!')

