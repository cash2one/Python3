#!/bin/bash

# Создает симлинки на стол, для самых важных gui элементов


good_vermailer_pwd=$PWD
cd "$HOME/Рабочий стол/"

#Менеждер для управления пользователями
ln -s "$good_vermailer_pwd/verse_manger.py" 'verse_manager'
#Зарубежный парсер
ln -s "$good_vermailer_pwd/eng_poetry_parser.py" 'eng_poetry_parser'
#Русскоязычный парсер
ln -s "$good_vermailer_pwd/rus_poetry_parser.py" 'rus_poetry_parser'
#Формирование списка авторов на основании таблицы poets
ln -s "$good_vermailer_pwd/authors_list.py" 'authors_list'


