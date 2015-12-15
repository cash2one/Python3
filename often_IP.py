#! /usr/bin/python

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import subprocess, time


class humanPrint:  
    
#    Возвращает табулируемую строку.
#    lOffset-количество пробелов в качестве отступа от начала, list-список строк
#    который нужно разложить по колонкам, colWidth - ширина колонки.

    def tabulatedString(self,lOffset,list,colWidth):
        string=''
        lineLenght=0
        for elem in list:
            string=string+' :'
            lineLenght=lineLenght+colWidth
            offset=' '*lOffset
            string=string+offset+elem
            string=string.ljust(lineLenght)
        string=string+' :'
        return string



if __name__ == "__main__":
    
#   Получает текщий IP адресс и возвращает его в виде строки
    def getIP():
        ifconfig=subprocess.check_output("ifconfig | grep 'inet addr:'", shell=True,  universal_newlines=True)
        ifconfig=ifconfig.split('\n')
        ifconfig=ifconfig[1].split('P-t-P:')
        stringIP=ifconfig[0]; stringIP=stringIP.split('inet addr:')
        currIP=stringIP[1].strip()
        return currIP

    print (getIP())
    
#    previousIP=getIP()
#    
#    while True:
#        time.sleep(60)
#        currIP=getIP()
#        if previousIP == currIP:
#            
#            previousIP = currIP
#    
   
    a = humanPrint()
    for x in range(10):
        print(a.tabulatedString(5, ['22', '44', '66', '88'], 14))