#! /usr/bin/python3

#        отступы табуляцией
#        by Andrew Sotnikov aka Luca Brasi,
#        e-mail: andrew.sotnikov@zoho.com
#        --------------

from lxml import html
import requests
import pymysql
import  time

class Parse:
    def __init__(self):
        page = requests.get('http://www.russian-poetry.ru/Random.php')
        tree = html.fromstring(page.text)

        v_author=tree.xpath("/html/body/table/tr[4]/td/p[1]/b/a")
        v_name=tree.xpath("/html/body/table/tr[4]/td/p[2]/b")
        v_content=tree.xpath('/html/body/table/tr[4]/td/pre')
        label='\n------------\n'
        self.author=v_author[0].text
        self.v_name=v_name[0].text
        self.content=v_content[0].text

class DbActions(Parse):
    def __init__(self):
        Parse.__init__(self)
        self.db=pymysql.connect('localhost','andrew','andrew','verses')
        self.db.set_charset('utf8')
#        print(self.author,self.v_name, self.content)

    def getRow(self,query,row):
        # prepare a cursor object using cursor() method
        cursor = self.db.cursor()
        # execute SQL query using execute() method.
        sql = ('SELECT {0} FROM verses_list '
               'WHERE {0}=\'{1}\''.format(row,query))

        try:
            # Execute the SQL command
            cursor.execute(sql)
            # Fetch all the rows in a list of lists.
            results = cursor.fetchall()
            print(results)
        except:
            print ("Error: unable to fecth data")


    def addToDb(self):

        # prepare a cursor object using cursor() method
        cursor = self.db.cursor()
        # execute SQL query using execute() method.
        sql = ('INSERT INTO verses_list (author,verse_name,verse_content)'
        ' VALUES (\'{0}\',\'{1}\',\'{2}\')'.format(self.author,self.v_name,
                                                   self.content))

        try:
            # Execute the SQL command
            cursor.execute(sql)
            # Commit your changes in the database
            self.db.commit()
        except:
            print('Походу такой стих "{0}" уже есть '.format(self.v_name))
            # Rollback in case there is any error
            self.db.rollback()

    def closeConncetion(self):
        self.db.close()


if __name__ == "__main__":

    for x in range(1,450):
        res=Parse()
        model=DbActions()
        model.addToDb()
        model.closeConncetion()
        print('{0:<5}: Добавлен {1} --- {2}  '.format(x,model.author,
                                                      model.v_name))

        time.sleep(3)
