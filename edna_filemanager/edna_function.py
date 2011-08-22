# -*- coding: utf-8 -*-


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
import glib
import getpass

gettext.install('edna', unicode=True)
###############################################################################
betc = {'row_fg':3,
        'row_bg':2,
        'flag':1,
        'name':0,}

filerc = os.path.join(os.getenv('XDG_CONFIG_HOME'), 'edna') 
if os.path.isdir(filerc):
    pass
else:
    os.makedirs(filerc)
filerc = os.path.join(filerc, 'edna.conf')

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
            
rc_hotkeys = {'key_1': 'F5',
            'key_2': 'Delete',
            'key_3': 'Ctrl p',
            'key_4': 'F2',
            'key_5': 'F7',
            'key_6': 'Ctrl F2',
            'key_7': 'F3',
            'key_8': 'Ctrl h'}
            
defaultrc = {'config': rc_config, 'hotkeys': rc_hotkeys, 'style': rc_style}

hotkeys_function_name = {'key_1': _('Copy'),
                        'key_2': _('Remove'),
                        'key_3': _('Properties'),
                        'key_4': _('Rename'),
                        'key_5': _('Make directory'),
                        'key_6': _('Open terminal'),
                        'key_7': _('View'),
                        'key_8': _('Show hide files')}
                        
keys_not_follow = ['Shift Shift_L', 'Shift Shift_R', 'Alt Alt_L', 'Alt Alt_R', 'Escape',
                    'Return', 'Ctrl Control_L', 'Ctrl Control_R', 'Caps_Lock',
                    'Alt ISO_Prev_Group', 'Alt ISO_Next_Group', 'Ctrl Shift_R',
                    'Ctrl Shift_L', 'Shift Control_R', 'Shift Control_L', 'Shift_L',
                    'Shift_R', 'Alt_R', 'Alt_L', 'Control_R', 'Control_L', 'Tab', 
                    'Left', 'Up', 'Right', 'Down', 'minus', 'equal', 'Shift plus',
                    'Home', 'End', 'Page_Up', 'Page_Down', 'space',
                    'Menu', 'grave', 'Insert', 'semicolon', 'comma', 'period',
                    'slash', 'backslash', 'BackSpace']
keys_not_follow += map(str, xrange(10))
keys_not_follow += map(chr, xrange(65, 123))
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

dic_icon['application/octet-stream'] = icon_load_try('inode-directory', int(rc_dict['style']['icon_size']))
dic_icon['empty'] = icon_load_try('empty', int(rc_dict['style']['icon_size']))

#dic_icon['empty'] = get_theme.load_icon('empty', int(rc_dict['style']['icon_size']), type_ico_load)
########################## edna function (begin) ##############################
class Panel_Pile():
    '''
    Класс обработки панелей
    '''
    def __init__(self):
        self.Panel_Box = {}
        
    def add_panel(self, Panel_Object, Panel_Name):
        '''
        Добавление панели
        '''
        self.Panel_Box[Panel_Name] = Panel_Object
        
    def __find_name_panel_opponent(self, Panel_Name):
        '''
        Поиск имени панели оппонента
        '''
        for i in self.Panel_Box.keys():
            # Элементарный поиск панели оппонента в будующем необходимо заменить на более изящний
            if i != Panel_Name:
                return i
        
    def get_panel(self, Panel_Name):
        '''
        Возвращает панели по имени
        '''
        return self.Panel_Box[Panel_Name]
        
    def get_path_in_panel_opponent(self, Panel_Name):
        '''
        Возвращает путь в панели оппонента
        '''
        return self.Panel_Box[self.__find_name_panel_opponent(Panel_Name)].treeview.OOF.Path
    
    def relist_panel(self):
        '''
        Переопрашивает списки панелей
        '''
        for i in self.Panel_Box.keys():
            self.Panel_Box[i].treeview.refresh_cells()
    
    def get_panel_opponent(self, Panel_Name):
        '''
        Возвращает соседнюю панель
        '''
        return self.Panel_Box[self.__find_name_panel_opponent(Panel_Name)]
    
