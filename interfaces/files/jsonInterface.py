#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' JSONInterface
    
    Интефейс доступа к JSON файлам
    
    Параметры инициализации:
    args
        name    str    - название интерфейса
    kargs
        ident    int    - отступ при записи
        base_path str    - базовый каталог
        encoding    str    - кодировка
'''
import json
import codecs
from .fileInterface import FileInterface

class JSONInterface(FileInterface):

    def __init__(self, *args, ident = 4, **kargs):
        super().__init__(*args, **kargs)
        self._ident = ident
    
    ''' get
    
        Чтение JSON файла
        Параметры:
            fname    str    - относительный путь к файлу
        Возврат:
            dict/list    - содержимое файла преобразованное
        
    '''   
    def get(self, fname):
        fpath = self.full_path(fname)
        with open(fpath, 'r', encoding = self._encoding) as fp:
            return json.load(fp)

    ''' send
    
        Запись файла
        Параметры:
            fname    str    - относительный путь к файлу
            data    str    - данные (содержимое файла)
    '''   
    def send(self, fname, data):
        fpath = self.full_path(fname)
        with open(fpath, 'wb') as fp:
            json.dump(data, codecs.getwriter(self._encoding)(fp), ensure_ascii = False, indent = self._ident)
    
