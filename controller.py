#!/usr/bin/python3

#        отступы табуляцией
#        by Andrew Sotnikov aka Luca Brasi,
#        e-mail: andruha.sota@mail.ru
#        --------------

from saumysql import Crud
import time, random, pdb
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

        sender = 'andrew.sotnikov.hlam@mail.ru'
        receivers = [email]
        text='\tПривет {0}!\n\n\tТвой сегодняшний автор - {1}\n {2:-<30}\n'\
             '\tСтих называется: {3}\n {4:-<30}\n' \
             '{5}'.format(name,verse_data[1],' ',verse_data[2],' ',
              verse_data[3])

        message=MIMEText(text, _charset='utf-8')

        message['Subject']='Тебе пришел свежий стишок!)'


        try:
            smtp = smtplib.SMTP('Mech_engineer')
            smtp.send_message(message,sender,receivers)
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


if __name__ == "__main__":

    CreateQueueTable()
    SendMail()
    DropQueueTable()