class Object_of_Files():
    '''
    Класс обработки списка файлов
    '''
    
    def __init__(self, number_of_panel, update_model=None):
        self.return_update_model = update_model
        self.number_of_panel = number_of_panel
        
    def __gen_listdir__(self, path):
        """
        Генерация списка файлов
        """
        show_hide_files = int(rc_dict['style']['show_hide_files'])
        if show_hide_files:
            return map(gio.File, os.listdir(path))
        else:
            return [gio.File(i) for i in os.listdir(path) if i[0] != '.']
        
    def add_path(self, path):
        '''
        Установка пути
        '''
        self.Path = gio.File(path)
        self.Cursor_Position = None
        self.Table_of_File = []
        os.chdir(path)
        self.Select_List = []
        self.gioFile_list = self.gioFile_list = self.__gen_listdir__(path)
        self.get_list_path()
        self.Model = self.create_model()
        self.Monitor_rootdir = None
        self.Monitor_rootdir = self.Path.monitor_directory(gio.FILE_MONITOR_NONE, None)
        self.Monitor_rootdir.connect('changed', self.event_change_in_rootdir)
        
    def selection(self, gioFile_uri):
        '''
        Действие с выделения элементов списка
        '''
        try: self.Select_List.index(gioFile_uri)
        except: self.Select_List.append(gioFile_uri)
        else: self.Select_List.remove(gioFile_uri)
    
    def selection_add(self):
        sel_list = [[i, os.path.isfile(gio.File(i).get_path())] for i in self.Select_List]
        if self.now_in_selection(self.Cursor_Position.get_uri()) == False:
                sel_list.append([self.Cursor_Position.get_uri(), os.path.isfile(self.Cursor_Position.get_path())])
        return sel_list
    
    def now_in_selection(self, gioFile_uri):
        '''
        Проверка состоит ли запрашиваемый элемент в списке выделеных элементов
        '''
        try: self.Select_List.index(gioFile_uri)
        except: return False
        else: return True
    
    def ch_path(self, gioFile):
        '''
        Смена пути
        '''
        self.Cursor_Position = self.Path
        self.Path = gioFile
        p = gioFile.get_path()
        os.chdir(p)
        self.gioFile_list = self.__gen_listdir__(p)
        self.get_list_path()
        self.Model = self.create_model()
        self.Monitor_rootdir = self.Path.monitor_directory(gio.FILE_MONITOR_NONE, None)
        self.Monitor_rootdir.connect('changed', self.event_change_in_rootdir)
        
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
        self.Monitor = []
        self.Monitor_rootdir = None
        
    def event_change_in_rootdir(self, monitor, file1, file2, evt_type):
        '''
        Обработка событий происходящих с отображаемой папкой
        '''
        if evt_type == gio.FILE_MONITOR_EVENT_DELETED:
            #print 'Удаление', file1
            for i in xrange(len(self.Table_of_File)):
                if file1.get_uri() == self.Table_of_File[i][self.Path_Index]:
                    #self.gioFile_list.pop(i)
                    self.Table_of_File.pop(i)
                    #self.Model = self.create_model()
                    if self.return_update_model: self.return_update_model(file1.get_uri(), 0)
                    return
        elif evt_type == gio.FILE_MONITOR_EVENT_CHANGED:
            #print 'Изменение', file1
            for i in xrange(len(self.Table_of_File)):
                if file1.get_uri() == self.Table_of_File[i][self.Path_Index]:
                    new_row = self.get_row_path(file1)
                    for j in xrange(len(self.Table_of_File[i]) - 1):
                        self.Table_of_File[i][j] = new_row[j]
                    #self.Model = self.create_model()
                    if self.return_update_model: self.return_update_model(file1.get_uri(), 1, new_row)
                    return
        elif evt_type == gio.FILE_MONITOR_EVENT_CREATED:
            #print 'Создание', file1
            new_row = self.get_row_path(file1)
            new_row.append(rc_dict['style']['even_row_fg'])
            self.Table_of_File.append(new_row)
            if self.return_update_model: self.return_update_model(file1.get_uri(), 2, new_row)
            return
    
    def changed_event(self, monitor, file1, file2, evt_type):
        '''
        Обработка событий происходящих с файлами
        '''
        if (evt_type in (gio.FILE_MONITOR_EVENT_CREATED,
           gio.FILE_MONITOR_EVENT_DELETED)):
           print "Changed_file1:", file1
           print "Changed_file2:", file2
           print "Changed_evt_type:", evt_type
           if evt_type == gio.FILE_MONITOR_EVENT_DELETED: print 'jjjjjj'
        
    def get_row_path(self, gioFile):
        '''
        Получение строки файла с описаными столбцами
        '''
        ret = get_cell(gioFile, os.path.isfile(gioFile.get_path()))
        return ret
        
    def get_list_path(self):
        '''
        Получение списка файлов с описаными столбцами
        '''
        self.Monitor = []
        try: Sum_cell.index('cell_user') # Проверка на то есть ли среди столбцов столбец Владелец
        except: pass
        else: get_dickt_nameusers() # Если есть то получение имен пользователей
        
        try: Sum_cell.index('cell_group') # Проверка на то есть ли среди столбцов столбец Группа
        except: pass
        else: get_dickt_namegroups() # Если есть то получение названий групп
        ######################################################################
        self.len_Sum_cell = len(Sum_cell)
        self.Path_Index = self.len_Sum_cell + 1
        self.Sort_Index = self.len_Sum_cell + 2
        self.Foreground_Index = self.len_Sum_cell + 3
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
            pr = self.Path.get_parent()
            #self.Monitor.append(pr.monitor_file(gio.FILE_MONITOR_NONE, None))
            #self.Monitor[len(self.Monitor) - 1].connect("changed", self.changed_event)
            ttt.append(pr.get_uri())
            ttt.append('0')
            
        self.Path_probe = os.path.isdir
        return_dir_append = return_dir.append
        return_fil_append = return_fil.append
        for i in self.gioFile_list:
            #self.Monitor.append(i.monitor_file(gio.FILE_MONITOR_NONE, None))
            #self.Monitor[len(self.Monitor) - 1].connect("changed", self.changed_event)
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
            m[i].append(rc_dict['style']['even_row_fg'])
        self.Table_of_File = m
        
    def create_model(self):
        model = gtk.ListStore(
                            gtk.gdk.Pixbuf, str, 
                            str, str, 
                            str, str, 
                            str, str, 
                            str, str, 
                            str, str, 
                            str, str)
    
        for item in self.Table_of_File:
            iter = model.append()
            model.set(iter)
            for j in xrange(len(item)):
                model.set_value(iter, j, item[j])
                
        hl_model_sort = gtk.TreeModelSort(model)
        
        t = rc_dict['config']['panel_sort%s' % self.number_of_panel]
        if len(t) == 1:
            sort_order = gtk.SORT_ASCENDING
            t = int(t)
        else:
            sort_order = gtk.SORT_DESCENDING
            t = int(t[1:])
        if t < len(Sum_cell) and Sum_cell[t] == 'cell_name':
            t = self.Sort_Index
        else:
            t = 1
        hl_model_sort.set_sort_column_id(t, sort_order)
        hl_model_sort.connect('sort-column-changed', self.__change_sort)
        return hl_model_sort
        
    def __change_sort(self, *args):
        n = args[0].get_sort_column_id()
        if n[0]:
            number = n[0]
            if n[1] == gtk.SORT_DESCENDING:
                h = '-'
            else:
                h = ''
            if number == self.Sort_Index: Sum_cell.index('cell_name')
            rc_dict['config']['panel_sort%s' % self.number_of_panel] = h + str(number)
            print self.Sort_Index
            print rc_dict['config']['panel_sort%s' % self.number_of_panel]
            if self.Path.get_uri() != 'file:///': print 'root'
        
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
            r = f.read(200)
            f.close()
        except: temp = 'empty'
        else: temp = str(gio.content_type_guess(None, r, True)[0])
    else:
        temp = 'application/octet-stream'
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
                    b = icon_load_try(i, int(rc_dict['style']['icon_size']))
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
                b = icon_load_try(i, 24)
            except:
                pass
            else:
                return b
        return icon_load_try('empty', 24)

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
    basename = gioFile.get_basename()
    if basename[0] == '.':
        if is_fil:
            basename = '21' + basename[1:]
        else:
            basename = '10' + basename[1:]
    else:
        if is_fil:
            basename = '20' + basename[1:]
        else:
            basename = '11' + basename[1:]
        
    ret.append(basename)
    return ret

def get_user_shell():
    """Get the user's shell defined in /etc/passwd ."""
    data = None
    try:
        # Read out the data in /etc/passwd
        with open('/etc/passwd') as f:
            data = f.readlines()
    except e:
        print "Something unexpected happened!"
        raise e
    for i in data:
        tmp = i.split(":")
        # Check for the entry of the currently logged in user
        if tmp[0] == getpass.getuser(): 
            return i.split(":")[-1:][0].strip('\n')

########################### edna function (end) ###############################        

def main():
    path = '/home/mort'
    p = Get_gioFile_list(path)
    print p
    #OOF = Object_of_Files()
    #print OOF.add_path(path)

if __name__ == '__main__':
    main()

