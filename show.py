#!C:/Python36/python.exe
# coding: utf8

"""
 * Страница сообщений для проекта Стена сообщений (The Wall of Messages)
 * Проект разработан в порядке выполнения тестового задания на вакансию веб-разработчик в компании Light IT
 *
 * Copyright (C) 2017 Alexander Malygin
 *
"""
import cgi
from thewall import *

print("Content-type: text/html;charset=utf-8\n")
with open('thewall_header.html') as f: print(f.read())

tw = TheWall()
form = cgi.FieldStorage()   # параметры запроса
uid = form.getvalue('uid')  # ID пользователя в базе, параметр передаётся при переходе со страницы авторизации
uname = tw.getUserName(uid) # Имя пользователя, если он задан и есть в базе
if uname is None: uid=None  # Если нет такого - играем без пользователя

if uid is None: # режим только для чтения

    with open('thewall_ro.html') as f: print(f.read())

else:           # режим с возможностью добавления сообщений

    txt = form.getvalue('msgtext') # текст нового сообщения
    pid = form.getvalue('msgpid')  # в таблице это null для первичных сообщений, ParentID для комментариев
    mid = tw.addMessage(pid, uid, txt) if txt else '' # свежее сообщение добавлено в базу

    with open('thewall_input.html') as f: print(f.read() % (uname, mid))

print("<hr width=100%>")

# собственно вывод иерархической структуры сообщений, данной нам в ощущения
def showTree(tree, level=0):

    if level: print("<ul>") # первый уровень - без отступа
    for row in tree:        # цикл по детям узла

      id  = row['id']
      cap = "#{0} {1} <b>{2}</b>".format(id, row['dt'], row['name']) # метка для сообщения и для редактора при ответе
      com = row['comments']                 # массив комментариев
      # разные маркеры для разных случаев
      if level: liclass = "cmnt"            # комментарий
      else: 
        if len(com): liclass = "msg1"       # первичное сообщение, есть комментарии
        else: liclass = "msg0"              # первичное сообщение, нет комментариев

      print("<a name=%s></a>" % (id))      # якорь для сообщения
      print("<li class=%s>%s" % (liclass, cap))
      print("<p><pre>%s</pre>" % (row['text'],))   # текст сообщения
      # кнопка ответа, переход к редактору
      if uid: print("<button name='answer' value={0} title='Comment this message' onClick=\"goAnswer({0}, '{1}')\">Comment</button>".format(id, cap))
      print("</p></li>")
      if len(com): showTree(com, level+1)   # всё то же самое для детей данного узла

    if level: print("</ul>")

# построение дерева из БД, параметр работает, но пока не актуален (в данной версии)
tree = tw.buildTree(form.getvalue('id'))
# вывод дерева
showTree(tree)

with open('thewall_footer.html') as f: print(f.read())
