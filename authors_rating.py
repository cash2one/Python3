#!/usr/bin/python3

#        отступы табуляцией
#        by Andrew Sotnikov aka Luca Brasi,
#        e-mail: andruha.sota@mail.ru
#        --------------

        # Поддерживает в актуальном состоянии количество подписчиков и рейтинг
        # в таблце poets.

        # На основании свежего рейтинга авторов формирует ТОП - список самых
        # популярных авторов.

from saumysql import Crud
import collections

class Rating():

    def __init__(self):

        self.crud=Crud('localhost','andrew','andrew','verses')
        self.getFollowers()
        self.updateFollowers()

    # Подсчитывает количество подписчиков приходящегося на каждого автора.
    def getFollowers(self):

        # Получить всех подписчиков
        self.crud.sql="SELECT authors FROM contacts"
        authors=self.crud.readAct()
        temp_list=[]

        # Создадим глобальный список в где один элемен - один автор.
        for author_group in authors:
            temp_list.append(author_group[0])

        all_authors=','.join(temp_list)
        all_authors=all_authors.split(',')

        # Теперь в authors_list - словарь.
        # Ключи - это имена авторов, значения- подпсичики
        self.authors_list=collections.Counter(all_authors)
        self.followersInAll()


    # Обновляет таблицу poets. Пишет актуальное количество подписчиков в
    # поле followers, и рейтинг, который высчитываеться исходя из числа
    # подписчиков.
    def updateFollowers(self):

        self.authors_list=dict(self.authors_list)
        for key in self.authors_list:
            try:
                rating=self.calculateRating(self.authors_list[key])
                self.crud.sql='''UPDATE poets SET followers={0}
                                 WHERE id={1}'''.format(self.authors_list[key],
                                                        key)
                self.crud.updateAct()

                self.crud.sql='''UPDATE poets SET rating={0}
                                 WHERE id={1}'''.format(rating,key)
                self.crud.updateAct()

            except Exception:
                print('Блеать!')


    # Подсчитывает сколько подписчиков всего, с учетом задействованных авторов
    def followersInAll(self):

        followers_in_all=0
        for key in self.authors_list:
            try:
                followers_in_all=followers_in_all+int(self.authors_list[key])
            except TypeError:
                print('Блеать!')

        self.followers_in_all=followers_in_all

    # Получает число подписчиков и вычисляет рейтинг по несложной формуле.
    # Возвращает рейтинг в %
    def calculateRating(self,followers):

        rating=(followers/self.followers_in_all)*100
        rating=round(rating, 2)

        return rating


    def __del__(self):

        self.crud.closeConnection()


# Формирует HTML файл с ТОП - n атворов
class RatingFile():

    output_file='/tmp/authors_rating_file.html'
    top=15

    def __init__(self):
        self.getTopList()
        self.makeFile()
        print('Шикарно. Сфоримирован список авторов. Найти его можно по адресу '
              '- {0}'.format(self.output_file))


    # Получает список авторов
    def getTopList(self):

        self.crud=Crud('localhost','andrew','andrew','verses')
        self.crud.sql='''SELECT lastname, name, patronymic, rating FROM poets
                         ORDER BY rating DESC LIMIT {0}'''.format(self.top)
        self.authors=self.crud.readAct()

    # Запускает на исполнение создание файла авторов
    def makeFile(self):

        self.f=open(self.output_file,'w')
        self.doHeader()
        self.doTable()
        self.doFooter()
        self.f.close()

    # Фомирует хэдер файла
    def doHeader(self):

        self.f.write('''
        <!DOCTYPE html>
        <html>
        <head>
        <meta charset="UTF-8">
        </head>
        <body>
        <table>
        <title>Full poetry list</title>
        <style type="text/css">
        table {margin-left: auto;margin-right: auto; margin-top: 5%}
        td {padding: 5px 30px; font-size: 14pt}
        </style>
        ''')

    # Формирует футер
    def doFooter(self):

        self.f.write('''
        </table>
        </body>
        </html>
        ''')

    # Формирует таблицу с авторами. С учетом ранее полученных предпочтений
    # (сортировки и выводимых полей)
    def doTable(self):

        self.f.write('''<tr><td colspan="3" style='text-align:center'>
                        <b>ТОП-{0} АВТОРОВ</b></td></tr>
                        <tr><td style='height:90px'>№</td><td>автор</td>
                        <td>рейтинг</td></tr>
                        '''.format(self.top))
        i=1
        for row in self.authors:

            self.f.write(
                '''<tr><td>{0}</td><td>{1}</td><td>{2} %</td></tr>'''.format(
                    i,' '.join([row[0],row[1],row[2]]),row[3]))
            i=i+1

if __name__ == "__main__":

    obj=Rating()
    obj2=RatingFile()
