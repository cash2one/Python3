#!/usr/bin/python3

#        отступы табуляцией
#        by Andrew Sotnikov aka Luca Brasi,
#        e-mail: andruha.sota@mail.ru
#        --------------

from saumysql import Crud


class AuthorTable():

    def __init__(self):

        self.crud=Crud('localhost','andrew','andrew','verses')
        self.existTable()

    def __del__(self):

        self.crud.closeConnection()

    def createPoetsTable(self):

        self.crud.sql='''CREATE TABLE poets (
                            id INT NOT NULL AUTO_INCREMENT,
                            PRIMARY KEY(id),
                            name VARCHAR(40) NOT NULL,
                            patronymic VARCHAR(40) NOT NULL,
                            lastname VARCHAR(40) NOT NULL,
                            followers INT NOT NULL,
                            rating float NOT NULL
                            );'''

        self.crud.createAct()

    def checkPoetsTable(self):

        self.crud.sql='SHOW TABLE STATUS LIKE \'poets\''
        authors = self.crud.readAct()
        if len(authors) == 0:
            print('Нету таблицы с авторами!')
            return False

        else:
            print('Есть такая таблица')
            return True


    def existTable(self):

        if self.checkPoetsTable() == False:
            self.createPoetsTable()




class FillAuthors():


    def __init__(self):

        self.crud=Crud('localhost','andrew','andrew','verses')
        self.gatAllAuthors()

    def __del__(self):

        self.crud.closeConnection()

    def parseAuthors(self,string):

        names=string.split(' ')
        temp_names=[]
        # Вырежем пробелы вокруг строки
        for x in names:
            temp_names.append(x.strip(' '))
        names=temp_names

        names_number=len(names)

        # Если тольоко фамилия
        if names_number == 1:

            author={'lastname':string,'name':'','patronymic':''}

        # Если фамилия имя
        elif names_number == 2:

            author={'lastname':names[1],'name':names[0],'patronymic':''}

        # Если фамилия, имя, отчество
        elif names_number == 3:

            author={'lastname':names[2],'name':names[0],
                    'patronymic':names[1]}

        return author



    def gatAllAuthors(self):

        self.crud.sql='SELECT DISTINCT author FROM verses_list'
        lst=self.crud.readAct()

        authors_list=[]
        # Пошел процесс преобразования фамилий
        for elem in lst:

            self.verseslist_IN_poets(elem[0])

    def verseslist_IN_poets(self,raw_author):

        author=self.parseAuthors(raw_author)
        self.crud.sql='''SELECT * FROM poets WHERE name=\'{0}\' and
                         patronymic=\'{1}\' and lastname=\'{2}\''''.format(
                    author['name'],author['patronymic'],author['lastname'])
        res = self.crud.readAct()
        if len(res) == 0:
            print('Автора {0} нету в списке!'.format(author['lastname']))
            id = self.addAuthorIntoPoets(author)
            self.updateAuthorID(id,raw_author)






    def addAuthorIntoPoets(self,author):

        self.crud.sql='''INSERT INTO poets (name, patronymic, lastname)
                      VALUES (\'{0}\',\'{1}\',\'{2}\')'''.format(
                      author['name'],author['patronymic'],author['lastname'])
        self.crud.createAct()

        self.crud.sql='''SELECT id FROM poets WHERE name=\'{0}\' and
                         patronymic=\'{1}\' and lastname=\'{2}\''''.format(
                    author['name'],author['patronymic'],author['lastname'])

        id=self.crud.readAct()

        return id[0]

    def updateAuthorID(self,id,author):

        self.crud.sql=('''UPDATE verses_list SET author_id=\'{0}\'
                       WHERE author=\'{1}\''''.format(id,author))
        print('Успешно присовен ID={0:5} автору {1}'.format(id,author))
        self.crud.updateAct()




if __name__ == "__main__":

    obj=AuthorTable()
    obj2=FillAuthors()
