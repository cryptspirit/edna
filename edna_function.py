#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       edna_function.py
#       
#       Copyright 2011 CryptSpirit <cryptspirit@gmail.com>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
import os
import re
import ConfigParser
import time
import subprocess
import gtk
import edna_gui
import stat
import gettext
import gio
import gobject

gettext.install('edna', unicode=True)
###############################################################################
betc = {'row_fg':3,
        'row_bg':2,
        'flag':1,
        'name':0,}

filerc = '.ednarc'

md = ['Y', 
    'M', 
    'D', 
    'h', 
    'm', 
    's']

mc = ['cell_name', 
'cell_type', 
'cell_size', 
'cell_datec', 
'cell_datem', 
'cell_user', 
'cell_group', 
'cell_atr']

rc_config = {'panel_history0':'/',
            'panel_history1':'/'}
            
rc_style = {'cell_name':'1',  
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
            'icon_size':'18',
            'font_cell_text':'Sans 10'}
            
rc_hotkeys = {'key_1': 'F5',
            'key_2': 'Delete',
            'key_3': 'Ctrl p',
            'key_4': 'F2',
            'key_5': 'F7',
            'key_6': 'Ctrl F2',
            'key_7': 'F3'}
            
defaultrc = {'config': rc_config, 'hotkeys': rc_hotkeys, 'style': rc_style}

hotkeys_function_name = {'key_1': _('Copy'),
                        'key_2': _('Remove'),
                        'key_3': _('Properties'),
                        'key_4': _('Rename'),
                        'key_5': _('Make directory'),
                        'key_6': _('Open terminal'),
                        'key_7': _('View')}
############################### edna rc (begin) ###############################

def Sum_cell_function():
    '''
    Создает список с точной последовательностью столбцов в списке
    '''
    global Sum_cell
    t = rc_dict['style']['cell_sort']
    p = []
    for i in xrange(len(t)):
        if rc_dict['style'][mc[int(t[i])]] == '1':
            p.append(mc[int(t[i])])
    Sum_cell = p
    #k = rc_dict['hotkeys'].keys()

def read_rc():
    '''
    Функция чтения файла настроек
    '''
    global key_name_in_rc
    global rc_dict
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
                    if i == 'hotkeys' and len(rc_dict[i][j]) > 0: key_name_in_rc[rc_dict[i][j]] = j
            else:
                CP.add_section(i)
                need_write = True
                for j in defaultrc[i].keys():
                    CP.set(i, j, defaultrc[i][j])
                    if i == 'hotkeys': key_name_in_rc[defaultrc[i][j]] = j
                rc_dict[i] = defaultrc[i]
        if need_write:
            f = open(filerc, 'r+')
            CP.write(f)
            f.close()
        Sum_cell_function()
    else:
        CP = ConfigParser.ConfigParser()
        for i in defaultrc.keys():
            CP.add_section(i)
            for j in defaultrc[i].keys():
                CP.set(i, j, defaultrc[i][j])
                if i == 'hotkeys': key_name_in_rc[defaultrc[i][j]] = j
        f = open(filerc, 'w')
        CP.write(f)
        f.close()
        rc_dict = defaultrc
        Sum_cell_function()
                
def save_rc():
    '''
    Функция сохранения словаря настроек
    '''
    Sum_cell_function()
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
################################ edna rc (end) ################################

read_rc()
type_ico_load = gtk.ICON_LOOKUP_USE_BUILTIN
dic_icon = {}
get_theme = gtk.icon_theme_get_default()
dic_icon['application/octet-stream'] = get_theme.load_icon('inode-directory', int(rc_dict['style']['icon_size']), type_ico_load)
dic_icon['empty'] = get_theme.load_icon('empty', int(rc_dict['style']['icon_size']), type_ico_load)

