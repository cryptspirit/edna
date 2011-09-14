# -*- coding: utf-8 -*-

'''
Модуль работы с иконками
'''

from __builtin__ import edna_builtin

import gtk
import gio

type_ico_load = gtk.ICON_LOOKUP_USE_BUILTIN

get_theme = gtk.icon_theme_get_default()
get_theme_gnome = gtk.IconTheme()
get_theme_gnome.set_custom_theme('gnome')

def icon_load_try(name, size):
    '''
    Безопасная процедура загрузки иконок
    '''
    try:
        return get_theme.load_icon(name, size, type_ico_load)
    except glib.GError:
        return get_theme_gnome.load_icon(name, size, type_ico_load)

def create_icons_container():
    '''
    Создание контейнера с иконками
    '''
    dic_icon = {}
    dic_icon['application/octet-stream'] = icon_load_try('inode-directory', int(edna_builtin['configuration']['style']['icon_size']))
    dic_icon['empty'] = icon_load_try('empty', int(edna_builtin['configuration']['style']['icon_size']))
    return dic_icon

def get_ico(s, size_ico=True):
    '''
    Получение иконки по типу и если такой тип уже есть в словаре иконок то используеться
    словарь если нет то в словарь добавляеться новая иконка
    '''
    global edna_builtin

    p = gio.content_type_get_icon(s)
    pm = p.get_names()
    if size_ico:
        try:
            edna_builtin['icons container'].keys().index(s)
        except:
            for i in pm:
                try:
                    b = icon_load_try(i, int(edna_builtin['configuration']['style']['icon_size']))
                except:
                    pass
                else:
                    edna_builtin['icons container'][s] = b
                    return edna_builtin['icons container'][s]
            if s != 'None': print s
            return edna_builtin['icons container']['empty']
        else:
            return edna_builtin['icons container'][s]
    else:
        for i in pm:
            print i
            try:
                b = icon_load_try(i, 24)
            except:
                pass
            else:
                return b
        return icon_load_try('empty', 24)
