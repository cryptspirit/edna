# -*- coding: utf-8 -*-

'''
Работа с конфигурациями
'''

import ConfigParser
import os
from __builtin__ import edna_builtin
from edna_filemanager.tools import keybind

rc_config = {'panel_history0':'/',
            'panel_history1':'/',
            'panel_sort0':'0',
            'panel_sort1':'0'}
            
rc_style = {
            'window_maximize':'0',  
            'window_size':'295, 185',  
            'window_position':'200, 300',  
            'show_hide_files':'0',  
            'cell_name':'1',  
            'cell_type':'1', 
            'cell_size':'1', 
            'cell_datec':'0', 
            'cell_datem':'0', 
            'cell_user':'0', 
            'cell_group':'0', 
            'cell_atr':'0',
            'cell_sort':'01234567',
            'cell_name_expand':'1',  
            'cell_type_expand':'0', 
            'cell_size_expand':'0', 
            'cell_datec_expand':'0', 
            'cell_datem_expand':'0', 
            'cell_user_expand':'0', 
            'cell_group_expand':'0', 
            'cell_atr_expand':'0',
            'cell_name_alignment_h':'0.0',  
            'cell_type_alignment_h':'1.0', 
            'cell_size_alignment_h':'0.0', 
            'cell_datec_alignment_h':'0.0', 
            'cell_datem_alignment_h':'0.0', 
            'cell_user_alignment_h':'0.0', 
            'cell_group_alignment_h':'1.0', 
            'cell_atr_alignment_h':'1.0',
            'cell_name_alignment_v':'0.5',  
            'cell_type_alignment_v':'0.5', 
            'cell_size_alignment_v':'0.5', 
            'cell_datec_alignment_v':'0.5', 
            'cell_datem_alignment_v':'0.5', 
            'cell_user_alignment_v':'0.5', 
            'cell_group_alignment_v':'0.5', 
            'cell_atr_alignment_v':'0.5',
            'cell_name_size':'100',  
            'cell_type_size':'70', 
            'cell_size_size':'80', 
            'cell_datec_size':'70', 
            'cell_datem_size':'70', 
            'cell_user_size':'70', 
            'cell_group_size':'70', 
            'cell_atr_size':'70',
            'cell_datec_format':'D.M.Y',
            'cell_datem_format':'D.M.Y',
            'cell_size_format':'2',
            'cell_date_type':'0',
            'cell_atr_format':'0',
            'date_format':'0',
            'even_row_fg':'#DFDDF0',
            'even_row_bg':'#454a56',
            'odd_row_fg':'#DFDDF0',
            'odd_row_bg':'#41517a',
            'sel_row_fg':'#474747',
            'sel_row_bg':'#599839',
            'cursor_row_bg':'#0C110A',
            'cursor_row_fg':'#C0CCBC',
            'icon_size':'18',
            'font_cell_text':'Sans 10'}
            
defaultrc = {'config': rc_config, 'hotkeys': keybind.default_rc_hotkeys, 'style': rc_style}

mc = ['cell_name', 
'cell_type', 
'cell_size', 
'cell_datec', 
'cell_datem', 
'cell_user', 
'cell_group', 
'cell_atr']

def get_path_to_conf():
    '''
    Получения пути к файлу конфигураций
    '''
    filerc = os.path.join(os.getenv('XDG_CONFIG_HOME'), 'edna') 
    if os.path.isdir(filerc):
        pass
    else:
        os.makedirs(filerc)
    filerc = os.path.join(filerc, 'edna.conf')
    return filerc

def sequence_of_columns_function(rc_dict):
    '''
    Создает список с точной последовательностью столбцов в списке
    '''
    t = rc_dict['style']['cell_sort']
    p = []
    for i in xrange(len(t)):
        if rc_dict['style'][mc[int(t[i])]] == '1': p.append(mc[int(t[i])])
    return p


def read_rc(filerc):
    '''
    Функция чтения файла настроек
    '''
    rc_dict = {}
    key_name_in_rc = {}
    need_write = False
    if os.path.isfile(filerc):
        CP = ConfigParser.ConfigParser()
        CP.read(filerc)
        for i in defaultrc.keys():
            if CP.has_section(i):
                rc_dict[i] = {}
                for j in defaultrc[i].keys():
                    if CP.has_option(i, j):
                        rc_dict[i][j] = CP.get(i, j)
                    else:
                        rc_dict[i][j] = defaultrc[i][j]
                        CP.set(i, j, defaultrc[i][j])
                        need_write = True
                    if i == 'hotkeys' and len(rc_dict[i][j]) > 0: key_name_in_rc[j] = rc_dict[i][j]
            else:
                CP.add_section(i)
                need_write = True
                for j in defaultrc[i].keys():
                    CP.set(i, j, defaultrc[i][j])
                    if i == 'hotkeys': key_name_in_rc[j] = defaultrc[i][j]
                rc_dict[i] = defaultrc[i]
        if need_write:
            f = open(filerc, 'r+')
            CP.write(f)
            f.close()
    else:
        CP = ConfigParser.ConfigParser()
        for i in defaultrc.keys():
            CP.add_section(i)
            for j in defaultrc[i].keys():
                CP.set(i, j, defaultrc[i][j])
                if i == 'hotkeys': key_name_in_rc[j] = defaultrc[i][j]
        f = open(filerc, 'w')
        CP.write(f)
        f.close()
        rc_dict = defaultrc
    return rc_dict, key_name_in_rc
                
def save_rc(filerc, rc_dict):
    '''
    Функция сохранения словаря настроек
    '''
    #sequence_of_columns_function(rc_dict)
    need_write = False
    if os.path.isfile(filerc):
        CP = ConfigParser.ConfigParser()
        CP.read(filerc)
        for i in rc_dict.keys():
            if CP.has_section(i):
                for j in rc_dict[i].keys():
                    if CP.has_option(i, j):
                        if CP.get(i, j) != rc_dict[i][j]:
                            CP.set(i, j, rc_dict[i][j])
                            need_write = True
                    else:
                        CP.set(i, j, rc_dict[i][j])
                        need_write = True
            else:
                CP.add_section(i)
                need_write = True
                for j in rc_dict[i].keys():
                    CP.set(i, j, rc_dict[i][j])
        if need_write:
            f = open(filerc, 'r+')
            CP.write(f)
            f.close()
    else:
        CP = ConfigParser.ConfigParser()
        for i in rc_dict.keys():
            CP.add_section(i)
            for j in rc_dict[i].keys():
                CP.set(i, j, rc_dict[i][j])
        f = open(filerc, 'w')
        CP.write(f)
        f.close()