########################## edna function (begin) ##############################
class Object_of_Files():
    '''
    Класс обработки списка файлов
    '''
    def __init__(self):
        pass
        
    def add_path(self, path):
        '''
        Установка пути
        '''
        self.Path = gio.File(path)
        self.Cursor_Position = None
        os.chdir(path)
        self.Select_List = []
        self.gioFile_list = map(gio.File, os.listdir(path))
        self.Model = self.create_model()
        
    def ch_path(self, gioFile):
        '''
        Смена пути
        '''
        self.Cursor_Position = self.Path
        self.Path = gioFile
        p = gioFile.get_path()
        os.chdir(p)
        self.gioFile_list = [gio.File(os.path.join(p, i)) for i in os.listdir(p)]
        self.Model = self.create_model()
        
    def gio_activation(self, gioFile_uri):
        '''
        Активация элемента списка
        '''
        gioFile = gio.File(gioFile_uri)
        if os.path.isdir(gioFile.get_path()):
            self.ch_path(gioFile)
        else:
            ret = get_launch(gioFile)
            if ret:
                ret.launch_uris([gio.File(gioFile_uri).get_uri()], None)
            print ret
        
    def clean_now(self):
        '''
        Очистка
        '''
        self.Path = None
        self.Cursor_Position = None
        self.gioFile_list = []
        self.Select_List = []
        self.Model = None
        
    def get_list_path(self):
        '''
        Получение списка файлов с описаными столбцами
        '''
        try: Sum_cell.index('cell_user') # Проверка на то есть ли среди столбцов столбец Владелец
        except: pass
        else: get_dickt_nameusers() # Если есть то получение имен пользователей
        
        try: Sum_cell.index('cell_group') # Проверка на то есть ли среди столбцов столбец Группа
        except: pass
        else: get_dickt_namegroups() # Если есть то получение названий групп
        ######################################################################
        self.len_Sum_cell = len(Sum_cell)
        self.Path_Index = self.len_Sum_cell + 1
        self.Background_Index = self.len_Sum_cell + 3
        self.Foreground_Index = self.len_Sum_cell + 2
        ######################################################################
        return_dir = []
        return_fil = []
        if self.Path.get_path() != '/':
            ttt = []
            
            ttt.append(dic_icon['application/octet-stream'])
            for j in Sum_cell:
                if j == 'cell_name':
                    ttt.append('..')
                elif j == 'cell_size':
                    ttt.append('<DIR>')
                else:
                    ttt.append('')
            ttt.append(self.gioFile_list[0].get_parent())
            
        self.Path_probe = os.path.isdir
        return_dir_append = return_dir.append
        return_fil_append = return_fil.append
        for i in self.gioFile_list:
            print i
            if self.Path_probe(i.get_path()):
                return_dir_append(get_cell(i, False))
            else:
                return_fil_append(get_cell(i, True))
        
        return_dir.sort()
        return_fil.sort()
        
        m = return_dir + return_fil
        if self.Path.get_path() != '/':
            m.insert(0, ttt)
        op = 0
        
        for i in xrange(len(m)):
            if i % 2 != 0:
                color_fg = rc_dict['style']['odd_row_fg']
                color_bg = rc_dict['style']['odd_row_bg']
            else:
                color_fg = rc_dict['style']['even_row_fg']
                color_bg = rc_dict['style']['even_row_bg']
            m[i].append(color_fg)
            m[i].append(color_bg)
        return m
        
    def create_model(self):
        self.Table_of_File = self.get_list_path()
        self.Length_Table = len(self.Table_of_File)
        model = gtk.ListStore(
                            gtk.gdk.Pixbuf, gobject.TYPE_STRING, 
                            gobject.TYPE_STRING, gobject.TYPE_STRING, 
                            gobject.TYPE_STRING, gobject.TYPE_STRING, 
                            gobject.TYPE_STRING, gobject.TYPE_STRING, 
                            gobject.TYPE_STRING, gobject.TYPE_STRING, 
                            gobject.TYPE_STRING, gobject.TYPE_STRING, 
                            gobject.TYPE_STRING, gobject.TYPE_STRING)
        
        for item in self.Table_of_File:
            iter = model.append()
            model.set(iter)
            for j in xrange(len(item)):
                model.set_value(iter, j, item[j])
        return model

def save_open(path, flg, miss):
    global answer
    answer = 0
    try: f = open(path, flg)
    except:
        f = None
        if miss:
            pass
        else:
            t = threading.Timer(1, lambda *y: tread_window(path))
            t.start()
            t.join()
            print answer
    return f, answer

def get_file_attr(file):
    '''
    Получение атрибутов файла
    '''
    s = ''
    s1 = ''
    kl = {'R':4, 'W':2, 'X':1}
    jb = os.lstat(file)[stat.ST_MODE]
    mode = stat.S_IMODE(jb)
    if stat.S_ISDIR(jb):
        s += 'd'
    else:
        s += '-'
    for i in 'USR', 'GRP', 'OTH':
        u = 0
        for j in 'R', 'W', 'X':
            if mode & getattr(stat, 'S_I%s%s' % (j, i)):
                s += j.lower()
                u += kl[j]
            else:
                s += '-'
        s1 += str(u)
    f = [s, s1]
    return f[int(rc_dict['style']['cell_atr_format'])]
    
