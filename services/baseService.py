#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from threading import RLock
from utils import get_err_info, t_str

''' BaseService
    
    Базовый класс для сервисов
    
    Параметры инициализации:
        name      str     название сервиса
        config    dict    конфигурация системы
        
'''
class BaseService(object):
    _Lock = RLock           # класс блокировки для переменных доступных из разных потоков 
    _wait_timeout = 3       # задержка между запусками сервиса
    
    def __init__(self, name, config = None):
        self._name = f'{self.__class__.__name__}({name})'
        self._exit_lock = self._Lock()
        self._exit_flg = None
        log_level = config.get('log_level', 'NOTSET')
        self._log_err_flg = log_level in ('ERROR', 'DEBUG')
        self._log_flg = log_level in ('DEBUG',)        
        self.init_interfaces(config)
    
    def init_interfaces(self, config):
        pass
    
    def close_interfaces(self):
        pass
    
    @property
    def name(self):
        return self._name
    
    ''' exit_flg
    
        Флаг завершения работы сервиса
        
    '''   
    @property
    def exit_flg(self):
        with self._exit_lock:
            return self._exit_flg
    
    @exit_flg.setter
    def exit_flg(self, value):
        with self._exit_lock:
            self._exit_flg = value
    
    ''' run
    
        Запуск рабочего цикла сервиса
        
    '''   
    def run(self):
        while not self.exit_flg:  
            self.work()
            self.wait()
        self.close()    
    
    ''' work
    
        Рабочий метод 
        
    '''   
    def work(self):
        raise NotImplementedError('Метод "work" должен быть переопределен')
        
    ''' wait
    
        Пауза между запусками рабочего метода 
        
    '''   
    def wait(self):
        time.sleep(self._wait_timeout)
    
    ''' close
    
        Завершение работы 
        
    '''   
    def close(self):
        self.exit_flg = True
        self.close_interfaces()
    
    ''' log_error
    
        Логирование описания и трассировки текущей ошибки 
        
    '''   
    def log_error(self, only_name = None):
        txt = get_err_info(only_name = only_name)
        if self._log_err_flg:
            print(f'ERROR: {t_str()}: {self.name}:', txt)
        return txt

    ''' log
    
        Логирование данных
        Параметры:
            *args - данные для логирования
    '''   
    def log(self, *args):
        if self._log_flg:
            print(f'{t_str()} {self.name}:', *args)
