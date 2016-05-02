#!/usr/bin/python3
# messagebox.py

from PyQt4 import QtGui
from PyQt4 import QtCore
import  sys
import add_view, main_view, remove_view, edit_view
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


        self.crud.createAct()

    def editContacts(self,id,name,qpd,authors):

        authors=','.join(authors)
        self.crud.sql='''UPDATE contacts SET name='{0}',quantity_per_day='{1}',
                         authors='{2}' WHERE id=\'{3}\''''.format(name,qpd,
                                                                  authors,id)

        self.crud.updateAct()


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
        # Подключили кнопку refresh
        self.connect(self.pushButton_6,QtCore.SIGNAL('clicked()'),
             self.refreshTable)



    # Центрирование окна
    def center(self):

        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # Делает refresh таблицы. А то без него как то скучно.
    def refreshTable(self):

        self.tableWidget.clear()
        self.showIntoTable()

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
        name=self.tableWidget.item(currentRow,1).text()
        qpd=self.tableWidget.item(currentRow,3).text()
        print('Текущее значени выбранного элемента {0}'.format(id_value))
        crud=Model()
        self.window4 = None
        if int(qpd) !=0:
            crud.zeroizeQpd(id_value)

        else:

            if self.window4 is None:
                id_value=str(id_value)
                print(id_value)
                self.window4 = Edit(self)
                self.window4.selectPreviousAuthors(id_value)
                self.window4.showPreviousName(name)


            self.window4.show()


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
        self.results=self.getRow()
        self.crud.closeConnection()


        self.listWidget.setSelectionMode(
            QtGui.QAbstractItemView.MultiSelection)
        for x in self.results[0]:
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

        # Получим индексы выбранных авторов. Запишем их в indexes
        indexes=[]
        for item in items:
            index=self.listWidget.row(item)
            indexes.append(index)

        authors_id=[]
        for index in indexes:
            authors_id.append(str(self.results[1][index][0]))

        # Добавление в таблцу с контактами
        self.model=Model()
        self.model.addIntoContacts(self.lineEdit_2.text(),self.lineEdit.text(),
        self.lineEdit_4.text(), self.lineEdit_3.text(), authors_id)


    def getRow(self):

        self.crud.sql = ('SELECT lastname, name, patronymic '
                         'FROM poets ORDER BY lastname')
        raw_authors=self.crud.readAct()
        authors_name=[]
        for elem in raw_authors:
            authors_name.append([' '.join(elem)])

        self.crud.sql = ('SELECT id FROM poets ORDER BY lastname')
        authors_id=self.crud.readAct()

        return authors_name, authors_id


#Окно редактирования в БД
class Edit(QtGui.QWidget, edit_view.Ui_Form):


    def __init__(self, parent=None):

        super().__init__(parent=None)
        self.setupUi(self)
        self.addToList()

    # Выборка списка авторов из verses_list. Вывод выборки в listWidget
    # в окне добавления.
    def addToList(self):

        self.model=Model()
        self.results=self.getRow()

        self.listWidget.setSelectionMode(
            QtGui.QAbstractItemView.MultiSelection)
        for x in self.results[0]:
            self.listWidget.addItems(x)



    def uncheckAll(self):

        for row in range(0,self.listWidget.count()):

            item=self.listWidget.item(row)
            self.listWidget.setItemSelected(item,False)



    def printInput(self):


        items=self.listWidget.selectedItems()

        # Получим индексы выбранных авторов. Запишем их в indexes
        indexes=[]
        for item in items:
            index=self.listWidget.row(item)
            indexes.append(index)

        authors_id=[]
        for index in indexes:
            authors_id.append(str(self.results[1][index][0]))

        # Добавление в таблцу с контактами
        self.model=Model()
        self.model.editContacts(self.id,self.lineEdit_2.text(),self.spinBox.value(),
        authors_id)



    def getRow(self):

        self.model.crud.sql = ('SELECT lastname, name, patronymic '
                         'FROM poets ORDER BY lastname')
        raw_authors=self.model.crud.readAct()
        authors_name=[]
        for elem in raw_authors:
            authors_name.append([' '.join(elem)])

        self.model.crud.sql = ('SELECT id FROM poets ORDER BY lastname')
        authors_id=self.model.crud.readAct()

        return authors_name, authors_id


    def selectPreviousAuthors(self,id):

        self.id=id
        self.model.crud.sql = ('''SELECT authors FROM contacts
                                  WHERE id=\'{0}\''''.format(id))

        authors_id=self.model.crud.readAct()
        authors_id=authors_id[0].split(',')

        self.model.crud.sql = ('SELECT id FROM poets ORDER BY lastname')
        authors_list=self.model.crud.readAct()

        indexes=[]
        for author in enumerate(authors_list):
            for author_id in authors_id:

                # Он же нихера не строка!
                str_author = str(author[1][0])
                if author_id == str_author:
                    indexes.append(author[0])
        print(indexes)
        for row in indexes:
            listWidet_item=self.listWidget.item(row)
            listWidet_item.setSelected(True)


    def showPreviousName(self,name):

        self.lineEdit_2.setText(name)


if __name__ == "__main__":

    model=Model()

    app = QtGui.QApplication(sys.argv)
    window=Main()
    window.show()
    app.exec_()
