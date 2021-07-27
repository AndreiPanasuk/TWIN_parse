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
    
    
    ''' close
    
        Завершение работы
        
    '''   
    def close(self):
        pass
