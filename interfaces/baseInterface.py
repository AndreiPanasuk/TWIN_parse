#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' BaseInterface
    
    Базовый класс для интефейсов
    
    Параметры инициализации:
        name    str    название интерфейса
        
'''
from utils import get_err_info, t_str

class BaseInterface(object):
    
    def __init__(self, name):
        self._name = f'{self.__class__.__name__}({name})'
        
    @property
    def name(self):
        return self._name
    
    ''' send
    
        Отправить данные 
        
    '''   
    def send(self, *args, **kargs):
        raise NotImplementedError('Метод "send" должен быть переопределен')
    
    ''' get
    
        Получить данные 
        
    '''   
    def get(self, *args, **kargs):
        raise NotImplementedError('Метод "get" должен быть переопределен')
    
    ''' log_error
    
        Логирование описания и трассировки текущей ошибки 
        
    '''   
    def log_error(self):
        txt = get_err_info()
        print(f'ERROR: {t_str()}: {self.name}:', txt)

    ''' log
    
        Логирование данных
        Параметры:
            *args - данные для логирования
    '''   
    def log(self, *args):
        print(f'{t_str()} {self.name}:', *args)
