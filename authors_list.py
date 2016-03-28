#!/usr/bin/python3

#        отступы табуляцией
#        by Andrew Sotnikov aka Luca Brasi,
#        e-mail: andruha.sota@mail.ru
#        --------------

        # Формирует список авторов в правильном порядке. После пишет их в
        # файл output_file.


from saumysql import Crud

output_file='/tmp/authorslist'


# Ставит фамилию из начала строки в конец.
# Например, получает строку формата Александр Сергеевич Пушкин.
# Возвращает   Пушкин Александр Сергеевич.
def formatAuthors(string):

    string=string[0]
    names=string.split(' ')
    names_number=len(names)
    if names_number == 1:

        author=string

    elif names_number >= 2:

        lastname=names[names_number-1]
        author=[lastname]
        for x in names:
            if x != lastname:
                author.append(x)
        author=' '.join(author)

        return author

#Получение списка авторов из БД
crud=Crud('localhost','andrew','andrew','verses')
crud.sql='SELECT DISTINCT author FROM verses_list'
list=crud.readAct()

authors_list=[]

# Пошел процесс преобразования фамилий
for elem in list:

    author=formatAuthors(elem)
    authors_list.append(author)

authors_list.sort()

# Процесс записи в файл
f=open(output_file,'w')
i=1
for author in authors_list:
    f.write('{0:<6}{1}\n'.format(i,author))
    i=i+1

f.close()
