#!/usr/bin/python3

#        отступы табуляцией
#        by Andrew Sotnikov aka Luca Brasi,
#        e-mail: andruha.sota@mail.ru
#        --------------
import  sys, pymysql

class Crud():

    sql='' #SQl запрос

    def __init__(self,host,user,passwd,dbname):

        #Подсодинение в БД
        self.db=pymysql.connect(host,user,passwd,dbname)
        self.db.set_charset('utf8')

    def createAct(self):

        # prepare a cursor object using cursor() method
        cursor = self.db.cursor()
        try:
            cursor.execute(self.sql)
            self.db.commit()
        except:
            print("Что-то пошло не так, метод create fail!")
            self.db.rollback()

    def readAct(self):

        cursor = self.db.cursor()
        try:
            cursor.execute(self.sql)

            if cursor.rowcount == 1:
                results=cursor.fetchone()
            else:
                results=cursor.fetchall()

            return  results
        except:
            print ("Error: unable to fetch data")

    def updateAct(self):

        cursor = self.db.cursor()
        try:
            cursor.execute(self.sql)
            self.db.commit()
        except:
            print("Что-то пошло не так, метод update fail")
            self.db.rollback()

    def deleteAct(self):

        cursor = self.db.cursor()
        try:
            cursor.execute(self.sql)
            self.db.commit()
        except:
            print("Что-то пошло не так, метод delete fail")
            self.db.rollback()

    def closeConnection(self):
        self.db.close()

if __name__ == "__main__":
    pass