def get_file_date(path, cm):
    '''
    Получение даты создания или даты последней модификации файла 
    '''
    b = rc_dict['style'][cm]
    ss = ''
    if cm == 'cell_datec_format':
        nm = 8
    else:
        nm = 9
    if len(b) > 0:
        s = time.localtime(os.lstat(path)[nm])
        
        for i in xrange(len(b)):
            if b[i] in md:
                t = str(s[md.index(b[i])])
                if len(t) == 1: t = '0' + t
                ss += t
            else:
                ss += b[i] 
    return ss
    
def get_file_uid(path):
    '''
    Получение индификатора владельца файла
    '''
    return get_username(str(os.lstat(path)[4]))

def get_file_gid(path):
    '''
    Получение индификатора группы владельца файла
    '''
    return get_groupname(str(os.lstat(path)[5]))

def get_username(uidd):
    '''
    Сравнение индефикатора с сушествующим списком имен пользователей
    '''
    try: dickt_nameusers.keys().index(uidd)
    except: return uidd
    else: return dickt_nameusers[uidd][0]

def get_groupname(gidd):
    '''
    Сравнение индефикатора с сушествующим списком имен групп
    '''
    try: dickt_namegroups.keys().index(gidd)
    except: return gidd
    else: return dickt_namegroups[gidd][0]

def get_file_size(path):
    '''
    Получение размера файла в байтах
    '''
    try: t = os.path.getsize(path)
    except: t = 0
    return get_in_format_size(t)

def get_mime(path_i, is_fil):
    '''
    Получение mimetype
    '''
    if is_fil:
        try:
            f = open(path_i)
            r = f.read(100)
            f.close()
        except: temp = 'empty'
        else: temp = str(gio.content_type_guess(None, r, True)[0])
    else:
        temp = str(gio.content_type_guess(path_i, None, True)[0])
    if temp:
        pass
    else:
        temp = 'empty'
    return temp
    
def get_ico(s, size_ico=True):
    '''
    Получение иконки по типу и если такой тип уже есть в словаре иконок то используеться
    словарь если нет то в словарь добавляеться новая иконка
    '''
    global dic_icon
    p = gio.content_type_get_icon(s)
    pm = p.get_names()
    if size_ico:
        try:
            dic_icon.keys().index(s)
        except:
            for i in pm:
                try:
                    b = get_theme.load_icon(i, int(rc_dict['style']['icon_size']), type_ico_load)
                except:
                    pass
                else:
                    dic_icon[s] = b
                    return dic_icon[s]
            if s != 'None': print s
            return dic_icon['empty']
        else:
            return dic_icon[s]
    else:
        for i in pm:
            print i
            try:
                b = get_theme.load_icon(i, 24, type_ico_load)
            except:
                pass
            else:
                return b
        return get_theme.load_icon('empty', 24, type_ico_load)

def get_full_size(path, no_list=False):
    '''
    Определение размера каталога
    '''
    summ = 0
    os_path_join = os.path.join
    os_path_getsize = os.path.getsize
    if no_list:
        list = []
        list_append = list.append
        list_dirs = []
        list_dirs_append = list_dirs.append
    for root, dirs, files in os.walk(path):
        for name in files:
            p = os_path_join(root, name)
            try: summ += os_path_getsize(p)
            except: pass
            if no_list: list_append([p, True])
        for name in dirs:
            p = os_path_join(root, name)
            try: summ += os_path_getsize(p)
            except: pass
            if no_list: list_dirs_append([p, False])
    if no_list:
        return summ, list_dirs + list
    else:                        
        return summ                     
    
def get_full_size_in_thread(path, text_object):
    '''
    Определение размера каталога в фоновом режиме
    '''
    summ = 0
    os_path_join = os.path.join
    os_path_getsize = os.path.getsize
    for root, dirs, files in os.walk(path):
        for name in files:
            p = os_path_join(root, name)
            try: summ += os_path_getsize(p)
            except: pass
            else:
                gtk.gdk.threads_enter()
                text_object.set_text(get_in_format_size(summ))
                gtk.gdk.threads_leave()
        for name in dirs:
            p = os_path_join(root, name)
            try: summ += os_path_getsize(p)
            except: pass
            else:
                gtk.gdk.threads_enter()
                text_object.set_text(get_in_format_size(summ))
                gtk.gdk.threads_leave()   
    gtk.gdk.threads_enter()
    text_object.set_text(get_in_format_size(summ))
    gtk.gdk.threads_leave()  

