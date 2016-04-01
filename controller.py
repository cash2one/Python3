#!/usr/bin/python3

#        отступы табуляцией
#        by Andrew Sotnikov aka Luca Brasi,
#        e-mail: andruha.sota@mail.ru
#        --------------

from saumysql import Crud
import time, random, os, saulog
import smtplib
from email.mime.text import MIMEText


#       #       #       #    CONTROLLER     #       #       #       #
#
# Приводит в действие механизм рассылки стишков. Работает с MySQL БД
# verses. Минимальный набор для безошибочной рабыты:
# БД                           verses:
#                                |
#                       _________|__________
#                      |                    |
# таблицы         verses_list            contacts
#
#       #       #       #    CONTROLLER     #       #       #       #



# Все что касается логирования
class Logs():

    #Текущее время
    curTime=round(time.time())
    #путь к лог-файлу
    logfile='/var/log/andrew/good_verse_mailer.log'


    # Делает запись текщего дня в файле с логом
    def printDay(self):

        f = open(self.logfile, 'a')
        f.write('{0:-^140}\n{1:-^140}\n{2:-^140}\n'.format(
            '',(time.strftime('%A')),''))
        f.close()


    # Удаляет лог-файл по истечении одной недели
    def clearLogFile(self):

        # Время недели в секунах - week = 7x24x3600 = 604800
        week = 86400
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

            finally:

                TimeMarks.setActualLogTime(self)

        else:
            print('не торопись :) неделя еще не прошла')

    #Пишет в логфайл инфу об отправке
    def writeSendInfo(self,name,email,author,verse_name,verse_ID ):

        message=('Для {0} (e-mail {1}): \n\tавтор - {2}, \n\tназвание: {3},'
                '\n\tID: {4}').format(name,email,author,verse_name,verse_ID)
        saulog.WriteLog(self.logfile, message)


# Создает таблицу queue. В ней формируються данные необходимые для рассылки,
# посредством SendMail.
class CreateQueueTable(Logs):

    def __init__(self):

        # Время для начала отсчета
        st_time=self.curTime
        #задержка межу отправками сообщения получателям
        delay=-10

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
        #print(list)

        for row in list:
            exec_time=self.curTime
            name=str(row[1])
            email=str(row[2])
            interval=2
            authors=str(row[5])
            # quantity_per_day - желаемое количество стишков в день
            qpd=int(row[3])

            if qpd == 0:
                print('Этот человек уже отписался от рассылки!')
                continue

            elif qpd == 1:
                # каждый раз генериуем новый verse_id для следущего абонента
                # в таблице queue
                verse_id=self.getRandVerseID(authors)
                exec_time = exec_time + delay
                self.addRowIntoQueue(name,email,exec_time,verse_id)

            # Для тех кто отписался от рассылки стишки не рассылаем!

            else:
                #то же что и в ветке if, только для больего количества qpd
                #print('qpd is {0}'.format(qpd))
                interval_list=self.calculateDayInterval(qpd)

                for once,interval in zip((range(0,qpd)),interval_list):

                    exec_time=self.curTime
                    verse_id=self.getRandVerseID(authors)
                    exec_time = exec_time + delay + interval
                    self.addRowIntoQueue(name,email,exec_time,verse_id)

        crud.closeConnection()
        self.queueBlocker()

    # Принимает список предпочитаемых авторов. На основании списка авторов
    # возвращает id одного случайного стиха
    def getRandVerseID(self,authors):

        # получить случайного автора
        authors=authors.split(',')
        rand_author=(random.choice(authors)).strip()
        #print('random autor ------ > {0}'.format(rand_author))
        #получить случайный verse_id
        crud=Crud('localhost','andrew','andrew','verses')
        crud.sql='''SELECT id FROM verses_list WHERE author=\'{0}\'
                 ORDER BY RAND() LIMIT 1'''.format(rand_author)
        #Возвращает кортеж, поэтому прийдеться извлечь ключ
        verse_id=(crud.readAct())[0]
        crud.closeConnection()

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

    # Возвращает список интервалов с учетом жедаемого количества
    # повторов в день(день принят за 10 часов)

    def calculateDayInterval(self,reruns):

        #Принимает, что в максимальный период отправки составляет 10 часов
        hours_in_day=36000

        if reruns >= 2:
            offset=round(hours_in_day/(reruns-1))
            interval=[]
            lap=0
            for x in (range(0,reruns)):
                interval.append(lap)
                lap=lap+offset
        else:
            interval=0

        return interval


    # Создает фейковую строку которая задерживает очередь и не дает
    # повторно вызываться log.printDay
    def queueBlocker(self):

        exec_time = self.curTime+72000
        crud=Crud('localhost','andrew','andrew','verses')
        crud.sql="INSERT INTO queue (name, email, exec_time, verse_id)" \
                 "VALUES (\'{0}\',\'{1}\',\'{2}\',\'{3}\')".format(
                'blocker_queue','none',exec_time,1234567)
        crud.createAct()
        crud.closeConnection()


