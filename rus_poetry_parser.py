#!/usr/bin/python3

#        отступы табуляцией
#        by Andrew Sotnikov aka Luca Brasi,
#        e-mail: andruha.sota@mail.ru
#        --------------

#        GUI для парсинга русских стихов с сайта
#        http://ru-poetry.ru/
#         В первом input'указать автора из адресной строки. Во втором полное
#         имя для внесения в базу.


from lxml import html
import requests, time, sys, saumysql, threading, re
from PyQt4 import QtGui
from PyQt4 import QtCore
import rus_parse_poet_view


class View(QtGui.QMainWindow, rus_parse_poet_view.Ui_MainWindow):

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


        # По окончанию выводим messagebox с выборкой из БД
        # по данному автору.
        # Т.е. в качестве инфы оторбажает количество стихов.
        if complete==True:

            crud=saumysql.Crud('localhost','andrew','andrew','verses')
            crud.sql='SELECT * FROM verses_list WHERE author=\'{0}\''.format(
                self.parser.fullname)
            verses_list=crud.readAct()
            number=len(verses_list)

            msg = QtGui.QMessageBox()
            msg.setIcon(QtGui.QMessageBox.Information)
            msg.setText("Сейчас в базе {0} стихов,\n\nавтора {1}".format(
                number, self.parser.fullname))
            msg.setWindowTitle("Verse database")
            msg.setStandardButtons(QtGui.QMessageBox.Ok)
            msg.exec()


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

    # Парсит окончания и адресной строки. Например, из строки:
    # http://ru-poetry.ru/poetry/6624
    # выберет -           poetry/6624
    # Возвратит список окончаний для заданного автора.
    def createEndOfLink(self):

        url='http://ru-poetry.ru/{0}'.format(self.author)

        page = requests.get(url)
        tree = html.fromstring(page.text)

        end=tree.xpath(".//*[@id='content']/div[1]/div[1]/div/div[2]/node()/"
                          "child::node()/child::node()/attribute::href")


        self.upper_limit=len(end)-1

        return end

    # Основная часть парсера
    def getVerse(self,end):

        url='http://ru-poetry.ru/{0}'.format(end)
        page = requests.get(url)
        tree = html.fromstring(page.text)


        v_name=tree.xpath(".//*[@id='content']/div[1]/div[1]/div/h1/text()")
        raw_v_content=tree.xpath(".//*[@id='content']/div[1]/div[1]/div/"
                                 "div[3]/child::text()")

        label='\n------------\n'
        v_name=v_name[0]
        print(v_name,label)

        v_content=[]
        # Форматируем содержимое. Удаляем отступы в начала строки.
        for row in raw_v_content:
            row=str(row).strip('\n')
            row=row.strip(' ')
            v_content.append(row)

        # Форматирование содержимого закончилось
        v_content='\n'.join(v_content)

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
