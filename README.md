# thewall-py
The Wall of Messages - test job from Light IT, Python edition

Александр Малыгин, электропочта avm68@ukr.net

Проект Стена сообщений (The Wall of Messages) разработан в порядке выполнения 
тестового задания на вакансию веб-разработчик в компании Light IT.

Использованные технологии; HTML,CSS,JavaScript,Python,MySQL

Приложение испытывалось в следующих браузерах:
Internet Explorer 11
Яндекс.Браузер 17.7.1.804
Opera 47.0.2631.80

Серверная часть работала на машине разработчика под WampServer Version 3.1.0 64bit:
Apache 2.4.27 - PHP 5.6.31
MySQL 5.7.19
Python 3.6.2 (в режиме CGI)

Список файлов;
.htaccess           - здесь настройка, чтобы апач включил CGI, а также редирект по дефолту на авторизацию
thewall_auth.html   - интерфейс страницы авторизации
thewall_footer.html - конец страницы стены
thewall_header.html - начало страницы стены
thewall_input.html  - форма ввода в стене
thewall_ro.html     - сообщение о режиме read-only
auth.py             - страница авторизации
fbauth.py           - класс авторизации на Фейсбук
index.py            - главная страница (редирект на авторизацию)
show.py             - страница отображения и ввода сообщений
thewall.py          - ядро системы: класс с функциями работы с БД
thewall-full-struct.sql - скрипт для создания чистой БД с нуля в MySQL

На хостинг приложение не выложено, разрабатывалось и испытывалось локально.


Требования к установке:

1) Веб-приложение должно иметь домен thewall.avm
Это обусловлено привязкой к Facebook Application для авторизации, в настройке которого указан адрес сайта:
http://thewall.avm/

2) Настройки для апача в httpd.conf (обработка питона как CGI и вывод страниц в utf-8)

DirectoryIndex index.py
AddHandler cgi-script .py

AddDefaultCharset UTF-8
SetEnv PYTHONIOENCODING utf8

3) Python находится здесь: C:/Python36/python.exe
Была использована 32-битная версия.

4) Дополнительные библиотеки:

Пакет MySQLdb был скачан отсюда: https://pypi.python.org/pypi/mysqlclient
Установка:
pip install mysqlclient-1.3.10-cp36-cp36m-win32.whl

Пакет requests
pip install requests


Стена сообщений реализована как статическое дерево. Вся структура читается из базы и выводится 
пользователю при помощи рекурсивных функций. В задании не было явного требования, чтобы дерево 
подгружалось частями. Для нескольких сотен сообщений (и для тествовго задания) считаю это 
приемлемым (в смысле нагрузки на сервер и клиента).

Известные недостатки, которые можно было бы исправить в следующих версиях (если бы это был 
коммерческий проект):

* UserID передаётся от страницы auth в show в явном виде через параметр. 
Для отладки это очень удобно, но для реального применения является уязвимостью.
Решение: передавать вошедшего пользователя через cookies.

* Статическое дерево не контролируется никак и может быть громоздким, как для юзабилити, 
так и для сервера и браузера. Варианты решения:
1) сделать пагинацию с ограничением количества первичных сообщений (что просто) или любых 
сообщений (немного сложнее), передаваемых на клиента.
2) сделать динамическую подгрузку ветвей, при этом вначале выводятся только первичные 
сообщения или с ограничением глубины ветвей. Требует использования технологии AJAX.
3) динамическая подгрузка по принципу "бесконечного скролла" также позволила бы решить 
проблему большого дерева. Однако, с точки зрения юзабилити, infinite scroll есть зло (личное мнение).

* При попытке обновить страницу (F5) после отправки формы браузер пытается повторить отправку.
Такое поведение наблюдается на многих сайтах. Как с ним бороться, пока не знаю.

* Многострочный текст в сообщениях выводится в дереве с удвоенным интервалом. Следствие показало, 
что из БД текст приходит с разделителем "\r\n". Print выводит это как "\r\r\n", а браузеры 
воспринимают дополнительный перевод строки и отрабатывают его в теге <PRE>.
Оставлено как иллюстрация обнаруженной ошибки не по вине программы.
Кстати, PHP версия из той же базы тот же текст выводит нормально, не через строчку.
