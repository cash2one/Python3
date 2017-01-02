#! /usr/bin/python3
# -*- coding: utf-8 -*-

#/* ******************** */
#   simplest and lightweight timer

#   requirements:
#       python3
#       PyQT4

#       wrote by:
#            Andrew Sotnikov <andruha.sota@mail.ru> 2016
#            aka Luca Brasi


import sys, time, threading
from PyQt4 import QtCore, QtGui



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

class Ui_Form(QtGui.QWidget):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.setupUi(self)
        self.timer_started = False
        #поключим кнопку start
        self.connect(self.pushButton,QtCore.SIGNAL('clicked()'),
             self.startTimer)
        #поключим кнопку pause
        self.connect(self.pushButton_2,QtCore.SIGNAL('clicked()'),
             self.pauseTimer)
        #поключим кнопку stop
        self.connect(self.pushButton_3,QtCore.SIGNAL('clicked()'),
             self.stopTimer)
        #пусть qlabel будет менять каждый раз при сигнале updateVal
        self.connect(self,QtCore.SIGNAL('updateVal()'),
             self.updateValues)
        #блокировка кнопки start
        self.start_btn_bl = None



    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(395, 166)
        self.horizontalLayoutWidget = QtGui.QWidget(Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(50, 100, 279, 81))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushButton = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton_3 = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.horizontalLayout.addWidget(self.pushButton_3)
        self.horizontalLayoutWidget_2 = QtGui.QWidget(Form)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(90, 10, 201, 80))
        self.horizontalLayoutWidget_2.setObjectName(_fromUtf8("horizontalLayoutWidget_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label = QtGui.QLabel(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(26)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        self.label_2 = QtGui.QLabel(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(26)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.label_3 = QtGui.QLabel(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(26)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_2.addWidget(self.label_3)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("sau_timer", "sau_timer", None))
        self.pushButton.setText(_translate("Form", "start", None))
        self.pushButton_2.setText(_translate("Form", "pause", None))
        self.pushButton_3.setText(_translate("Form", "stop", None))
        self.label.setText(_translate("Form", "00 :", None))
        self.label_2.setText(_translate("Form", "00 :", None))
        self.label_3.setText(_translate("Form", "00", None))

    #стартует таймер
    def startTimer(self):

        if (self.start_btn_bl != True):

            self.pause = False
            self.timer_started = True
            self.timer_hour = 0
            self.timer_min = 0
            self.timer_sec = 0
            #создаем и запускаем отдельный поток
            th1 = threading.Thread(target=self.timerLoop)
            th1.start()

    #слот для обновления значений в элементе qlabel
    def updateValues(self):

        #правим значения для каждого qlabel
        self.label.setText('{0:02d} :'.format(self.timer_hour))
        self.label_2.setText('{0:02d} :'.format(self.timer_min))
        self.label_3.setText('{0:02d}'.format(self.timer_sec))



    #цикл на высчитывание таймера, который запускаеться в отдельном
    #потоке
    def timerLoop(self):

        self.start_btn_bl = True

        while (self.timer_started == True):

            #каждую секунду делаем инкремент к счетчику и эмитируем
            #updateVal()
            time.sleep(1)
            if self.pause == False:
                self.timer_sec = self.timer_sec + 1
                self.emit(QtCore.SIGNAL('updateVal()'))

            #если секнды переваливают за 60 добавляем единицу к минуте
            #а табло с секундами очищаем до нуля
            if (self.timer_sec == 60):
                self.timer_min = self.timer_min + 1
                self.timer_sec = 0
            #если минуты переваливают за 60 добавляем единицу к часам
            #а табло с минутами очищаем до нуля
            if (self.timer_min == 60):
                self.timer_hour = self.timer_hour + 1
                self.timer_min = 0



    #пауза таймера
    def pauseTimer(self):

        if self.pause == False:
            self.pause = True

        else:
            self.pause = False

    #остановка таймера
    def stopTimer(self):

        self.pause = False
        self.timer_started = False
        self.start_btn_bl = False
        self.label.setText('00 :')
        self.label_2.setText(' 00 :')
        self.label_3.setText(' 00')



if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)
    window=Ui_Form()
    window.show()
    app.exec_()

