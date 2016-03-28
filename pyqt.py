#!/usr/bin/python3
# messagebox.py

from PyQt4 import QtGui
from PyQt4 import QtCore
import  sys
import add_view, main_view, remove_view
from saumysql import Crud


class Model():

    def __init__(self):

        self.crud =  Crud('localhost','andrew','andrew','verses')
        self.existTable()

    def __del__(self):
        self.crud.closeConnection()

    def checkContactTable(self):

        self.crud.sql='SHOW TABLE STATUS LIKE \'contacts\''
        contacts = self.crud.readAct()
        if len(contacts) == 0:
            print('Нету таблицы с контактами!')
            return False

        else:
            print('Есть такая таблица')
            return True


    def createContactTable(self):

        self.crud.sql='''CREATE TABLE contacts (
                            id INT NOT NULL AUTO_INCREMENT,
                            PRIMARY KEY(id),
                            name VARCHAR(40) NOT NULL,
                            email VARCHAR(40) NOT NULL,
                            quantity_per_day INT NOT NULL,
                            intervals INT NOT NULL,
                            authors TEXT NOT NULL
                            );'''

        self.crud.createAct()


    def existTable(self):

        if self.checkContactTable() == False:
            self.createContactTable()

    def addIntoContacts(self,name,email,quantity_per_day,intervals,authors):

        authors=','.join(authors)

        self.crud.sql='''INSERT INTO contacts (name, email, quantity_per_day,
                         intervals, authors) VALUES (\'{0}\',\'{1}\', {2}, {3},
                         \'{4}\')'''.format(name,email,quantity_per_day,
                                            intervals, authors)

        print(self.crud.sql)
        self.crud.createAct()

    def removeFromContacts(self,id):

        id=int(id)
        self.crud.sql='DELETE FROM contacts WHERE id={0}'.format(id)
        self.crud.deleteAct()


    def zeroizeQpd(self,id):

        id=int(id)
        self.crud.sql=("UPDATE contacts SET quantity_per_day=0 "
                       "WHERE id={0}".format(id))
        self.crud.updateAct()



class Main(QtGui.QWidget, main_view.Ui_Form):

    def __init__(self, parent=None):

        QtGui.QWidget.__init__(self,parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.handleButton)
        self.pushButton_2.clicked.connect(self.handleButton2)
        #Окно добавления в БД
        self.window2 = None
        #Окно удаления из БД
        self.window3 = None

    def handleButton(self):

        if self.window2 is None:
            self.window2 = Add(self)
        self.window2.show()

    def handleButton2(self):

        if self.window3 is None:
            self.window3 = Remove(self)
        self.window3.show()