class SendMail(Logs):

    everything_was_do=False #Аттрибут завершения рассылки

    def __init__(self):

        crud=Crud('localhost','andrew','andrew','verses')
        #получить количество элементов queue
        crud.sql='SELECT * FROM queue'
        queue=crud.readAct()
        print(len(queue))
        if (len(queue)) >= 1:

            # По-тихоньку отправляем письма из очереди
            for x in queue:

                if self.canSend(x[0]) == True:
                    self.sender(x)
                    # Если не одного элемента не осталось - завершаем цикл
                else:
                    'Прийдеться подождать с отправкой сообщений...'
        else:
            print('Очередь на данный момент пустая!')

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
            time.sleep(5) #Чтобы не грузить сервер
            smtp = smtplib.SMTP('Mech_engineer')
            smtp.send_message(message)
            smtp.quit()
            print ("Successfully sent email")

            #Запишем лог
            self.writeSendInfo(name,email,verse_data[1],verse_data[2],verse_id)
            #После отправки сообщения смело можем его удалять из очереди
            self.deleteFromQueue(id)

        except smtplib.SMTPException:
            print ("Error: unable to send email")

    # Получает id стиха и делает выборку из verses_list
    #Возрващает verse_data. Спецификация такая:
    #
    #  id         author         verse_name         verse_content
    def getWholeVerseData(self, verse_id):
        crud=Crud('localhost','andrew','andrew','verses')
        crud.sql='SELECT * FROM verses_list WHERE id=\'{0}\''.format(verse_id)
        verse_data=crud.readAct()
        crud.closeConnection()

        return verse_data

    # По id удаляет элемент из очереди. Рассчитано что он удаляеться после
    # успешной отправки адресату.
    def deleteFromQueue(self, id):

        crud=Crud('localhost','andrew','andrew','verses')
        crud.sql='DELETE FROM queue WHERE id=\'{0}\''.format(id)
        verse_data=crud.deleteAct()
        crud.closeConnection()

    # На основе временных меток проверяет можно ли отсылать строку
    # из очереди.
    def canSend(self, id):

        crud=Crud('localhost','andrew','andrew','verses')
        crud.sql='SELECT exec_time FROM queue WHERE id=\'{0}\''.format(id)
        exec_time=(crud.readAct())[0]
        curTime=round(time.time())
        crud.closeConnection()

        if curTime >= exec_time:
            print(curTime-exec_time)
            return True
        else:
            print(curTime-exec_time)
            return False

# Удаляет таблицу с очередью
class DropQueueTable(Logs):
    def __init__(self):

        #Удаляем queue
        crud=Crud('localhost','andrew','andrew','verses')
        crud.sql='DROP TABLE queue;'
        crud.deleteAct()
        print('Drop\'нули таблицу queue')
        crud.closeConnection()

# Создает таблицу временных меток и поддерживает ее дальнейшее
# функицонирование
class TimeMarks(Logs):

    def __init__(self):

        #Проверить наличие time_marks
        self.checkTimeMarksExist()
        self.clearLogFile()
        #Пробуем разблокировать очередь, если прошло 20 часов
        self.unlockQueue()

    def __del__(self):

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
                     'VALUES (\'queue\',{0},false)'.format(self.curTime))
            self.crud.createAct()
            self.crud.sql=('INSERT INTO time_marks (name,last_time,locked)'
                     'VALUES (\'log\',{0},false)'.format(self.curTime))
            self.crud.createAct()

        #В противном случае можно завязывать с этапом создания time_marks
        else :
            print('time_marks?! Походу есть такая таблица!')


    # Получает значени блокировки таблицы queue
    def getQueueLock(self):

        self.crud.sql='SELECT locked FROM time_marks WHERE name=\'queue\''
        locked=self.crud.readAct()
        locked=locked[0]

        return locked

    # Принимает lockedval. Это булево значение в числовом виде (0 или 1).
    # На основе lockedval ставит бит доступа на запись в таблицу Queue.
    def setQueueLock(self,lockedval):


        self.crud.sql=('UPDATE time_marks SET locked=\'{0}\' WHERE '
                       'name=\'queue\''.format(lockedval))
        self.crud.updateAct()

        self.crud.sql=('SELECT locked FROM time_marks WHERE '
                       'name=\'queue\'')
        locked=(self.crud.readAct())[0]
        print('Значение locked было изменено. Текущее значение'
              ' {0}'.format(locked))


    # Снимает блокировку на запись таблицы queue. Делает это только при
    # случае если минуло значение времени allowed_time
    def unlockQueue(self):

        allowed_time=72000 #Эквивалентно 20-ти часам

        self.crud.sql=('SELECT last_time FROM time_marks WHERE name=\'queue\'')
        last_time=self.crud.readAct()[0]

        elapsed = self.curTime - last_time
        print('Прошло времени - {0}, а нужно {1} для сбрасывания '
                  'блокировки'.format(elapsed,allowed_time))

        if elapsed >= allowed_time:
            #Снять блокировку с queue
            self.setQueueLock(0)
            # выставим актуальное время
            self.setActualQueueTime()

        else:
            print('Еще рано сбрасывать блокировку')


    # Выставляет текущее время в таблице временных меток для строки queue
    def setActualQueueTime(self):

        actual_time=self.curTime
        self.crud.sql=('UPDATE time_marks SET last_time=\'{0}\' WHERE '
                       'name=\'queue\''.format(actual_time))
        self.crud.updateAct()


    # Выставляет текущее время в таблице временных меток для строки log
    def setActualLogTime(self):

        actual_time=self.curTime
        self.crud.sql=('UPDATE time_marks SET last_time=\'{0}\' WHERE '
                       'name=\'log\''.format(actual_time))
        self.crud.updateAct()

# ___________________________________________________________
# __________________________OBJECTS__________________________
# ___________________________________________________________


if __name__ == "__main__":

    time_marks = TimeMarks()

    # Уж если нет блокировки на queue - сам Бог велел начать все с чистого
    # листа, удалив таблициу очереди. После отпечатать новый день в логе.
    if (time_marks.getQueueLock()) == 0:
        time_marks.printDay()
        DropQueueTable()

    #Проверим блокировку очереди. Если блокировки нету - пишем туда
    # записи. Ну и после лочим.
    if (time_marks.getQueueLock()) == 0:
        CreateQueueTable()
        time_marks.setQueueLock(1)

    #Список получателей уже есть, можно начинать рассылку
    sendMail = SendMail()
