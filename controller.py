#!/usr/bin/python3

#        отступы табуляцией
#        by Andrew Sotnikov aka Luca Brasi,
#        e-mail: andruha.sota@mail.ru
#        --------------

from saumysql import Crud
import time, random, pdb


        # CONTROLLER
class CreateQueueTable:

    def __init__(self):
        # Время для начала отсчета
        st_time=round(time.time())
        exec_time=round(time.time())
        #задержка межу отправками сообщения получателям
        delay=5

        #Проверить существует ли таблица queue
        crud=Crud('localhost','andrew','andrew','verses')
        crud.sql='SHOW TABLE STATUS LIKE \'queue\''
        result=crud.readAct()
        # Таблицы нету, его прийдеться создать
        if  len(result) == 0:
            print('Нету таблицы queue!')
            #Cоздадим таблицу queue
            crud.sql='''CREATE TABLE queue(
                            id INT NOT NULL AUTO_INCREMENT,
                            name VARCHAR(40) NOT NULL,
                            email VARCHAR(40) NOT NULL,
                            exec_time INT NOT NULL,
                            verse_id INT NOT NULL,
                            PRIMARY KEY (id)
                            );'''
            result=crud.createAct()

        #В противном случае можно завязывать с этапом создания queue
        else :
            print('queue?! Походу есть такая таблица!')

        # Сделать выборку из таблицы с контактами
        crud.sql = 'SELECT * FROM contacts'
        list = crud.readAct()
        print(list)

        for row in list:
            name=str(row[0])
            email=str(row[1])
            interval=int(row[3])
            authors=str(row[4])
            # quantity_per_day
            qpd=int(row[2])

            if qpd == 1:
                # каждый раз генериуем новый verse_id для следущего абонента
                # в таблице queue
                verse_id=self.getRandVerseID(authors)
                exec_time = exec_time + delay
                self.addRowIntoQueue(name,email,exec_time,verse_id)

            else:
                #то же что и в ветке if, только для больего количества qpd
                print('qpd is {0}'.format(qpd))

                for once in range(0,qpd):
                    verse_id=self.getRandVerseID(authors)
                    exec_time = exec_time + delay + interval
                    self.addRowIntoQueue(name,email,exec_time,verse_id)


        crud.closeConnection()


    def getRandVerseID(self,authors):

        # получить случайного автора
        authors=authors.split(',')
        rand_author=(random.choice(authors)).strip()
        print('random autor ------ > {0}'.format(rand_author))
        #получить случайный verse_id
        crud=Crud('localhost','andrew','andrew','verses')
        crud.sql='''SELECT id FROM verses_list WHERE author=\'{0}\'
                 ORDER BY RAND() LIMIT 1'''.format(rand_author)
        #Возвращает кортеж, поэтому прийдеться извлечь ключ
        verse_id=(crud.readAct())[0]
        crud.closeConnection()
        # import pdb; pdb.set_trace()
        print(verse_id)

        return verse_id

    def addRowIntoQueue(self,name,email,exec_time,verse_id):

        print(' Имя - {0},\n Email - {1},\n exec_time - {2},\n '
              'verse_id - {3}\n'.format(name,email,exec_time,verse_id))




class DropQueueTable():
    def __init__(self):

        #Удаляем queue
        crud=Crud('localhost','andrew','andrew','verses')
        crud.sql='DROP TABLE queue;'
        crud.deleteAct()
        print('Drop\'нули таблицу queue')
        crud.closeConnection()




if __name__ == "__main__":
    name=CreateQueueTable()
    #drop=DropQueueTable()