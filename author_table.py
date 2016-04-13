#!/usr/bin/python3

#        отступы табуляцией
#        by Andrew Sotnikov aka Luca Brasi,
#        e-mail: andruha.sota@mail.ru
#        --------------

from saumysql import Crud
import re


# Создает таблицу poets, если такой нету
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


# Заполняет таблицу poets значениями
class FillAuthors():


    def __init__(self):

        self.crud=Crud('localhost','andrew','andrew','verses')
        self.gatAllAuthors()
        self.getOneLineAuthors()


    def __del__(self):

        self.crud.closeConnection()

    # Парсит автора. Получает строку типа Александр Сергеевич Пушкин.
    # Возвращает словарь: authors['name':Александр, 'patronymic':Сергеевич,
    # 'lastname':Пушкин]
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

    # Получает список всех авторов и ложит их в lst_distinct
    def gatAllAuthors(self):

        self.crud.sql='SELECT DISTINCT author FROM verses_list'
        self.lst_distinct=self.crud.readAct()

        authors_list=[]
        # Пошел процесс преобразования фамилий
        for elem in self.lst_distinct:

            self.verseslist_IN_poets(elem[0])

    # Соединяет список всех авторов в одну строку
    def getOneLineAuthors(self):

        self.authors_line=[]
        for elem in self.lst_distinct:

            self.authors_line.append(elem[0])

    # Проверяет наличие поэта в poets. Если такового нету - добавляет его
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

    # Получает список authors=[имя, отчество, фамилия]
    # Приводит в соответстиве таблицу poets. Если автор есть в poets, но его
    # нету в verses_list - этот автор удаляеться.
    def poets_IN_verseslist(self, author):

        lst_distinct=';'.join(self.authors_line)
        # author - это кортеж, поэтому создадим новую переменную
        lastname=author[2]

        # Если такая фамилия есть то поищем подетальней
        if lst_distinct.count(lastname) != 0:

            # Проекранируем спецсимволы
            lastname=lastname.replace('(','\(')
            lastname=lastname.replace(')','\)')
            pattern=r'{0}\s*{1}\s*{2}'.format(author[0],author[1],lastname)
            # Ищем по всем имеющимся параметрам. Имя, Отчество, Фамилия
            res=re.search(pattern,lst_distinct)
            if res == None:
                print('Такого автора действительно нету в verses_list'
                  ' {0} {1} {2}'.format(author[0],author[1],lastname))
                # Молча удаляем лишнего поэта
                self.crud.sql=("DELETE FROM poets WHERE name='{0}' and "
                               "patronymic='{1}' and lastname='{2}'").format(
                                author[0],author[1],author[2])
                self.crud.deleteAct()

        # Нету автора с такой фамилией? Смело можно удалять.
        else:
            print('Какой-то левый автор, нету его в verses_list'
                  ' {0}'.format(lastname))
            self.crud.sql=("DELETE FROM poets WHERE name='{0}' and "
               "patronymic='{1}' and lastname='{2}'").format(
                author[0],author[1],author[2])
            self.crud.deleteAct()



    # Непосредственно доавляет автора в poets table. Возвращет свеже присвоенное
    # id для данного поэта
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


    # Обновляет id поэта в verese_list table
    def updateAuthorID(self,id,author):

        self.crud.sql=('''UPDATE verses_list SET author_id=\'{0}\'
                       WHERE author=\'{1}\''''.format(id,author))
        print('Успешно присовен ID={0:5} автору {1}'.format(id,author))
        self.crud.updateAct()

    # Остюда начинаеться процесс синхронизации поэтов verses_list -> poets
    def synchroPoetryToVerses_list(self):

        self.crud.sql='SELECT name, patronymic, lastname FROM poets'
        authors=self.crud.readAct()
        for author in authors:
            self.poets_IN_verseslist(author)



if __name__ == "__main__":

    obj=AuthorTable()
    obj2=FillAuthors()
    obj2.synchroPoetryToVerses_list()
