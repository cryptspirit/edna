# -*- coding: utf-8 -*-

from __builtin__ import edna_builtin

import gtk
import gio
import os
import pango
from edna_filemanager import function
from edna_filemanager.tools import keybind
from edna_filemanager.tools import icons_work

class Object_of_Files():
    '''
    Класс обработки списка файлов
    '''
    
    def __init__(self, number_of_panel, update_model=None, callback=None):
        self.return_update_model = update_model
        self.number_of_panel = number_of_panel
        self.callback = callback
        
    def __gen_listdir__(self, gioFile):
        """
        Генерация списка файлов
        """
        show_hide_files = int(edna_builtin['configuration']['style']['show_hide_files'])
        listdir = os.listdir(gioFile.get_path())
        if show_hide_files:
            return map(gio.File, listdir)
        else:
            return [gio.File(i) for i in listdir if i[0] != '.']
        
    def add_path(self, gioFile):
        '''
        Установка пути
        '''
        self.Path = gioFile
        self.Cursor_Position = None
        self.Table_of_File = []
        os.chdir(gioFile.get_path())
        self.Select_List = []
        self.gioFile_list = self.gioFile_list = self.__gen_listdir__(self.Path)
        self.get_list_path()
        self.Model = self.create_model()
        self.Monitor_rootdir = None
        self.Monitor_rootdir = self.Path.monitor_directory(gio.FILE_MONITOR_NONE, None)
        self.Monitor_rootdir.connect('changed', self.event_change_in_rootdir)
        if self.callback: self.callback(self.Path)
        
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
        os.chdir(gioFile.get_path())
        self.gioFile_list = self.__gen_listdir__(self.Path)
        self.get_list_path()
        self.Model = self.create_model()
        self.Monitor_rootdir = self.Path.monitor_directory(gio.FILE_MONITOR_NONE, None)
        self.Monitor_rootdir.connect('changed', self.event_change_in_rootdir)
        if self.callback: self.callback(self.Path)
        
    def gio_activation(self, gioFile):
        '''
        Активация элемента списка
        '''
        if os.path.isdir(gioFile.get_path()):
            self.ch_path(gioFile)
        else:
            ret = get_launch(gioFile)
            if ret:
                ret.launch_uris([gioFile.get_uri()], None)
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
            new_row.append(edna_builtin['configuration']['style']['even_row_fg'])
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
        try: edna_builtin['sequence of columns'].index('cell_user') # Проверка на то есть ли среди столбцов столбец Владелец
        except: pass
        else: get_dickt_nameusers() # Если есть то получение имен пользователей
        
        try: edna_builtin['sequence of columns'].index('cell_group') # Проверка на то есть ли среди столбцов столбец Группа
        except: pass
        else: get_dickt_namegroups() # Если есть то получение названий групп
        ######################################################################
        self.len_Sum_cell = len(edna_builtin['sequence of columns'])
        self.Path_Index = self.len_Sum_cell + 1
        self.Sort_Index = self.len_Sum_cell + 2
        self.Foreground_Index = self.len_Sum_cell + 3
        ######################################################################
        return_dir = []
        return_fil = []
        if self.Path.get_path() != '/':
            ttt = []
            
            ttt.append(edna_builtin['icons container']['application/octet-stream'])
            for j in edna_builtin['sequence of columns']:
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
                return_dir_append(function.get_cell(i, False))
            else:
                return_fil_append(function.get_cell(i, True))
        
        return_dir.sort()
        return_fil.sort()
        
        m = return_dir + return_fil
        if self.Path.get_path() != '/':
            m.insert(0, ttt)
        op = 0
        
        for i in xrange(len(m)):
            m[i].append(edna_builtin['configuration']['style']['even_row_fg'])
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
        
        #t = edna_builtin['configuration']['config']['panel_sort%s' % self.number_of_panel]
        t = '0'
        if len(t) == 1:
            sort_order = gtk.SORT_ASCENDING
            t = int(t)
        else:
            sort_order = gtk.SORT_DESCENDING
            t = int(t[1:])
        if t < len(edna_builtin['sequence of columns']) and edna_builtin['sequence of columns'][t] == 'cell_name':
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
            if number == self.Sort_Index: edna_builtin['sequence of columns'].index('cell_name')
            edna_builtin['configuration']['config']['panel_sort%s' % self.number_of_panel] = h + str(number)
            print self.Sort_Index
            print edna_builtin['configuration']['config']['panel_sort%s' % self.number_of_panel]
            if self.Path.get_uri() != 'file:///': print 'root'


