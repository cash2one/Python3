#!/usr/bin/python3

#        отступы табуляцией
#        by Andrew Sotnikov aka Luca Brasi,
#        e-mail: andruha.sota@mail.ru
#        --------------

from saumysql import Crud
import time, random, os
import smtplib
from email.mime.text import MIMEText


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

    # Принимает список предпочитаемых авторов. На основании списка авторов
    # возвращает id одного случайного стиха
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


    #Добавляет строку в таблицу Queue
    def addRowIntoQueue(self,name,email,exec_time,verse_id):

        # print(' Имя - {0},\n Email - {1},\n exec_time - {2},\n '
        #       'verse_id - {3}\n'.format(name,email,exec_time,verse_id))
        crud=Crud('localhost','andrew','andrew','verses')
        crud.sql="INSERT INTO queue (name, email, exec_time, verse_id)" \
                 "VALUES (\'{0}\',\'{1}\',\'{2}\',\'{3}\')".format(name,
                 email,exec_time,verse_id)
        crud.createAct()
        crud.closeConnection()


class SendMail():
    def __init__(self):
        crud=Crud('localhost','andrew','andrew','verses')

        #получить количество элементов queue
        crud.sql='SELECT * FROM queue'

        queue=crud.readAct()
        print(len(queue))
        # import pdb; pdb.set_trace()

        # отправить их в метод отправки
        for x in queue:
            self.sender(x)

        # Если не одного элемента не осталось - завершаем цикл
        # и подменяем значение на everythingToDo=True

        crud.closeConnection()

    #Получает сдежуюший кортеж элементов:
    #   id  	name 	email 	exec_time 	verse_id
    def sender(self,data):

        id=data[0]; name=data[1]; email=data[2]; verse_id=data[4]

        verse_data=self.getWholeVerseData(verse_id)
        # Формат verse_data: id  author  verse_name  verse_content

        text='\tПривет {0}!\n\n\tТвой сегодняшний автор - {1}\n {2:-<30}\n'\
             '\tСтих называется: {3}\n {4:-<30}\n' \
             '{5}'.format(name,verse_data[1],' ',verse_data[2],' ',
              verse_data[3])

        message=MIMEText(text, _charset='utf-8')

        message['From']='Andrew Sotnikov <andrew.sotnikov.hlam@mail.ru>'
        message['To']=email
        message['Subject']='Тебе пришел свежий стишок!)'

        try:
            smtp = smtplib.SMTP('Mech_engineer')
            smtp.send_message(message)
            smtp.quit()
            print ("Successfully sent email")
            #После отправки сообщения смело можем его удалять из очереди
            self.deleteFromQueue(id)

        except smtplib.SMTPException:
            print ("Error: unable to send email")

    # Получает id стиха и делает выборку из verses_list
    #Возрващает verse_data. Спецификация такая:
    #  id  author  verse_name  verse_content
    def getWholeVerseData(self, verse_id):
        crud=Crud('localhost','andrew','andrew','verses')
        crud.sql='SELECT * FROM verses_list WHERE id=\'{0}\''.format(verse_id)
        verse_data=crud.readAct()
        crud.closeConnection()

        return verse_data


    def deleteFromQueue(self, id):

        crud=Crud('localhost','andrew','andrew','verses')
        crud.sql='DELETE FROM verses_list WHERE id=\'{0}\''.format(id)
        verse_data=crud.deleteAct()
        crud.closeConnection()


class DropQueueTable():
    def __init__(self):

        #Удаляем queue
        crud=Crud('localhost','andrew','andrew','verses')
        crud.sql='DROP TABLE queue;'
        crud.deleteAct()
        print('Drop\'нули таблицу queue')
        crud.closeConnection()

class TimeMarks():

    #Текущее время
    curTime=round(time.time())
    #путь к лог-файлу
    logfile='/var/log/andrew/good_verse_mailer.log'

    def __init__(self):

        #Проверить наличие time_marks
        self.checkTimeMarksExist()
        self.clearLogFile()
        self.setQueueLock(0)


        self.crud.closeConnection()

    #Проверяет наличие таблицы time_marks. Если ее нет, то создает.
    #В противном случае проходит мимо
    def checkTimeMarksExist(self):

        self.crud=Crud('localhost','andrew','andrew','verses')
        self.crud.sql='SHOW TABLE STATUS LIKE \'time_marks\''
        result=self.crud.readAct()
        # Таблицы нету, её прийдеться создать
        if  len(result) == 0:
            print('Нету таблицы временных меток! Щас создадим')
            #Cоздадим таблицу time_marks
            self.crud.sql='''CREATE TABLE time_marks(
                            name VARCHAR(40) NOT NULL,
                            last_time INT NOT NULL,
                            locked BOOLEAN NOT NULL
                            );'''
            result=self.crud.createAct()
            #наполним значениями
            self.crud.sql=('INSERT INTO time_marks (name,last_time,locked)'
                     'VALUES (\'controller\',{0},false)'.format(
                round(time.time())
            ))
            self.crud.createAct()
            self.crud.sql=('INSERT INTO time_marks (name,last_time,locked)'
                     'VALUES (\'log\',{0},false)'.format(
                round(time.time())
            ))
            self.crud.createAct()


        #В противном случае можно завязывать с этапом создания time_marks
        else :
            print('time_marks?! Походу есть такая таблица!')

    # Удаляет лог-файл по истечении одной недели
    def clearLogFile(self):

        # Время недели в секунах - week = 7x24x3600 = 604800
        week = 604800
        self.crud.sql='SELECT last_time FROM time_marks WHERE name=\'log\''
        last_time = (self.crud.readAct())[0]
        elapsed = self.curTime - last_time

        #Проверяем сколько времени прошло
        if elapsed >= week:
            try:
                os.remove(self.logfile)
                print('А лога уже нету. Скоро будет новый')

            except Exception:
                print('А был ли лог вообще?')

        else:
            print('не торопись :) неделя еще не прошла')


    # Получает значени блокировки таблицы Queue
    def getQueueLock(self):

        self.crud.sql='SELECT locked FROM time_marks WHERE name=\'controller\''
        locked=self.crud.readAct();locked=locked[0]

        return locked

    # Принимает lockedval. Это булево значение в числовом виде (0 или 1).
    # На основе lockedval ставит бит доступа на запись в таблицу Queue.


    def setQueueLock(self,lockedval):

        self.crud.sql=('UPDATE time_marks SET locked=\'{0}\' WHERE '
                       'name=\'controller\''.format(lockedval))

        self.crud.updateAct()

        self.crud.sql=('SELECT locked FROM time_marks WHERE '
                       'name=\'controller\'')
        locked=(self.crud.readAct())[0]

        print('Значение locked было изменено. Текущее значение'
              ' {0}'.format(locked))


if __name__ == "__main__":

    # CreateQueueTable()
    # SendMail()
    # DropQueueTable()
    TimeMarks()
