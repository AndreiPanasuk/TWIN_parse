#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' FileInterface
    
    Интефейс доступа к файлам
    
    Параметры инициализации:
    args
        name    str    - название интерфейса
    kargs
        base_path str    - базовый каталог    
        encoding    str    - кодировка
        
'''
import os

class FileInterface(object):
    
    def __init__(self, name, base_path = None, encoding = 'UTF8'):
        super().__init__(name)
        self._base_path = os.path.normpath(base_path)
        self._encoding = encoding
    
    ''' get
    
        Чтение файла
        Параметры:
            fname    str    - относительный путь к файлу
        Возврат:
            str    - содержимое файла
        
    '''   
    def get(self, fname):
        fpath = self.full_path(fname)
        with open(fpath, 'r', encoding = self._encoding) as fp:
            return fp.read()

    ''' send
    
        Запись файла
        Параметры:
            fname    str    - относительный путь к файлу
            data    str    - данные (содержимое файла)
    '''   
    def send(self, fname, data):
        fpath = self.full_path(fname)
        with open(fpath, 'w') as fp:
            fp.write(data)
    
    ''' full_path
    
        Сформировать путь к файлу с учетом базового каталога
        Параметры:
            fname    str    - относительный путь к файлу
        Возврат:
            str    - путь к файлу с учетом базового каталога
        
    '''   
    def full_path(self, fname):
        fname = os.path.normpath(fname)
        if self._base_path:
            return os.path.join(self._base_path, fname)
        else:
            return fname
        
    ''' dir
    
        Итератор имен файлов в каталоге
        Параметры:
            path    str    - относительный путь к каталогу
        
    '''   
    def dir(self, path):
        fpath = self.full_path(path)
        for _, _, files in os.walk(fpath):
            for fname in files:
                yield fname