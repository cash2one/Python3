#!/usr/bin/python3

#        отступы табуляцией
#        by Andrew Sotnikov aka Luca Brasi,
#        e-mail: andruha.sota@mail.ru
#        --------------

        # Поддерживает в актуальном состоянии количество подписчиков и рейтинг
        # в таблце poets.

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


if __name__ == "__main__":

    obj=Rating()