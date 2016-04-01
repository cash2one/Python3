#!/usr/bin/python3

#        отступы табуляцией
#        by Andrew Sotnikov aka Luca Brasi,
#        e-mail: andruha.sota@mail.ru
#        --------------

#        GUI для парсинга буржейских стихов с сайта
#        http://famouspoetsandpoems.com/


from lxml import html
import requests, time, sys, saumysql, threading
from PyQt4 import QtGui
from PyQt4 import QtCore
import parse_poet_view


class View(QtGui.QMainWindow, parse_poet_view.Ui_MainWindow):

    def __init__(self, parent=None):

        QtGui.QWidget.__init__(self,parent)
        self.setupUi(self)
        self.connect(self.pushButton,QtCore.SIGNAL('clicked()'),
             self.setVal)


    def setVal(self):

        self.parser=Parse()
        self.parser.low_limit=int(self.lineEdit.text())
        self.parser.upper_limit=int(self.lineEdit_2.text())
        self.parser.author=self.lineEdit_3.text()
        self.parser.fullname=self.lineEdit_4.text()

        self.progressBar.setRange(self.parser.low_limit,self.parser.upper_limit)

        th1=threading.Thread(target=self.parser.runParser)
        th1.start()
        self.updateProgressBar()




    def updateProgressBar(self):

        complete=False
        while complete==False:
            time.sleep(0.1)
            try:
                if (self.parser.value==self.parser.upper_limit):
                    complete=True

                self.progressBar.setValue(self.parser.value)

            except Exception:
                pass


class Parse:

    low_limit=5965
    upper_limit=6050
    author='lord_byron'


    def runParser(self):


        url_end=range(self.low_limit,self.upper_limit+1)

        for x in url_end:
            self.getVerse(x)
            self.value=x



    def getVerse(self,end):

        url='http://famouspoetsandpoems.com/poets/{0}/poems/{1}'.format(
            self.author,end)
        page = requests.get(url)
        tree = html.fromstring(page.text)


        v_name=tree.xpath("/html/body/table/tr/td[1]/table[4]/tr/td[2]/div[4]/span")
        v_content=tree.xpath('/html/body/table/tr/td[1]/table[4]/tr/td[2]/div[5]/node()')

        label='\n------------\n'
        v_name=v_name[0].text

        print(v_name,label)
        previous=0
        for elem in v_content:
            if (type(elem).__name__) == 'HtmlElement' and previous == 'HtmlElement':
                print('\n')
            elif (type(elem).__name__) == 'HtmlElement':
                pass

            else:
                print(elem)

            previous=type(elem).__name__
            # print('previous -> {0}'.format(previous))





        time.sleep(1)

if __name__ == "__main__":

    # pare=Parse()

    app = QtGui.QApplication(sys.argv)
    window=View()
    window.show()
    app.exec_()
