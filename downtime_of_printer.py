#! /usr/bin/python

#        отступы табуляцией
#        by Andrew Sotnikov aka Luca Brasi,
#        e-mail: andruha.sota@mail.ru
#        --------------

import os,re, time
from subprocess import *



# Открывает исходный файл и возващает его в реверсированном порядке.
# Принимает аргументы: filename - путь к файлу, replace=True - заменит
# исходный файл на реверсированный.

class ReverseFile:
    def __init__(self,filename,replace=False):
        self.doJobList()
        f1=open(filename)
        f2=open(filename+'_tmp','w')
        ls=[]
        for x in f1:
            ls.append(x)
        ls=reversed(ls)
        for x in ls:
            f2.write(x)

        f1.close()
        f2.close()
        if replace==True:
            os.remove(filename)
            os.rename((filename+'_tmp'),filename)

    def doJobList(self):
        os.chdir('/tmp/')
        call('lpstat -W completed > 1', shell=True)

class getInfo():

    year={'Янв':31,'Фев':28,'Мар':31,
          'Апр':30,'Май':31,'Июн':30,
          'Июл':31,'Авг':31,'Сен':30,
          'Окт':31,'Ноя':30,'Дек':31}

    month=('Янв','Фев','Мар','Апр','Май','Июн',
           'Июл','Авг','Сен','Окт','Ноя','Дек')

    # Вызывает lpstat -d и парсит вывод.
    # Возвращает дефолтный имя дефолтного принтера.
    def getDefPrinter(self):
        pattern=check_output(['lpstat -d'],shell=True);pattern=str(pattern)
        res=re.search(r'(?<=destination:\s).+?(?=\\n)',pattern)
        printer=res.group(0)
        print('Твой дефолтный принтер - {0}'.format(printer))
        return printer


    def getPrLastDate(self):
        printer=self.getDefPrinter()
        f2=open('/tmp/1')
        for x in f2:
            if (re.search(printer,x)) != None:
                print(x)
                break
        date=self.parseDate(x)
        self.getDifference(date)

        f2.close()

    # Получает строку формата:
    # Canon_E464-114 andrew  18432 Пнд 01 Фев 2016 21:06:54
    # Парсит string и возврщает список date, такого формата:
    # ('01', 'Фев', '2016')

    def parseDate(self,string):
        # date=re.search(r'.{11}\s(?=\d{2}:\d{2}:\d{2})',string)
        date=re.search(r'.(\d{2})\s(.{3})\s(\d{4})\s(?=\d{2}:\d{2}:\d{2})',
                       string)
        date=date.group(1,2,3)
        print(date)
        return date

    # Получает количество дней с момента последнего запуска принтера и
    # возвращает это значение.
    def getDifference(self,date):

        # Начало получения количества дней с момента последнего запуска
        d_from_last=0
        for x in self.month:
            if date[1] in x:
                d_from_last=d_from_last+int(date[0])
                break
            d_from_last=d_from_last+self.year[x]
        # Конец получения количества дней с момента последнего запуска

        doy=int(time.strftime('%j',time.gmtime()))
        year=int(time.strftime('%Y',time.gmtime()))
        if (int(date[2])) != year:
            doy=doy+365
        days_difference=doy-d_from_last
        print('Печать не проводилась {0} дней'.format(days_difference))

        return days_difference

if __name__ == "__main__":
    a=ReverseFile('/tmp/1',replace=True)
    b=getInfo()
    b.getPrLastDate()
