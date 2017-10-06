# -*- coding: utf-8 -*-
"""
 * Модель для проекта Стена сообщений (The Wall of Messages)
 * Проект разработан в порядке выполнения тестового задания на вакансию веб-разработчик в компании Light IT
 *
 * Copyright (C) 2017 Alexander Malygin
 *
"""

import MySQLdb

# В классе TheWall реализована логика взаимодействия приложения с БД и построения дерева сообщений.

class TheWall (object):
    def __init__(self):
        self.db = MySQLdb.connect(user='root', db='thewall', charset='utf8')

#  Добавление пользователя в БД, на основе информации из соцсети
#  Если такой уже есть, обновляется его имя
#  Возврат ID пользователя в таблице User
    def updateUser(self, sid, name):
        cur = self.db.cursor()
        cur.execute("SELECT ID,Name FROM User WHERE SocID=%s", (sid,))
        row = cur.fetchone()
        if row is None:
            cur.execute("INSERT INTO User (SocID, Name) VALUES (%s, %s)", (sid, name))
            return self.db.insert_id()
        else:
            if row[1] != name:
                cur.execute("UPDATE User SET Name=%s WHERE ID=%s", (name, row[0]))
            return row[0];

# Получение имени пользователя по его ID
    def getUserName(self, uid):
        cur = self.db.cursor()
        cur.execute("SELECT Name FROM User WHERE ID=%s", (uid,))
        row = cur.fetchone()
        if row is None: return None
        else: return row[0]

# Построение иерархической структуры списка сообщений в виде вложеннывх массивов
# Одна запись содержит значения id,parentid,userid,createstamp,name,text из текущей выборки
# и массив comments из рекурсивного вызова функции
    def buildTree(self, pid=None):
        cur = self.db.cursor()
        # первичные сообщения (parentid is null) выводятся в обратном порядке, комментарии в хронологическом
        sql = ("SELECT m.id,m.parentid,m.userid,m.createstamp,u.name,m.text FROM message as m, user as u WHERE m.userid=u.id AND m.parentid "
            + ("is null ORDER BY ID DESC" if pid is None else "= %s ORDER BY CreateStamp" % (pid,)))
        cur.execute(sql)
        result = []
        try:
          for row in cur:
              result.append(dict(
                  id   = row[0],
                  pid  = row[1],
                  uid  = row[2],
                  dt   = row[3],
                  name = row[4],
                  text = row[5],
                  comments = self.buildTree(row[0])
              ));
        finally:
          cur.close()
        return result

# Добавление нового сообщения
# Возврат ID новой записи в таблице Message
    def addMessage(self, id, uid, txt):
        cur = self.db.cursor()
        if id is None: id='null'
        cur.execute("INSERT INTO message (parentid, userid, text) VALUES ({0}, {1}, '{2}')".format(id, uid, txt))
        return self.db.insert_id()
