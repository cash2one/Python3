#!/usr/bin/python3

#        отступы табуляцией
#        by Andrew Sotnikov aka Luca Brasi,
#        e-mail: andruha.sota@mail.ru
#        --------------
        
#        Создает файл index_file.html

from saumysql import Crud
import collections




# Формирует HTML файл с ТОП - n атворов
class IndexFile():

    output_file='/tmp/index.html'


    def __init__(self):
        self.getTopList()
        self.makeFile()
        print('Шикарно. Сфоримирован список авторов. Найти его можно по адресу '
              '- {0}'.format(self.output_file))


    # Получает список авторов
    def getTopList(self):

        self.crud=Crud('localhost','andrew','andrew','verses')
        self.crud.sql='''SELECT lastname, name, patronymic, id FROM poets
                         ORDER BY lastname'''
        self.authors=self.crud.readAct()

    # Запускает на исполнение создание файла авторов
    def makeFile(self):

        self.f=open(self.output_file,'w')
        self.doHeader()
        self.doAuthorList()
        self.doBottomPart()
        self.doFooter()
        self.f.close()

    # Фомирует хэдер файла
    def doHeader(self):

        self.f.write('''
        <!DOCTYPE html>
        <html>
        <head>
        <meta charset="UTF-8">
        <script src="myScript.js"></script>
        <style type="text/css">
            #wrapper {width: 700px; margin-left: auto;margin-right: auto; border: 1px solid black;
            padding-left:30px}
            #header {height: 200px; margin-left:-30px; margin-bottom:40px; font-size: 24pt;color:green; font-weight: bold;
            text-align: center}
            .user_input {width: 375px} select {width: 635px}
            option {font-size: 12pt} tr {height: 35px} .btn {font-size: 12pt;
            width: 100px}
            #content {height: 680px}
            #footer  {height: 30px; font-size: 16pt; color:#CAE1FF;
            margin-left: -30px;padding: 15px 170px; text-align: center;
            background-color:#228B22}
        </style>
        </head>
        <body>
        <title>WELCOME!</title>
        <form method="POST" action="handler.php" onsubmit="return empty_form()">
        <div id="wrapper">
        <div id="header">
        GOOD VERSE MAILER
        <img src="images/header_image.jpg" alt="authors" style="margin: 5px 0px 0px 3px">
        <div style="font-size: 16pt; color:green; margin: -6px 0px 0px 0px; font-weight: normal"> poetry for everyone </div>
        </div>
        <div id="content">
        <div style="margin-bottom: 20px">
        <table>
            <tr><td width="250px">Имя: </td> <td><input type="text" class="user_input" name="name"></td> </tr>
            <tr><td>email:</td><td><input type="email" class="user_input" name="email"></td> </tr>
            <tr><td>количество в день:</td><td><input type="text" pattern="[1-9]{1}" name="qpd" class="user_input"></td> </tr>
        </table>
        </div>

        ''')


    def doBottomPart(self):

        self.f.write('''
        <div style="width: 450px; float:left; margin:10px 0px 10px 0px"><input type="radio" name="user" value="new" checked>новый пользователь</div>
        <div style="width: 200px; float:left; margin:10px 0px 10px 0px"><input type="radio" name="user" value="old">мне бы поменять :)</div>
        <div style="margin-top:60px; margin-bottom:0px"> <table><tr>
        <td width="425px"><button type="button" class="btn">Помощь</button></td>
        <td width="100px"><button type="reset" class="btn">Сборосить </button> </td>
        <td width="100px"><button type="submit" class="btn">ОК!</button></td>
        </tr></table> </div>
        </div>

        ''')

    # Формирует футер
    def doFooter(self):

        self.f.write('''

        <div id="footer">Andrew Sotnikov ^ 2016 ^ </div>
        </div>
        </form>
        </body>
        </html>
        ''')

    # Формирует таблицу с авторами. С учетом ранее полученных предпочтений
    # (сортировки и выводимых полей)
    def doAuthorList(self):

        self.f.write('''<div><select size="20" multiple  name="author[]">''')
        for row in self.authors:

            self.f.write(
                '''<option value="{1}">{0}</option>'''.format(
                    ' '.join([row[0],row[1],row[2]]),row[3]))

        self.f.write('''</select></div>''')

if __name__ == "__main__":

    obj=IndexFile()

