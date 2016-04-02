#!/usr/bin/python3

#        отступы табуляцией
#        by Andrew Sotnikov aka Luca Brasi,
#        e-mail: andruha.sota@mail.ru
#        --------------

#        GUI для парсинга буржейских стихов с сайта
#        http://famouspoetsandpoems.com/
#         В первом input'указать автора из адресной строки. Во втором полное
#         имя для внесения в базу.


from lxml import html
import requests, time, sys, saumysql, threading, re
from PyQt4 import QtGui
from PyQt4 import QtCore
import parse_poet_view


class View(QtGui.QMainWindow, parse_poet_view.Ui_MainWindow):

    def __init__(self, parent=None):

        QtGui.QWidget.__init__(self,parent)
        self.setupUi(self)
        self.connect(self.pushButton,QtCore.SIGNAL('clicked()'),
             self.setVal)
        self.progressBar.reset()

    # Вызываеться при нажании на кнопку "start!".
    # Запускает парсер
    def setVal(self):

        self.parser=Parse()
        self.parser.author=self.lineEdit_3.text()
        self.parser.fullname=self.lineEdit_4.text()
        th1=threading.Thread(target=self.parser.runParser)
        th1.start()
        self.updateProgressBar()


    # Обновляет progress-bar
    def updateProgressBar(self):

        complete=False
        while complete==False:
            time.sleep(0.5)
            try:
                self.progressBar.setRange(self.parser.low_limit,self.parser.upper_limit)
                print('Это был стих {0} / {1}'.format(self.progressBar.value(),
                self.progressBar.maximum()))
                if (self.parser.value==self.parser.upper_limit):
                    complete=True

                self.progressBar.setValue(self.parser.value)

            except Exception:
                pass

class Parse:

    # Имя в url
    author=''
    fullname=''
    # Задержка между подключениями
    delay=2
    # progress_bar
    low_limit=0


    # Запускает парсер
    def runParser(self):

        url_end=self.createEndOfLink()
        i=0
        for x in url_end:
            self.getVerse(x)
            self.value=i
            i=i+1

    # Парсит окончания и адресной строки.  Например, match'ит 15703 из:
    # http://famouspoetsandpoems.com/poets/pablo_neruda/poems/15703
    # Возвратит список окончаний для заданного автора.
    def createEndOfLink(self):

        url='http://famouspoetsandpoems.com/poets/{0}/poems'.format(self.author)

        page = requests.get(url)
        tree = html.fromstring(page.text)

        v_name=tree.xpath("/html/body/table/tr/td[1]/table[4]/tr/td[2]/"
                          "table[2]/child::node()/child::*/child::*/attribute::*")

        end=[]
        for elem in v_name:
            elem=re.search(r'(?<=/poems/).+',str(elem))
            res=elem.group(0)
            end.append(res)

        self.upper_limit=len(end)-1

        return end

    # Основная часть парсера
    def getVerse(self,end):

        url='http://famouspoetsandpoems.com/poets/{0}/poems/{1}'.format(
            self.author,end)
        page = requests.get(url)
        tree = html.fromstring(page.text)


        v_name=tree.xpath("/html/body/table/tr/td[1]/table[4]/tr/td[2]/"
                          "div[4]/span")
        raw_v_content=tree.xpath('/html/body/table/tr/td[1]/table[4]/tr/td[2]/'
                             'div[5]/node()')

        label='\n------------\n'
        v_name=str(v_name[0].text)
        v_name=v_name.strip(' ')

        print(v_name,label)

        v_content=[]
        previous=0

        # Форматирование содержимого стиха
        for elem in raw_v_content:
            if (type(elem).__name__) == 'HtmlElement' and previous == 'HtmlElement':

                v_content.append('\n')
            elif (type(elem).__name__) == 'HtmlElement':
                pass
            else:
                elem=str(elem).lstrip('\n')
                elem=str(elem).lstrip('\t')
                v_content.append(elem.strip(' '))

            previous=type(elem).__name__

        v_content='\n'.join(v_content)
        # Форматирование содержимого закончилось
        self.addIntoVersesList(self.fullname, v_name, v_content)

        time.sleep(self.delay)


    # Добавляет стишок в таблицу verses_list
    def addIntoVersesList(self,author,verse_name,verse_content):

        author=author.strip(' ')
        verse_content=verse_content.replace('\'','\\\'' )

        crud=saumysql.Crud('localhost','andrew','andrew','verses')
        crud.sql='''INSERT INTO verses_list (author, verse_name, verse_content)
                    VALUES (\'{0}\',\'{1}\',\'{2}\')'''.format(
                    author, verse_name, verse_content)
        print(verse_name)
        crud.createAct()
        crud.closeConnection()

if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)
    window=View()
    window.show()
    app.exec_()
