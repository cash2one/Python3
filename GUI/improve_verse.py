#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'improve_verse.ui'


#    GUI interface for manage verses in GOOD VERSE MAILER database.
#    Provide following functions:

#        -select verse from db for overview
#        -change connent of selected verse


#        by Andrew Sotnikov aka Luca Brasi,
#        e-mail: andruha.sota@mail.ru
#        --------------



from PyQt4 import QtCore, QtGui
import sys, time
from saumysql import Crud

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):

        QtGui.QMainWindow.__init__(self,parent)
        self.setupUi(self)

        #поключим кнопку select
        self.connect(self.pushButton,QtCore.SIGNAL('clicked()'),
             self.selectValue)
        #поключим кнопку refresh
        self.connect(self.pushButton_6,QtCore.SIGNAL('clicked()'),
             self.refreshTextEdit)
        #поключим кнопку edit
        self.connect(self.pushButton_4,QtCore.SIGNAL('clicked()'),
             self.updateVerse)
        #поключим кнопку quit
        self.connect(self.pushButton_3,QtCore.SIGNAL('clicked()'),
             self.closeWindow)
        self.center()



    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(863, 743)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(30, 20, 201, 41))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setContentsMargins(5, 1, 10, 5)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.textEdit = QtGui.QTextEdit(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.textEdit.setFont(font)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.horizontalLayout.addWidget(self.textEdit)
        self.pushButton = QtGui.QPushButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout.addWidget(self.pushButton)
        self.horizontalLayout.setStretch(0, 1)
        self.textBrowser = QtGui.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(30, 90, 791, 521))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.textBrowser.setFont(font)
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.pushButton_6 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(30, 630, 146, 39))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_6.sizePolicy().hasHeightForWidth())
        self.pushButton_6.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_6.setFont(font)
        self.pushButton_6.setObjectName(_fromUtf8("pushButton_6"))
        self.horizontalLayoutWidget_2 = QtGui.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(440, 630, 381, 41))
        self.horizontalLayoutWidget_2.setObjectName(_fromUtf8("horizontalLayoutWidget_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setSpacing(100)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.pushButton_4 = QtGui.QPushButton(self.horizontalLayoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_4.sizePolicy().hasHeightForWidth())
        self.pushButton_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.horizontalLayout_2.addWidget(self.pushButton_4)
        self.pushButton_3 = QtGui.QPushButton(self.horizontalLayoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.horizontalLayout_2.addWidget(self.pushButton_3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 863, 27))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.textEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Droid Sans\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">99999</p></body></html>", None))
        self.pushButton.setWhatsThis(_translate("MainWindow", "get element in DB by this ID", None))
        self.pushButton.setText(_translate("MainWindow", "select", None))
        self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Droid Sans\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">your verse appear here...</p></body></html>", None))
        self.pushButton_6.setWhatsThis(_translate("MainWindow", "get fresh values from DB", None))
        self.pushButton_6.setText(_translate("MainWindow", "refresh", None))
        self.pushButton_4.setWhatsThis(_translate("MainWindow", "this button get text from text edit and adjust in accordance with DB", None))
        self.pushButton_4.setText(_translate("MainWindow", "edit", None))
        self.pushButton_3.setWhatsThis(_translate("MainWindow", "leave Main window", None))
        self.pushButton_3.setText(_translate("MainWindow", "quit", None))
        
#    центрирование окна
    def center(self):
        frameGm = self.frameGeometry()
        screen = QtGui.QApplication.desktop().screenNumber(QtGui.QApplication.desktop().cursor().pos())
        centerPoint = QtGui.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())


#    получает текущее значение поля с id        
    def selectValue(self):
   
#       получаем значение input'a с ID                   
        verseID = self.textEdit.toPlainText()
        self.model = Model()
        self.model.getVerseContent(verseID)
        self.verseContent = self.model.getVerseContent(verseID)
        self.showVerseContent()
        print('Значение получено!')

#    отображение стишка в поле
    def showVerseContent(self):
    
        self.textBrowser.setText(self.verseContent)
        self.textBrowser.setReadOnly(False)

                
#    получаем новые значения стишка из БД и отображаем их в форме
    def refreshTextEdit(self):
        
        #       получаем значение input'a с ID                   
        verseID = self.textEdit.toPlainText()
        self.model = Model()
        self.model.getVerseContent(verseID)
        self.verseContent = self.model.getVerseContent(verseID)
#        чтобы не было путаницы, добавим строрку 'новые значения'
        self.textBrowser.setText("{0:#^60}\n\n{1}".format('FROM DB',self.verseContent))
        self.textBrowser.setReadOnly(False)
        print('Обновлено в БД!')
    
    def updateVerse(self):

#       получаем значение input'a с ID           
        verseID = self.textEdit.toPlainText()
#       получаем текущий текст отредактированного стишка        
        improvedVerseContent = self.textBrowser.toPlainText()
        self.model = Model()
        self.model.changeVerseContent(verseID, improvedVerseContent)
        
        
        
        
    #   закрывает MainWindow        
    def closeWindow(self):
    
        self.close()
        
        
class Model():

    def __init__(self):

        self.crud =  Crud('localhost','andrew','andrew','verses')

    def __del__(self):
        self.crud.closeConnection()


#    получает текст стишка по заданному ID
    def getVerseContent(self,idVal):

        self.crud.sql='''SELECT verse_content FROM `verses_list` WHERE `id`={0}'''.format(idVal)
        verseContent = self.crud.readAct()

        return verseContent[0]

#    меняет содержание стишка в БД
    def changeVerseContent(self, idVal, verseContent):
    
        self.crud.sql='''UPDATE verses_list SET verse_content='{1}' 
        WHERE id={0}'''.format(idVal, verseContent)
        self.crud.updateAct()


if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)
    window=Ui_MainWindow()
    window.show()
    app.exec_()





