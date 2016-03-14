#!/usr/bin/python3
# messagebox.py

from PyQt4 import QtGui
from PyQt4 import QtCore
import  sys, pymysql
from add_view import *
from saumysql import Crud


class Main(QtGui.QWidget, Ui_Form):

    def __init__(self, parent=None):

        QtGui.QWidget.__init__(self,parent)
        self.setupUi(self)
        self.connect(self.pushButton,QtCore.SIGNAL('clicked()'),
                     self.printInput)
        self.addToList()


    def addToList(self):

        self.crud=Crud('localhost','andrew','andrew','verses')
        results=self.getRow('author','verses_list')
        self.crud.closeConnection()

        self.listWidget.setSelectionMode(
            QtGui.QAbstractItemView.MultiSelection)
        for x in results:
            self.listWidget.addItems(x)


    def printInput(self):

        print(self.lineEdit.text())
        print(self.lineEdit_2.text())
        print(self.lineEdit_3.text())
        print(self.lineEdit_4.text())
        items=self.listWidget.selectedItems()
        self.selectedItems=[]
        for x in items:
            self.selectedItems.append(x.text())
        print(self.selectedItems)

    def getRow(self,row,query):

        self.crud.sql = ('SELECT {0} FROM {1} LIMIT 150'.format(row,query))
        data=self.crud.readAct()

        return data



app = QtGui.QApplication(sys.argv)
icon=Main()
icon.show()
app.exec_()