def get_launch_apps(path):
    '''
    Определяет по типу какими програмамми можно открывать файл
    '''
    mime_type = get_mime(path, True)
    print mime_type
    apps_list = gio.app_info_get_all_for_type(mime_type)
    ret_list = []
    for i in apps_list:
        ret_list.append({'app_name':i.get_name(), 'desktop':i.get_id(), 'icon':i.get_icon().get_names()[0]})
    return ret_list
    
def get_launch(gioFile):
    '''
    Определяет по типу какой программой открывать файл по умолчанию
    '''
    temp = get_mime(gioFile.get_path(), True)
    if temp != None:
        list_apps = gio.app_info_get_all_for_type(temp)
        return list_apps[0]
    else:
        return None

def get_typ(n):
    '''
    Получение расширения файла если оно есть
    '''
    type = n.rfind('.', 1)
    if type != 0 and type != -1:
        return n[:type], n[type + 1:]
    else:
        return n, ''
    
    
def deleting_files_folders(path, flag):
    '''
    Удаление папок
    '''
    if os.path.islink(path):
        os.remove(path)
    else:
        if flag:
            #try:
            os.remove(path)
            #except:
            #    print 'галяк', path
        else:
            #try:
            os.rmdir(path)
            #except:
            #    print 'галяк', path
            
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
            return 'Ctrl'
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
        k = s + ' ' + k
    return k
    
def get_in_format_size(t):
    '''
    Преобразование размера файла в байтах в формат указаный в настройках
    '''
    s = ''
    if rc_dict['style']['cell_size_format'] == '0':
        t = str(t)
        if len(t) > 3:
            l = len(t)
            for i in xrange(l):
                s += t[i]
                if (l - i - 1) % 3 == 0 and i != l - 1:
                    s += ' '
        else:
            s = t
    elif rc_dict['style']['cell_size_format'] == '1':
        if t < 1024:
            s = str(t) + ' B'
        elif t >= 1024 and t <= 1048576:
            s = str(round(t / 1024., 2)) + ' kB'
        else:
            s = str(round(t / 1048576., 2)) + ' MB'
    elif rc_dict['style']['cell_size_format'] == '2':
        if t < 1024:
            s = str(t) + ' B'
        elif t >= 1024 and t <= 1048576:
            s = str(round(t / 1024., 2)) + ' kB'
        elif t >= 1048576 and t <= 1073741824:
            s = str(round(t / 1048576., 2)) + ' MB'
        else:
            s = str(round(t / 1073741824., 2)) + ' GB'
    return s
    
def get_dickt_nameusers():
    '''
    Получение списка имен пользователей по их индефикатору
    '''
    global dickt_nameusers
    f = open('/etc/passwd','r')
    r = f.readlines()
    f.close()
    dickt_nameusers = {}
    for i in r:
        y = i.split(':')
        dickt_nameusers[y[2]] = y
        
def get_dickt_namegroups():
    '''
    Получение списка названий групп по их индефикатору
    '''
    global dickt_namegroups
    f = open('/etc/group','r')
    r = f.readlines()
    f.close()
    dickt_namegroups = {}
    for i in r:
        y = i.split(':')
        dickt_namegroups[y[2]] = y
    
def get_cell(gioFile, is_fil):
    '''
    Получение строки для списка файлов
    '''
    ret = []
    temp = get_mime(gioFile.get_path(), is_fil)
    ret.append(get_ico(temp))
    t = ''
    n = gioFile.get_basename()
    if is_fil:
        n, t = get_typ(gioFile.get_basename())
    for j in Sum_cell:
        if j == 'cell_name':
            if is_fil:
                ret.append(n)
            else:
                ret.append(gioFile.get_basename())
        elif j == 'cell_type':
            ret.append(t)
        elif j == 'cell_size':
            if is_fil:
                ret.append(get_file_size(gioFile.get_path()))
            else:
                ret.append('<DIR>')
        elif j == 'cell_datec':
                ret.append(get_file_date(gioFile.get_path(), 'cell_datec_format'))
        elif j == 'cell_datem':
                ret.append(get_file_date(gioFile.get_path(), 'cell_datem_format'))
        elif j == 'cell_user':
                ret.append(get_file_uid(gioFile.get_path()))
        elif j == 'cell_group':
                ret.append(get_file_gid(gioFile.get_path()))
        elif j == 'cell_atr':
                ret.append(get_file_attr(gioFile.get_path()))
    ret.append(gioFile.get_uri())
    return ret
########################### edna function (end) ###############################        

def main():
    path = '/home/mort'
    p = Get_gioFile_list(path)
    print p
    #OOF = Object_of_Files()
    #print OOF.add_path(path)

if __name__ == '__main__':
    main()

