#!/usr/bin/python3

#        отступы табуляцией
#        by Andrew Sotnikov aka Luca Brasi,
#        e-mail: andruha.sota@mail.ru
#        --------------

        # Заменяет в таблице имена авторов на id в таблице contacts


from saumysql import Crud
import time, sys, saumysql

class ConvertAuthors():

    def __init__(self):

        self.crud=saumysql.Crud('localhost','andrew','andrew','verses')
        self.main()


    def __del__(self):

        self.crud.closeConnection()


    # Перебирает профиль контактов. В каждом контакте где есть имя автора в
    # символьной форме - подменяет его на числовое.
    def main(self):

        self.crud.sql='SELECT authors,id FROM contacts'
        contacts=self.crud.readAct()
        for contact in contacts:

            literalAuthors=contact[0]
            customer_id=contact[1]
            id_authors=self.literalToDigits(literalAuthors)
            self.crud.sql='''UPDATE contacts SET authors='{0}'
                             WHERE id='{1}\''''.format(id_authors,customer_id)
            self.crud.updateAct()


    # Получает строку авторов. Разбирает ее возвращает строку где вместо
    # вместо имен авторов - author_id
    def literalToDigits(self,literalAuthors):

        self.crud.sql=('SELECT name, patronymic, lastname, id '
                                   'FROM poets')

        author_data=self.crud.readAct()
        temp_author_data=[]

        # Сводим ИМЯ, ОТЧЕСТВО, ФАМИЛИЯ - в одну строку
        for x in author_data:

            author=' '.join([x[0],x[1],x[2]])
            # Вырежем пробелы в начале строки
            author=author.strip()
            # Заменим двойные пробелы. Характерно для авторов без отчества
            author=author.replace('  ',' ')
            authorANDid=[author,x[3]]
            temp_author_data.append(authorANDid)


        digitsAuthor=literalAuthors
        for author in temp_author_data:

            literal=str(author[0])
            digit=str(author[1])
            # if literalAuthors.count(literal) >0:
            #     print(literal,'----',digit,'----')
            digitsAuthor=digitsAuthor.replace(literal,digit)

        digitsAuthor=digitsAuthor.strip()
        print(digitsAuthor)

        return digitsAuthor


if __name__ == "__main__":

    obj=ConvertAuthors()