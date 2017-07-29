#! /usr/bin/python3

#        отступы табуляцией
#        by Andrew Sotnikov aka Luca Brasi,
#        e-mail: andrew.sotnikov@zoho.com
#        --------------

#    Внешний стартер. Хорош тем что запускает приложения которые имеют X Window.
#    Работает с MySQL базой данных. Поэтому как минимум надо создать БД laucher.
#    Ну и дать нужные permissions для соответствующего юзера.


import subprocess, time, threading, saulog, os.path, os
from saumysql import Crud



# традиционный класс для логирования. Ежедневно создает файл и пишет туда все
# задания.
class Log:

    logfile = '/var/log/andrew/smart_starter.log'

    def __init__(self):


            # проверить старый ли файл лога. Если старый то молча удаляем
            f_time = os.path.getmtime(self.logfile)
            fcreated_day = time.localtime(f_time).tm_mday
            cur_day = time.localtime(time.time()).tm_mday

            if fcreated_day != cur_day:
                os.remove(self.logfile)
                f = open(self.logfile,'w')
                f.write('{0:#<120}\n{1:#^120}\n{2:#<120}\n\n\n'.format('',
                time.strftime('           %A           '),''))
                f.close()



# подготавливает талицу shdedule в БД. Если такое талицы нету - создает
class Preparing:

    def __init__(self):

        self.crud=Crud('localhost','andrew','andrew','launcher')
        #Проверить наличие shedule
        self.checkProxiesTable()

    def __del__(self):

        self.crud.closeConnection()

    #Проверяет наличие таблицы с расписанием (shedule). Если ее нет, то создает.
    #В противном случае проходит мимо
    def checkProxiesTable(self):

        self.crud.sql='SHOW TABLE STATUS LIKE \'shedule\''
        result=self.crud.readAct()

        # Таблицы нету, её прийдеться создать
        if  len(result) == 0:
            print('Нету таблицы ! Щас создадим')

            #Cоздадим таблицу time_marks
            self.crud.sql='''CREATE TABLE shedule (
                             id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
                             cmd VARCHAR(300),
                             start_hour SMALLINT,
                             end_hour SMALLINT,
                             spacing INT,
                             is_launched SMALLINT,
                             launch_time INT );'''
            result=self.crud.createAct()


        #В противном случае можно завязывать с этапом создания shedule
        else :
            print('shedule?! Походу есть такая таблица!')


# Управляет заданиями из таблицы shedule
class Task(Log):


    def __init__(self):


        Log.__init__(self)

        # стартуем через 5 минут
        time.sleep(300)
    
        self.refresh_interval = 60

        # инициализируем соединение к БД
        self.crud = Crud('localhost', 'andrew', 'andrew', 'launcher')

        # Сделать выборку из shedule
        self.crud.sql = 'SELECT * FROM shedule'
        res = self.crud.readAct()
        # создай список программ для запуска
        self.tasks = []

        self.stack = {}
        # при инициализации приложения обнулим состояние запуска, время запуска.
        # А то вдруг что подвисло
        for row in res:
            self.crud.sql = '''UPDATE shedule SET is_launched='{0}',
                               launch_time='{1}' WHERE id='{2}'
                               '''.format(0, round(time.time()-80400), int(row[0]))
            self.crud.updateAct()

            # инициализируем стек
            self.stack[row[0]] = [0,round(time.time()-86400)]


        # пока соединение нам больше не нужно
        self.crud.closeConnection()

        updateDB_thread = threading.Thread(target=self.updateDb)
        updateDB_thread.start()


        while True:

            # инициализируем соединение к БД
            self.crud = Crud('localhost', 'andrew', 'andrew', 'launcher')
            # Сделать выборку из shedule
            self.crud.sql = 'SELECT * FROM shedule'
            res = self.crud.readAct()
            # пока соединение нам больше не нужно
            self.crud.closeConnection()

            # разберемся со временем. при каждой итерации будем поддерживать
            # время в актуальном состоянии
            self.cur_time = round(time.time())  # текущее время
            self.cur_hour = time.localtime(time.time()).tm_hour  # текущий час
            # если текущий час перевалил за 12, то преобразуй его в 24. Так будет
            # проще для расчетов
            if self.cur_hour == '00':
                self.cur_hour = 24
                print('cur_hour преобразовано в 24')

            # отсылаем задачи на выполнение. Если пришло время, процесс не являеться
            # уже запущенным и прошел заданный интервал  - запускаем.
            # Иначе - втычим
            for task in res:
                self.testPossibilty(task)

            time.sleep(self.refresh_interval)
            print('\n\n\n' )



    # проверяет вохможность запуска задачи которая передаеться. Если соблюдаються
    # условия то команда запускаеться, иначе - ждемс...
    def testPossibilty(self,task):

        id = task[0]
        cmd = task[1] #команда для запуска
        #    *** запуск происходит только если текущее время находиться
        #    между earlier_hour и later_hour  ***
        earlier_hour = int(task[2]) #время начала запуска cmd, если раньше этого
        # теущее время меньше этого времени то запускать команду рано
        later_hour = int(task[3]) #время конца запуска cmd. Действует противо-
        # положно earlier_hour. Образует верхний предел времени.

        is_launched = int(task[5]) #статус запуска
        launch_time = int(task[6]) #время запуска
        # сколько времени прошло с момента последнего запуска
        elapsed =  self.cur_time - int(launch_time)
        if (self.cur_hour >= earlier_hour) and (self.cur_hour <= later_hour):
            if (is_launched == 0) and (elapsed >= task[4]):

                # print('Прошло времени {0:4}, а надо {1}'.format(elapsed, task[4]))

                self.tasks.append(threading.Thread(target=self.executeTask,
                                                       args=[cmd,id]))
                last_elem=len(self.tasks) - 1
                self.tasks[last_elem].start()

            else:

                print('приложение уже {0} запущено, прийдеться '
                      'подождать'.format(cmd))


        else:
            print('время для запуска {0} не подходящее. Нехер даже'
                  ' напрягаться.'.format(cmd))
        self.cur_time = round(time.time())



    # постоянно обновляет в БД состояние запуска и время запуска приложения
    def updateDb(self):

        interval = 5

        while True:

            crud = Crud('localhost', 'andrew', 'andrew', 'launcher')

            for key in self.stack.keys():

                crud.sql = '''UPDATE shedule SET is_launched=\'{0}\',
                        launch_time=\'{1}\' WHERE id=\'{2}\' '''.format(
                    self.stack[key][0], self.stack[key][1], key)
                crud.updateAct()
                # print(crud.sql)
                # print(time.localtime(self.stack[key][1]))


            crud.closeConnection()
            time.sleep(interval)


    # исполняет команду которая передана. Обновляет флаги состояния запуска
    # и времени запуска
    def executeTask(self, cmd, id):


        saulog.WriteLog(self.logfile, 'Процесс {0} - запущен'.format(cmd))
        self.stack[id][0] = 1
        self.stack[id][1] = round(time.time())
        subprocess.call('{0}'.format(cmd), shell=True)
        print('процесс {0} запустился!'.format(cmd))
        self.stack[id][0] = 0
        saulog.WriteLog(self.logfile, 'Процесс {0} закончил свое выполнение'.format(cmd))


if __name__ == "__main__":

    Preparing()
    Task()
