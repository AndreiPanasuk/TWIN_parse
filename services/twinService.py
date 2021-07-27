#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .baseService import BaseService
from interfaces import JSONInterface, HTTPInterface, FileInterface

class TWINService(BaseService):
    
    def __init__(self, name, config = None):
        super().__init__(name, config = config)
        # инициализация данных результата работы
        if self._ifile.exists('output/result.json'):
            data = self._ifile.get('output/result.json')
            self._data = data[0]
        else:
            self._data = {
                "is_bot": True,
                "phrases": [],
                "replies": []
            }
        self._is_change = None  # признак модификации результата
        self._conn_error = None # признак ошибки интерфейса доступа к HTTP парсеру
        
    def init_interfaces(self, config):
        super().init_interfaces(config)
        # инициализация интерфейса доступа к JSON файлам
        name = 'files'
        fconfig = config[name]
        self._ifile = JSONInterface(name, **fconfig)
        
        # инициализация интерфейса доступа к HTTP парсеру
        name = 'parser'
        pconfig = config[name]
        self._iparser = HTTPInterface(name, **pconfig)
        
        # инициализация интерфейса записи файлов ошибок
        name = 'errors'
        econfig = config[name] 
        self._ierr = FileInterface(name, **econfig)
            
    def close_interfaces(self):
        super().close_interfaces()
        self._ifile.close()
        self._iparser.close()
        self._ierr.close()
        self._data = None
    
    ''' work
        
        Обработка входных файлов
        
    '''
    def work(self):
        self._is_change = False
        files = list(self._ifile.dir('input'))
        if files:
            files.sort()
            # Парсинг и Обработка входных файлов
            for fname in files:
                fpath = f'input/{fname}'
                try:
                    data = self._parse_file(fpath)
                    self._work_file(fpath, data)
                    self._ifile.move(fpath, f'processed/{fname}')
                except self._iparser.ConnectionError:
                    self.log_error(self._conn_error)
                    if not self._conn_error:
                        self._conn_error = True
                    break
                except:
                    self._conn_error = False
                    err_txt = self.log_error()
                    self._ifile.move(fpath, f'errors/{fname}')
                    self._ierr.send(f'{fname}.err', err_txt)
                else:
                    self._conn_error = False
        if self._is_change:
            result_fpath = 'output/result.json'
            self.log('сохранение результата', f'"{result_fpath}"')
            self._ifile.send(result_fpath, [self._data])
    
    ''' _parse_file
        
        Считать файл и установить поле "intent" для элементав, где is_bot = False
        Параметры:
            fname    str    - относительный путь к файлу
        Возврат
            list   - данные файла
        
    '''
    def _parse_file(self, fpath):
        self.log('парсинг файла', f'"{fpath}"')
        fdata = self._ifile.get(fpath)
        if fdata:
            for item in fdata:
                is_bot = item['is_bot']
                if not is_bot:
                    text = item['text']
                    resp = self._iparser.get(q = text)
                    intent = resp['intent']['name']
                    item['intent'] = intent
        return fdata
                    
    ''' _work_file
        
        Добавление данных входного файла в граф результата
        Параметры:
            fname    str    - относительный путь к файлу
            fdata    list   - данные файла
        
    '''
    def _work_file(self, fname, fdata):
        self.log('обработка файла', f'"{fname}"')
        if fdata:
            is_bot_next = True
            data = self._data
            last_ind = len(fdata) - 1
            for ind, item in enumerate(fdata):
                is_bot = item['is_bot']
                if is_bot == is_bot_next:
                    self._is_change = True
                    text = item['text']
                    if is_bot:
                        data['phrases'].append(text)
                        data = data['replies']
                    else:
                        intent = item['intent']
                        for d in data:
                            if d['intent'] == intent:
                                d['phrases'].append(text)
                                if ind < last_ind:
                                    replies = d['replies']
                                    if replies:
                                        data = d['replies'][0]
                                    else:
                                        data_next = dict(is_bot = True, phrases = [], replies = [])
                                        d['replies'] = [data_next]
                                        data = data_next
                                break
                        else:
                            d = dict(is_bot = False, intent = intent, phrases = [text], replies = [])
                            data.append(d)
                            if ind < last_ind:
                                data_next = dict(is_bot = True, phrases = [], replies = [])
                                d['replies'] = [data_next]
                                data = data_next
                    is_bot_next = not is_bot_next
