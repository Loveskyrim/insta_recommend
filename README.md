# insta_recommend
Instagram recommend system

Файл insta_parser.py запускается поредством команды 'python insta_parser.py [вид_поиска] [path_to_tags_file]' из терминала, где вместо [вид_поиска] ставится 'tag' или 'location' без кавычек, в зависимости от того, что нужно искать, вместо [path_to_tags_file] пишется путь к файлу с тегами (именами локаций). Установлен поиск по 20 первым страницам поиска. Одна страница примерно = 70 usernames.
В последнем коммите добавлена работа с прокси - адреса + порты берутся из файла 'socks4.txt' и в случае блокировки действующего соединения устанавливают новое через указанный адрес.

insta_parser.py имеет зависимости:
- requests
- fake_useragent
- json
- sys
- os
- time
- socks
- socket
- selenium.

Также в функции get_location_id(tag) необходимо указать актуальный путь к Chromedriver (некоторая версия представлена в репозитории).

Скрипт: 
1.для входного файла в формате json находит имя локации или тэга, для которого нужно произвести поиск;
2.эмулирует открытие браузера с поиском необходимого адреса страницы (в случае локации);
3.парсит страницу с поиском постов по введенному хештегу или локации;
4.вытаскивает username пользователей, разместивших эти посты.

Функционал трех последних пунктов приостановлен.
#5.парсит страницы полученных пользователей, выводя информацию о пользователе и подписи и количество лайков под каждым из 12 первых постов,
#6.выводит количество тегов, использованных пользователем на своих постах,
#7.выводит общее количество лайков у пользователя.


Файл langdetection.py запускается поредством команды 'python langdetection.py [file]' из терминала, где вместо [file] ставится имя файла, из которого читается датасет постов instagram, например из файла 1.csv читается датасет и в new_1.csv переписываются те записи, где вероятность нахождения 'en' > 0.9, и дабавляется столбаец с вероятностью нахождения 'en'. Можно импортировать функцию from langdetection import add_language и использовать как add_language('csvfile.csv').
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
