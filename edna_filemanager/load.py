# -*- coding: utf-8 -*-

'''
Модуль загрузки частей проекта и их инициализации
'''

from __builtin__ import edna_builtin

import gtk
from edna_filemanager.tools import conf
from edna_filemanager.tools import structure
from edna_filemanager.tools import icons_work
from edna_filemanager.tools import keybind
from edna_filemanager.apps import action
from edna_filemanager.root_window import Root_Window

def init_root_window():
    '''
    Иницилизация главного окна
    '''
    Edna_Window = Root_Window()
    Edna_Window.connect('destroy', edna_exit)
    Edna_Window.accel_group = gtk.AccelGroup()
    Edna_Window.add_accel_group(Edna_Window.accel_group)
    keybind.load_keys_shortcut(Edna_Window, Edna_Window.accel_group)
    Edna_Window.show_all()
    return Edna_Window

def edna_exit(*args):
    '''
    Выход
    '''
    args[0].__get_window_properties_to_configfile__()
    args[0].hide()
    gtk.main_quit()
    
def load_actions():
    '''
    Запись словарей действий
    '''
    global edna_builtin
    edna_builtin['actions'] = action.load_actions()
    
def load_structures():
    '''
    Запись словарей в общее пространство имен
    '''
    global edna_builtin
    edna_builtin['structures'] = structure.return_project_structures()
    
def load_icons_container():
    '''
    Создание контейнера иконок в общем пространстве имен
    '''
    global edna_builtin
    edna_builtin['icons container'] = icons_work.create_icons_container()
    
def load_config():
    '''
    Получение конфигураций и их запись в общее пространство имен
    '''
    global edna_builtin
    edna_builtin['config_file'] = conf.get_path_to_conf()
    config_from_file = conf.read_rc(edna_builtin['config_file'])
    edna_builtin['sequence of columns'] = conf.sequence_of_columns_function(config_from_file[0])
    edna_builtin['configuration'] = config_from_file[0]
    edna_builtin['hotkey conf'] = config_from_file[1]
