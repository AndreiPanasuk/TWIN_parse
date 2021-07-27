# -*- coding: utf-8 -*-
''' utils

    Вспомогательные функции
        
'''

import sys
import traceback
import datetime
from threading import Thread

''' get_err_info

    Получить описание и трассировку текущей ошибки в виде строки
    
    Параметры:
        only_name    bool    без трассировки
    Возврат:
        str
        
'''
def get_err_info(only_name = None):
    exc_type, exc_value, exc_traceback = sys.exc_info()
    if exc_value:
        ename = exc_type.__name__ if exc_type else ''
        if ename == 'ProgrammingError' and len(exc_value.args) > 1:
            txt = exc_value.args[1]
        else:
            try:
                txt = str(exc_value)
            except Exception as e:
                txt = 'Ошибка ???'
        if ename:
            txt = "%s: %s" % (ename, txt)
        txts = [txt]
        if not only_name:
            txts.append('TIME: %s' % datetime.datetime.now())
            txts.append("*** format_exception:")
            for itm in traceback.format_exception(exc_type, exc_value, exc_traceback):
                txts.append(str(itm))
        return '\n'.join(txts) 
    else:
        return 'Ошибка ???'

''' t_str
    
    Получить текущее время в виде строки в формате "%H:%M:%S.%f"
    
    Параметры:
        -
    Возврат:
        str
        
'''
def t_str():
    return datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]

''' make_thread
    
    Создание потока
    
    Параметры:
    args
        handler     function    - функция выполнения в потоке, 
        *args        list       - параметры функции
    kargs
        name     str     - название потока, 
        daemon   bool    - флаг "демон", 
        **kwargs dict    - ключевые параметры потока
        
    Возврат:
        threading.Thread    - созданный поток
'''
def make_thread(handler, *args, name = None, daemon = None, **kwargs):
    thread = Thread(target = handler, name = name, args=args, kwargs=kwargs)
    thread.daemon = daemon
    thread.start()
    return thread
    