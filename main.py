#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils import make_thread
from interfaces import JSONInterface
from services import TWINService

if __name__ == '__main__':
    iconfig = JSONInterface('config')
    config = iconfig.get('config.json')
    stwin = TWINService('twin', config)
    thread_twin = make_thread(stwin.run, name = 'thread_twin')
    while True:
        key = input('Введите q для завершения работы ... \n\n')
        if key in ('q', 'Q'):                        
            break
    stwin.close()
    thread_twin.join()
    print('... работа завершена')