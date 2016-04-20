#!/usr/bin/python3

#        отступы табуляцией
#        by Andrew Sotnikov aka Luca Brasi,
#        e-mail: andruha.sota@mail.ru
#        --------------

        # GUI окошко для формирования списка авторов. На выходе дает html
        # файл. Есть функция превьюшника в браузере.


import author_list_view
from saumysql import Crud
import requests, time, sys, saumysql, re, subprocess, threading
from PyQt4 import QtGui
from PyQt4 import QtCore


class View(QtGui.QMainWindow, author_list_view.Ui_MainWindow):

    output_file='/tmp/authorslist.html'

    def __init__(self, parent=None):

        QtGui.QWidget.__init__(self,parent)
        self.setupUi(self)


    # Приводит в действие кнопку 'strart!'
    def handler(self):

        self.getChoice()
        html=makeHTML(self.output_file,self.sortBy,self.author_id,self.rating,
                      self.followers)

    # Приводит в действие кнопку 'select file'. Повляеться форма с выбором
    # файла для сохранения
    def getFname(self):

        filename = QtGui.QFileDialog()
        self.output_file=filename.getSaveFileName()
        print(self.output_file)


    # Формирует список предпочтений и для html-файла.
    # Порядок сорировки и вывод/невывод полей: id, rating, followers
    def getChoice(self):

        # Определим порядок сортировки
        self.sortBy = 'lastname'

        if self.radioButton.isChecked() == True:
            self.sortBy = 'lastname'
        elif self.radioButton_2.isChecked() == True:
            self.sortBy = 'name'
        elif self.radioButton_3.isChecked() == True:
            self.sortBy = 'id'
        elif self.radioButton_4.isChecked() == True:
            self.sortBy = 'rating'

        # Выберем нужные нам поля
        if self.checkBox.isChecked() == True:
            self.author_id=True
        else:
            self.author_id=False

        if self.checkBox_2.isChecked() == True:
            self.rating=True
        else:
            self.rating=False

        if self.checkBox_3.isChecked() == True:
            self.followers=True
        else:
            self.followers=False


    # Приводит в действие кнопку preview
    def previewHTML(self):

        self.getChoice()
        th1=threading.Thread(target=self.openInBrowser)
        th1.start()

    # Открывает в браузере превьюшник файла
    def openInBrowser(self):

        temporaryFile='/tmp/author_list_preview.html'
        html=makeHTML(temporaryFile,self.sortBy,self.author_id,self.rating,
                      self.followers)
        subprocess.call('firefox -new-tab {0}'.format(temporaryFile), shell=True)


class makeHTML():

    def __init__(self,output_file,sortBy,author_id,rating,followers):

        self.f=open(output_file,'w')
        self.sortBy=sortBy
        self.author_id=author_id
        self.rating=rating
        self.followers=followers

        self.doHeader()
        self.doTable()
        self.doFooter()
        self.f.close()

    # Фомирует хэдер файла
    def doHeader(self):

        self.f.write('''
        <!DOCTYPE html>
        <html>
        <head>
        <meta charset="UTF-8">
        </head>
        <body>
        <table>
        <title>Full poetry list</title>
        <style type="text/css">
        td {padding: 5px 30px; font-size: 14pt}
        </style>
        ''')

    # Формирует футер
    def doFooter(self):

        self.f.write('''
        </table>
        </body>
        </html>
        ''')

    # Формирует таблицу с авторами. С учетом ранее полученных предпочтений
    # (сортировки и выводимых полей)
    def doTable(self):

        sortBy='lastname'
        author_id=''
        rating=''
        followers=''

        crud=saumysql.Crud('localhost','andrew','andrew','verses')
        crud.sql='SELECT * FROM poets ORDER BY {0}'.format(sortBy)
        rows=crud.readAct()
        for row in rows:

            author_data=self.makeAuthorName(row)
            author_id='';rating='';followers=''
            if self.author_id == True:
                author_id='<td>{0:^20}</td>'.format(row[0])
            if self.rating == True:
                rating='<td>{0:^20}</td>'.format(row[5])
            if self.followers == True:
                followers='<td>{0:^10}</td>'.format(row[4])

            self.f.write('\n\t\t<tr>{0}{1}{2}{3}</tr>'.format(author_id,
            author_data, rating, followers))

    # Собирает имя файла из полученной строки таблицы poets.
    # Учитывает сорировку возвращает строку формата: Пушкин Александр Сергеевич
    # или же Александр Сергеевич Пушкин
    def makeAuthorName(self,row):

        if (self.sortBy == 'name') or (self.sortBy == 'id') or (
                    self.sortBy == 'rating'):
            author_data='<td>{0} {1} {2}</td>'.format(row[1],row[2],row[3])

        elif self.sortBy == 'lastname':
            author_data='<td>{0} {1} {2}</td>'.format(row[3],row[1],row[2])

        # Вырежем пробелы в начале строки
        author_data=author_data.strip()
        # Заменим двойные пробелы. Характерно для авторов без отчества
        author_data=author_data.replace('  ',' ')

        return author_data


if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)
    window=View()
    window.show()
    app.exec_()