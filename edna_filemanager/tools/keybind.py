# -*- coding: utf-8 -*-

'''
Модуль работы с комбинациями клавиш
'''


def set_keys_shortcut(accel_group, string_of_keys_shortcut, bind_function):
    '''
    Устанавливает комбинацию клавиш и функцию для обработки события
    '''
    key, mask = gtk.accelerator_parse(string_of_keys_shortcut)
    accel_group.connect_group(key, mask, gtk.ACCEL_VISIBLE, bind_function)

def load_keys_shortcut(accel_group):
    '''
    Устанавливает обработку нажатия комбинаций клавиш по их списку и списку
    функций для обработки событий их нажатия
    '''
    