#Окно удаления в БД
class Remove(QtGui.QWidget, remove_view.Ui_Form):

    def __init__(self, parent=None):

        super().__init__(parent=None)
        self.setupUi(self)
        self.center()
        self.showIntoTable()


        # Подключили кнопку deactivate
        self.connect(self.pushButton_5,QtCore.SIGNAL('clicked()'),
             self.deactivateContact)
        # Подключили кнопку remove
        self.connect(self.pushButton_4,QtCore.SIGNAL('clicked()'),
             self.deleteRowData)
        # Подключили кнопку quit
        self.connect(self.pushButton_3,QtCore.SIGNAL('clicked()'),
             self.close)



    # Центрирование окна
    def center(self):

        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    # Делает выборку контактов из таблицы
    def fetchAllFromContacts(self):

        self.crud=Crud('localhost','andrew','andrew','verses')
        self.crud.sql='SELECT * FROM contacts ORDER BY name'
        self.contacts=self.crud.readAct()
        self.crud.closeConnection()


    def paintZeroQpd(self):

        color=QtGui.QColor(255,204,230)

        for row in range(0,self.tableWidget.rowCount()):
            qpd_col=self.tableWidget.item(row,3)
            qpd=int(qpd_col.text())
            if qpd == 0:

                for column in range(0,6):
                    cell=self.tableWidget.item(row,column)
                    cell.setBackgroundColor(color)







    # Выводит содержимое из БД в таблицу
    def showIntoTable(self):

        self.fetchAllFromContacts()
        rows=len(self.contacts)
        # Рисуем header и делаем разметку
        self.tableWidget.setRowCount(rows)
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels(['id','name','email',
        'quantity_per_day','intervals','authors'])
        # Выставим ширину столбцов
        self.tableWidget.setColumnWidth(1,160)
        self.tableWidget.setColumnWidth(2,160)
        self.tableWidget.setColumnWidth(5,798)
        # Растянем ширину столбца до контента хедера
        self.tableWidget.resizeColumnToContents(0)
        self.tableWidget.resizeColumnToContents(3)

        try:

            # Заполнение таблицы содержимым
            rownumb=0 #Номер текущего ряда
            for row in self.contacts:
                colnumb=0 #Номер текущего столбца
                for column in row:

                    if (colnumb == 3) or (colnumb == 4):
                        item=QtGui.QTableWidgetItem(str(column))
                        item.setTextAlignment(QtCore.Qt.AlignCenter)
                        self.tableWidget.setItem(rownumb,colnumb,item)

                    else:
                        self.tableWidget.setItem(rownumb,colnumb,
                                             QtGui.QTableWidgetItem(str(column)))

                    colnumb=colnumb+1
                rownumb=rownumb+1

            self.paintZeroQpd()
            # Таблица уже заполнена содержимым
        except TypeError:

            print('В таблице осталось мало записей!')


    # Удаляет выбранную строку из БД
    def deleteRowData(self):

        currentRow = self.tableWidget.currentRow()
        id_value=self.tableWidget.item(currentRow,0).text()
        print('Текущее значени выбранного элемента {0}'.format(id_value))
        crud=Model()
        crud.removeFromContacts(id_value)
        self.tableWidget.clear()
        self.showIntoTable()

    # Деактивирует выбранный контакт. Устанавливает значение qpd=0.
    # В результате контакт отписывается от рассылки.
    def deactivateContact(self):

        currentRow = self.tableWidget.currentRow()
        id_value=self.tableWidget.item(currentRow,0).text()
        print('Текущее значени выбранного элемента {0}'.format(id_value))
        crud=Model()
        crud.zeroizeQpd(id_value)
        self.tableWidget.clear()
        self.showIntoTable()



#Окно добавления в БД
class Add(QtGui.QWidget, add_view.Ui_Form):

    def __init__(self, parent=None):

        super().__init__(parent=None)
        self.setupUi(self)
        self.connect(self.pushButton,QtCore.SIGNAL('clicked()'),
                     self.printInput)

        self.connect(self.pushButton_2,QtCore.SIGNAL('clicked()'),
                     self.uncheckAll)

        self.addToList()

    # Выборка списка авторов из verses_list. Вывод выборки в listWidget
    # в окне добавления.
    def addToList(self):

        self.crud=Crud('localhost','andrew','andrew','verses')
        results=self.getRow('author','verses_list')
        self.crud.closeConnection()

        self.listWidget.setSelectionMode(
            QtGui.QAbstractItemView.MultiSelection)
        for x in results:
            self.listWidget.addItems(x)



    def uncheckAll(self):

        for row in range(0,self.listWidget.count()):

            item=self.listWidget.item(row)
            self.listWidget.setItemSelected(item,False)



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

        # Добавление в таблцу с контактами
        self.model=Model()
        self.model.addIntoContacts(self.lineEdit_2.text(),self.lineEdit.text(),
        self.lineEdit_4.text(), self.lineEdit_3.text(), self.selectedItems)


    def getRow(self,row,query):

        self.crud.sql = ('SELECT DISTINCT {0} FROM {1} ORDER BY {0}'.format(
            row,query))
        data=self.crud.readAct()

        return data

if __name__ == "__main__":

    model=Model()

    app = QtGui.QApplication(sys.argv)
    window=Main()
    window.show()
    app.exec_()