class File_List_Widget(gtk.ScrolledWindow):
    '''
    Класс списка файлов
    '''
    def __init__(self, start_path, callback=None):
        gtk.ScrolledWindow.__init__(self)
        self.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        self.treeview = Files_List(start_path, callback)
        self.add(self.treeview)
        
    def change_dir(self, path):
        self.treeview.change_dir(path)
    
class Files_List(gtk.TreeView):
    '''
    Список файлов
    '''
    def __init__(self, start_path, callback=None):
        gtk.TreeView.__init__(self)
        self.set_rules_hint(True)
        self.set_grid_lines(False)
        #self.return_panel_pile = return_panel_pile
        #self.number_of_panel = number_of_panel
        #self.Number_this_list = Number_this_list
        #self.get_selection().set_mode(gtk.SELECTION_MULTIPLE)
        self.get_selection().set_mode(gtk.SELECTION_BROWSE)
        self.OOF = Object_of_Files(start_path, self.update_model, callback)
        #self.OOF.add_path(edna_builtin['configuration']['config']['panel_history%s' % self.Number_this_list])
        self.OOF.add_path(start_path)
        self.connect('key-release-event', self.key_event)
        self.connect('key-press-event', self.key_event)
        self.connect('button-press-event', self.pr)
        self.connect('cursor-changed', self.cursor_changed)
        self.connect('focus-in-event', self.__focus_trap)
        self.connect('focus-out-event', self.__focus_trap)

    def __focus_trap(self, *args):
        '''
        Ловушка для фокуса клавиатуры
        '''

        if self.is_focus():
            pass
        else:
            i = self.get_cursor()[0]
            if i[0] % 2 != 0:
                color_fg = edna_builtin['configuration']['style']['odd_row_fg']
                color_bg = edna_builtin['configuration']['style']['odd_row_bg']
            else:
                color_fg = edna_builtin['configuration']['style']['even_row_fg']
                color_bg = edna_builtin['configuration']['style']['even_row_bg']
            self.modify_base(gtk.STATE_ACTIVE, gtk.gdk.Color(color_bg))
            self.modify_text(gtk.STATE_ACTIVE, gtk.gdk.Color(color_fg))
    
    def refresh_cells(self):
        '''
        Обновление списка файлов
        '''
        self.change_dir(self.OOF.Path.get_path())
    
    def update_model(self, gioFile_uri, operation, data=None):
        '''
        Реакция списка на изменения в файловой системе
        '''
        model = self.get_model().get_model()
        if operation == 0:
            #Удаление
            for i in xrange(len(self.OOF.Table_of_File) + 1):
                iter = model.get_iter(i)
                if model.get_value(iter, self.OOF.Path_Index) == gioFile_uri:
                    if (self.get_cursor()[0])[0] == i:
                        if i == len(self.OOF.Table_of_File):
                            self.set_cursor(len(self.OOF.Table_of_File) - 1)
                        else:
                            self.set_cursor(i)
                    model.remove(iter)
                    return
        elif operation == 1:
            #Изменения
            for i in xrange(len(self.OOF.Table_of_File)):
                iter = model.get_iter(i)
                if model.get_value(iter, self.OOF.Path_Index) == gioFile_uri:
                    for j in xrange(len(data)):
                        model.set_value(iter, j, data[j])
                    return
        elif operation == 2:
            #Создание
            iter = model.append()
            for j in xrange(len(data)):
                model.set_value(iter, j, data[j])
            return
        
    def Cells_Refresh(self):
        '''
        Обновление списка файлов
        '''
        #Переписываем стиль для отображения четных и нечетных строк
        rc_string = """
                    style "treeview-style" {
                        GtkTreeView::even-row-color = "%s"
                        GtkTreeView::odd-row-color = "%s"
                    }
                    class "GtkTreeView" style "treeview-style"
                    """ % (edna_builtin['configuration']['style']['even_row_bg'], edna_builtin['configuration']['style']['odd_row_bg'])
        #self.set_rules_hint(True)
        self.set_model(self.OOF.Model)
        self.__add_columns()
        self.__set_custom_cursor()
        gtk.rc_reset_styles(self.get_settings())
        gtk.rc_parse_string(rc_string)
        self.modify_base(gtk.STATE_SELECTED, gtk.gdk.Color(edna_builtin['configuration']['style']['cursor_row_bg']))
        self.modify_text(gtk.STATE_SELECTED, gtk.gdk.Color(edna_builtin['configuration']['style']['cursor_row_fg']))
        #self.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_VERTICAL)
        #self.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)
        
    def cursor_changed(self, *args):
        selection = self.get_selection()
        model_sel, iter_sel = selection.get_selected()
        self.OOF.Cursor_Position = gio.File(model_sel.get_value(iter_sel, self.OOF.Path_Index))
            
    def key_event(self, *args):
        '''
        Обработка нажатий клавиш списка
        '''
        if args[1].type == gtk.gdk.KEY_PRESS:
            key = keybind.get_key_info(args[1])
            print key
            if key == 'Shift Up' or key == 'Shift Down': self.select_function(key)
        elif args[1].type == gtk.gdk.KEY_RELEASE:
            key = keybind.get_key_info(args[1])
            if key == 'space': self.select_function(key)
            elif key == 'Right': self.chdir_new()
            elif key == 'Return': self.Enter_key()
            elif (key == 'BackSpace' or key == 'Left') and self.OOF.Path != '/': self.back_dir()
            #if key == 'Delete' or key == 'Shift Delete': self.deleting(key)
            #if key == 'F5' : self.copys(False)
    
    def Enter_key(self):
        '''
        Обработка нажатия клавиши Enter. Груповой запуск программ
        '''
        if os.path.isdir(self.OOF.Cursor_Position.get_path()):
            self.chdir_new()
        else:
            sel_list = self.OOF.selection_add()
            list_lanch = {}
            for i in sel_list:
                if i[1]:
                    ret = edna_function.get_launch(gio.File(i[0]))
                    if ret:
                        r_name = ret.get_name()
                        try:
                            list_lanch.keys().index(r_name)
                        except:
                            list_lanch[r_name] = {'app': ret, 'list':[i[0]]}
                        else:
                            list_lanch[r_name]['list'].append(i[0])
            for i in list_lanch.keys():
                list_lanch[i]['app'].launch_uris(list_lanch[i]['list'], None)
                
    def return_path_parent_row(self, gioFile_uri):
        model = self.get_model()
        for i in xrange(len(self.OOF.Table_of_File)):
            iter = model.get_iter(i)
            if model.get_value(iter, self.OOF.Path_Index) == gioFile_uri: return i
        return 0
            
    def select_function(self, key):
        
        selection = self.get_selection()
        model, iter = selection.get_selected()
        
        print 'iter', model
        gioFile_uri = model.get_value(iter, self.OOF.Path_Index)        
        self.OOF.selection(gioFile_uri)
        path = model.get_path(iter)[0]
        iter1 = model.convert_iter_to_child_iter(None, iter)
        sel_col = {}
        if self.OOF.now_in_selection(gioFile_uri):
            sel_col = edna_builtin['configuration']['style']['sel_row_fg']
        else:
            sel_col = edna_builtin['configuration']['style']['even_row_fg']
        self.OOF.Table_of_File[path][self.OOF.Foreground_Index] = sel_col
        print type(model.get_model())
        model.get_model().set(iter1, self.OOF.Foreground_Index, self.OOF.Table_of_File[path][self.OOF.Foreground_Index])
            
        cellse = edna_builtin['sequence of columns']
        if key == 'space':
            try:
                ic = cellse.index('cell_size') + 1
            except:
                pass
            else:
                n = gio.File(gioFile_uri).get_path()
                if os.path.isdir(n):
                    self.OOF.Table_of_File[path][ic] = edna_function.get_in_format_size(edna_function.get_full_size(n))
                    model.get_model().set(iter1, ic, self.OOF.Table_of_File[path][ic])
            
    def pr(self, *args):
        if args[1].type == gtk.gdk._2BUTTON_PRESS:
            self.chdir_new()
            
    def __set_custom_cursor(self):
        '''
        Установка курсора на прошлый каталог нижнего уровня
        '''
        try:
            path_of_list = self.return_path_parent_row(self.OOF.Cursor_Position.get_uri())
        except:
            path_of_list = 0
        self.set_cursor(path_of_list)
        
    def back_dir(self):
        '''
        Возвращение в родительский каталог
        '''
        if self.OOF.Path.get_path() != '/':
            self.OOF.gio_activation(self.OOF.Path.get_parent().get_uri())
            self.set_model(self.OOF.Model)
            self.__set_custom_cursor()
                    
    def chdir_new(self):
        '''
        Действие при активации пункта списка
        '''
        selection = self.get_selection()
        model, iter = selection.get_selected()        
        dp = model.get_value(iter, self.OOF.Path_Index)
        self.OOF.gio_activation(gio.File(dp))
        self.set_model(self.OOF.Model)
        #edna_builtin['configuration']['config']['panel_history%s' % self.Number_this_list] = self.OOF.Path.get_path()
        self.__set_custom_cursor()
        
    def change_dir(self, path):
        self.OOF.gio_activation(gio.File(path))
        self.set_model(self.OOF.Model)
        self.__set_custom_cursor()

    def __add_columns(self):
        '''
        Создание столбцов
        '''
        model = self.get_model()
        clmn = self.get_columns()
        if clmn:
            for i in clmn:
                self.remove_column(i)
        u = edna_builtin['sequence of columns']
        for i in xrange(self.OOF.len_Sum_cell):
            alg = [float(edna_builtin['configuration']['style']['%s_alignment_h' % u[i]]), float(edna_builtin['configuration']['style']['%s_alignment_v' % u[i]])]
            if u[i] == 'cell_name':
                column = gtk.TreeViewColumn()
                column.set_title(edna_builtin['structures']['colums name'][u[i]])
                renderer = gtk.CellRendererPixbuf()
                renderer.set_alignment(alg[0], alg[1])
                column.pack_start(renderer, False)
                column.set_sort_column_id(self.OOF.Sort_Index)
                column.set_attributes(renderer, pixbuf=0)
            else:
                #column = gtk.TreeViewColumn(edna_builtin['structures']['colums name'][u[i]], renderer, text=i + 1, background=self.OOF.Background_Index, foreground=self.OOF.Foreground_Index)
                column = gtk.TreeViewColumn(edna_builtin['structures']['colums name'][u[i]], renderer, text=i + 1, foreground=self.OOF.Foreground_Index)
                column.set_sort_column_id(i + 1)  
            column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
            column.expand = True
            column.set_min_width(int(edna_builtin['configuration']['style']['%s_size' % u[i]]))
            
            renderer = gtk.CellRendererText()
            #renderer.set_data(edna_builtin['structures']['colums name'][u[i]], i)
            renderer.set_alignment(alg[0], alg[1])
            #renderer.set_property('background-set' , True)
            renderer.set_property('foreground-set' , True)
            renderer.set_property('font-desc' , pango.FontDescription(edna_builtin['configuration']['style']['font_cell_text']))
            
            if u[i] == 'cell_name':
                column.pack_start(renderer, True)
                #column.set_attributes(renderer, text=i + 1, background=self.OOF.Background_Index, foreground=self.OOF.Foreground_Index)
                column.set_attributes(renderer, text=i + 1, foreground=self.OOF.Foreground_Index)
                
            itk = int(edna_builtin['configuration']['style']['%s_expand' % u[i]])
            column.set_expand(itk)
            #column.set_sort_indicator(True)
            self.append_column(column)
