#! /usr/bin/python3

#        отступы пробелами
#        by Andrew Sotnikov aka Luca Brasi,
#        e-mail: andruha.sota@mail.ru
#        --------------

from lxml import html
import requests, time
from saumysql import Crud
from subprocess import call



class Preparing:

    def __init__(self):

        crud=Crud('localhost','andrew','andrew','proxy')
        #Проверить наличие time_marks
        self.checkProxiesTable()

    def __del__(self):

        self.crud.closeConnection()

    #Проверяет наличие таблицы proxies. Если ее нет, то создает.
    #В противном случае проходит мимо
    def checkProxiesTable(self):

        self.crud=Crud('localhost','andrew','andrew','proxy')
        self.crud.sql='SHOW TABLE STATUS LIKE \'proxies\''
        result=self.crud.readAct()

        # Таблицы нету, её прийдеться создать
        if  len(result) == 0:
            print('Нету таблицы временных меток! Щас создадим')
            #Cоздадим таблицу time_marks
            self.crud.sql='''CREATE TABLE proxies (
                             id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
                             ip_address VARCHAR(20),
                             port SMALLINT, 
                             time INT, 
                             UNIQUE (ip_address));'''
            result=self.crud.createAct()


        #В противном случае можно завязывать с этапом создания time_marks
        else :
            print('proxies?! Походу есть такая таблица!')



class GetProxy:
    def __init__(self):
    
    
        URL='http://hideme.ru/proxy-list/?country=CNCZFRINPLRUESTRUAGB&ports=8080,80&type=hs#list'
        headers = {
           'User-Agent': 'Lynx/2.8.8pre.4 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/2.12.23' }    
#        page = requests.get('http://hideme.ru/proxy-list/?country=RUGBUS#list', headers=headers)
        page = requests.get(URL, headers=headers)
        tree = html.fromstring(page.text)


        ip_addresses = tree.xpath("//*[@id='content-section']/section[1]/div/table/tbody/tr/td[1]")
        ports = tree.xpath("//*[@id='content-section']/section[1]/div/table/tbody/tr/td[2]")

        for ip_address, port in zip(ip_addresses,ports):
            
            ip_address = ip_address.text
            port = port.text
            print('ip_address: {0:20}; port: {1}'.format(ip_address, port))
            proxyObj = ProxyAct(ip_address,port)
            proxyObj.addProxy()
            
class ProxyAct:

    def __init__(self,ip_address,port):
    
        self.ip_address = ip_address
        self.port = port
        
    def checkProxy(self):
    
        timeout = 10
        result = call('curl --connect-timeout {0} -x {1}:{2} http://google.com'.format(
                        timeout, self.ip_address, self.port), shell=True)

        if result == 0:
            print('Всё путем! IP: {0:16} - хороший'.format(self.ip_address))

            return 0
        else:
            print('Плохо, не подошел')
            
    def addProxy(self):
        
        if (self.checkProxy()) == 0:
            self.crud=Crud('localhost','andrew','andrew','proxy')
            self.crud.sql=('''INSERT INTO proxies (ip_address, port, time)
                             VALUES ('{0}', '{1}', '{2}')'''.format(self.ip_address,
                             self.port, round(time.time())))
            self.crud.createAct()
            self.crud.closeConnection()
            

        
        
    



if __name__ == "__main__":

    Preparing()
    GetProxy()

