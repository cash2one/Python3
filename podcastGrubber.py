#! /usr/bin/python

#        отступы табуляцией
#        by Andrew Sotniokv aka Luca Brasi, 
#        e-mail: andruha.sota@mail.ru
#        --------------
from urllib.request import urlopen
import re, time, subprocess

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

    # Перебирает self.links. Если находит повторяющиеся ссылки то удаляет их.self.links
    def delSame(self):
        for elem in self.links:
            if (self.links.count(elem)) >= 2:
                self.links.remove(elem)
                print('Удален {0}'.format(elem))

    # Печатает результаы для наглядности
    def printRes(self):
        for x in self.links:
            print ('http://www.bbc.co.uk'+x)

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
    P1.printRes()

    # Получение ссылок второго уровня
    pattern2=r'(?<=<a class=\"download bbcle-download-extension-mp3\" href\=\")(.*?[.]mp3)'
    pattern3=r'(?<=<a class=\"download bbcle-download-extension-pdf\" href\=\")(.*?[.]pdf)'
    for elem in P1.links:
        try:
            time.sleep(8)
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

