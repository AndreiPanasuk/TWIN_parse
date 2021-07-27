#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' HTTPInterface
    
    Интефейс доступа по протоколу HTTP|HTTPS
    
    Параметры инициализации:
    args
        name    str    - название интерфейса
    kargs
        base_url     str    - базовый URL    
        encoding     str    - кодировка ответа (может принимать значение "json")
        user         str    - логин
        passw        str    - пароль
        timeout      int    - максимальное время ожидания ответа
        max_count    int    - максимальное количество перезапросов
'''
import time
import requests
from requests.compat import urljoin

class HTTPInterface(object):
    
    def __init__(self, name, base_url = None, encoding = 'UTF8', user = None, passw = None,
                 timeout = 1, max_count = 3):
        super().__init__(name)
        self._base_url = base_url
        self._encoding = encoding
        self._user = user
        self._passw = passw
        self._timeout = timeout
        self._max_count = max_count
        self._session = None
    
    ''' get
    
        GET запрос
        Параметры:
        kargs
            url    str    - относительный URL
            timeout      int    - максимальное время ожидания ответа
            encoding     str    - кодировка ответа (может принимать значение "json")
            **params    dict    - параметры запроса
            
        Возврат:
            str/dict|list    - ответ сервера
        
    '''   
    def get(self, url = None, timeout = None, encoding = None, **params):
        return self._make_req('get', url, timeout, encoding, **params)

    ''' send
    
        POST запрос
        Параметры:
        kargs
            url    str    - относительный URL
            timeout      int    - максимальное время ожидания ответа
            encoding     str    - кодировка ответа (может принимать значение "json")
            **data    dict    - данные в запросе
            
        Возврат:
            str/dict|list    - ответ сервера
    '''   
    def send(self, url = None, timeout = None, encoding = None, **data):
        return self._make_req('post', url, timeout, encoding, **data)

    ''' encode_response
    
        Декодирование ответа сервера
        Параметры:
            resp    requests.response    - ответ сервера
            encoding    str              - тип кодировки
        Возврат:
            str/dict|list    - декодированный ответ сервера
        
    '''   
    def encode_response(self, resp, encoding):
        if encoding == 'json':
            if resp.content:
                return resp.json()
        elif encoding:
            resp.encoding = encoding
            return resp.text
                        
    ''' full_url
    
        Сформировать URL с учетом базового URL
        Параметры:
            url    str    - относительный url
        Возврат:
            str    - URL с учетом базового URL
        
    '''   
    def full_url(self, url):
        if self._base_url and url:
            return urljoin(self._base_url, url)
        elif url:
            return url
        else:
            return self._base_url
        
    ''' create_session
    
        Сформировать HTTP сессию (с базовой аутентификацией)
        
    '''   
    def create_session(self):
        session = requests.Session()
        self.auth(session)
        return session 

    ''' auth
    
        Установить параметры базовой аутентификации для сессии
        Параметры:
            session     requests.Session    - сессия HTTP
        
    '''   
    def auth(self, session):
        if self._user:
            session.auth = (self._user, self._passw)
    
    def _make_req(self, method, url, timeout, encoding, **params):
        furl = self.full_url(url)
        cnt = 0
        timeout = timeout or self._timeout
        encoding = encoding or self._encoding
        while True:
            cnt += 1
            try:
                session = self.get_session()
                if method == 'get':
                    resp = session.get(furl, params = params, timeout = timeout)
                else:
                    resp = session.post(url, data = params, timeout = timeout)
                status = resp.status_code
                if status in (200, 201):
                    ret = self.encode_response(resp, encoding)
                    return ret
                else:
                    raise Exception('%s: %s (%s)' % (status, resp.reason or 'HTTP response error', self._url))
            except requests.exceptions.ConnectionError as e:
                self.close_session()
                raise e
            except Exception as e:
                if cnt >= self._max_req_count:
                    self.close_session()
                    raise e
                else:
                    time.sleep(timeout)
