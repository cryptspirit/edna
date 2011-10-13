# -*- coding: utf-8 -*-

'''
Модуль реакции на действия пользвателя
'''

from __builtin__ import edna_builtin

import gtk
from edna_filemanager.widgets import question_windows

def load_actions():
    '''
    Установка действий
    '''
    Actions_dict = {'action_1': __copy_action__,
                    'action_2': __deleting_action__,
                    'action_3': __properties_file__,
                    'action_4': None,
                    'action_5': None,
                    'action_6': None,
                    'action_7': None,
                    'action_8': __show_hide_file__,
                    'action_9': __edit_path__}
                     
    return Actions_dict


def __copy_action__(accel_group, Edna_Window, keyval, modifier):
    '''
    Копирование
    '''
    panel_for_action, name_panel_for_action = Edna_Window.panel_pile.where_the_focus()
    remove_after = False
    path_to_copy = Edna_Window.panel_pile.get_path_in_panel_opponent(name_panel_for_action)
    action_file_list = panel_for_action.get_action_file_list()
    question = question_windows.Question_to_Copy(path_to_copy, action_file_list.OOF.Path, action_file_list.OOF.selection_add(), remove_after)

def __properties_file__(accel_group, Edna_Window, keyval, modifier):
    '''
    Свойства файла
    '''
    y = properties_file_window(self.OOF.Cursor_Position)

def __deleting_action__(accel_group, Edna_Window, keyval, modifier):
    '''
    Удаление файлов
    '''
    y = question_window(self.OOF.selection_add())

def __show_hide_file__(accel_group, Edna_Window, keyval, modifier):
    '''
    показать/скрыть скрытые файлы
    '''
    edna_builtin['configuration']['style']['show_hide_files'] = str(int(not int(edna_builtin['configuration']['style']['show_hide_files'])))
    self.return_panel_pile().relist_panel()
    
def __edit_path__(accel_group, Edna_Window, keyval, modifier):
    '''
    Редактировать path
    '''
    panel_for_action, name_panel_for_action = Edna_Window.panel_pile.where_the_focus()
    panel_for_action.path_panel.edit_path()