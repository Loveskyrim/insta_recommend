# insta_recommend
Instagram recommend system

Файл insta_parser.py запускается поредством команды 'python insta_parser.py [tag] [pages]' из терминала, где вместо [tag] ставится главный тег, по которому нужно выполнить поиск, вместо [pages] пишется число страниц для нахождения usernames. Одна страница примерно = 70 usernames.
insta_parser.py имеет зависимости:
- requests
- json
- sys
- os
Скрипт: 
1.парсит страницу с поиском постов по введенном хештегу,
2.вытаскивает username пользователей, разместивших эти пост.

Функционал трех последних пунктов приостановлен.
#3.парсит страницы полученных пользователей, выводя информацию о пользователе и подписи и количество лайков под каждым из 12 первых постов,
#4.выводит количество тегов, использованных пользователем на своих постах,
#5.выводит общее количество лайков у пользователя.


Файл lanfdetection.py запускается поредством команды 'python langdetection.py [file]' из терминала, где вместо [file] ставится имя файла, из которого читается датасет постов instagram, например из файла 1.csv читается датасет и в new_1.csv переписываются те записи, где вероятность нахождения 'en' > 0.9, и дабавляется столбаец с вероятностью нахождения 'en'. Можно импортировать функцию from langdetection import add_language и использовать как add_language('csvfile.csv').
Зависимости:
- emoji
- csv, os, sys
- langdetect

Файл location_parse.py запускается посредством команды 'python langdetection.py [file]' из терминала, где вместо [file] ставится имя файла, из которого читается датасет постов instagram, например из файла 1.csv читается датасет датасет и в new_1.csv переписываются строчки с заполненными колонками атрибутов локации.
Зависимости:
- json
- csv
- sys
- os

Файл tags.py запускается посредством команды 'python tags.py [file]' из терминала, где вместо [file] ставится имя файла с заполненными атрибутами локаций, из которого читается датасет постов instagram, например из файла 1.csv читается датасет датасет и в tags1.csv переписываются строчки с заполненными колонками owner.id, taken_at_timestamp, location.id, insta_description.
Зависимости:
- csv
- sys
- os
