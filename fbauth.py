# -*- coding: utf-8 -*-

"""
FBAuth class

This module implements Facebook authentication API

Copyright(C) 2017 Alexander Malygin
Original PHP code author: Anton Kuliashou

"""

import urllib
import requests

class FBAuth (object):
    # Параметры авторизации
    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id     = client_id     # Идентификатор приложения на Facebook
        self.client_secret = client_secret # Секрет приложения
        self.redirect_uri  = redirect_uri  # Полный адрес страницы, получающей код для запроса авторизации
        self.user_info   = None
        self.auth_status = False

    # Собственно процесс авторизации на фейсбуке для данного приложения
    def auth(self, code):
        query = urllib.parse.urlencode(dict(
            client_id     = self.client_id,
            redirect_uri  = self.redirect_uri,
            client_secret = self.client_secret,
            code = code ))
        host = "https://graph.facebook.com/oauth/access_token?"
        r = requests.get(host+query)
        token = r.json()
        r.close()
        if token.get('access_token'):
            query = urllib.parse.urlencode(dict(
                access_token = token['access_token'],
                fields       = "id,first_name,last_name,picture.width(120).height(120)" ))
            host = "https://graph.facebook.com/me?"
            r = requests.get(host+query)
            self.user_info = r.json()
            r.close()
            if (self.user_info.get("id")):
              self.auth_status = True
              return True
        return False

    # Генерация ссылки на сервис авторизации фейсбука
    def getLink(self):
        host = "https://www.facebook.com/dialog/oauth?"
        query = urllib.parse.urlencode(dict(
            client_id     = self.client_id,
            redirect_uri  = self.redirect_uri,
            response_type = 'code' ))
        return host+query
