# -*- coding: utf-8 -*-

'''
Модуль работы с комбинациями клавиш
'''

from __builtin__ import edna_builtin

import gtk

default_rc_hotkeys = {'action_1': 'F5',
                        'action_2': 'Delete',
                        'action_3': '<Control>p',
                        'action_4': 'F2',
                        'action_5': 'F7',
                        'action_6': '<Control>F2',
                        'action_7': 'F3',
                        'action_8': '<Control>h',
                        'action_9': '<Control>l'}


def get_normal_flag_name(flag):
    '''
    Преобразование Флагов клавиш в человеческий вид
    '''
    try:
        f = flag.value_names[0]
    except:
        return None
    else:
        if f == 'GDK_SHIFT_MASK':
            return 'Shift'
        elif f == 'GDK_CONTROL_MASK':
            return 'Control'
        elif f == 'GDK_MOD1_MASK':
            return 'Alt'
        else:
            return None

def get_key_info(key_box):
    '''
    Текстовое представление названий нажатых клавиш
    '''
    k = gtk.gdk.keyval_name(key_box.keyval)
    s = get_normal_flag_name(key_box.state)
    if s:
        k = '<%s>%s' % (s, k)
    return k

def set_keys_shortcut(accel_group, string_of_keys_shortcut, bind_function):
    '''
    Устанавливает комбинацию клавиш и функцию для обработки события
    '''
    if bind_function:
        key, mask = gtk.accelerator_parse(string_of_keys_shortcut)
        accel_group.connect_group(key, mask, gtk.ACCEL_VISIBLE, bind_function)

def load_keys_shortcut(Edna_Window, accel_group):
    '''
    Устанавливает обработку нажатия комбинаций клавиш по их списку и списку
    функций для обработки событий их нажатия
    '''
    for key in edna_builtin['actions'].keys():
        set_keys_shortcut(accel_group, edna_builtin['hotkey conf'][key], edna_builtin['actions'][key])

