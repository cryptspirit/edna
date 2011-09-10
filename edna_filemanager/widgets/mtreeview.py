# -*- coding: utf-8 -*-
import gtk



class File_Cells(gtk.TreeView):
    '''
    Класс списка файлов
    '''
    def __init__(self, number_of_panel, Number_this_list, return_panel_pile, path_entry=gtk.Label):
        gtk.TreeView.__init__(self)
        self.set_rules_hint(True)
        self.set_grid_lines(False)
        self.return_panel_pile = return_panel_pile
        self.path_entry = path_entry
        self.number_of_panel = number_of_panel
        self.Number_this_list = Number_this_list
        self.Hotkeys_Function = {'key_1': self.copys,
                                'key_2': self.deleting,
                                'key_3': self.properties_file,
                                'key_4': '',
                                'key_5': '',
                                'key_6': '',
                                'key_7': '',
                                'key_8': self.show_hide_file}
        #self.get_selection().set_mode(gtk.SELECTION_MULTIPLE)
        self.get_selection().set_mode(gtk.SELECTION_BROWSE)
        self.OOF = edna_function.Object_of_Files(self.number_of_panel, self.update_model)
        self.OOF.add_path(edna_function.rc_dict['config']['panel_history%s' % self.Number_this_list])
        self.path_entry.set_text(self.OOF.Path.get_path())
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
                color_fg = edna_function.rc_dict['style']['odd_row_fg']
                color_bg = edna_function.rc_dict['style']['odd_row_bg']
            else:
                color_fg = edna_function.rc_dict['style']['even_row_fg']
                color_bg = edna_function.rc_dict['style']['even_row_bg']
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
                    """ % (edna_function.rc_dict['style']['even_row_bg'], edna_function.rc_dict['style']['odd_row_bg'])
        #self.set_rules_hint(True)
        self.set_model(self.OOF.Model)
        self.__add_columns()
        self.__set_custom_cursor()
        gtk.rc_reset_styles(self.get_settings())
        gtk.rc_parse_string(rc_string)
        self.modify_base(gtk.STATE_SELECTED, gtk.gdk.Color(edna_function.rc_dict['style']['cursor_row_bg']))
        self.modify_text(gtk.STATE_SELECTED, gtk.gdk.Color(edna_function.rc_dict['style']['cursor_row_fg']))
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
            key = edna_function.get_key_info(args[1])
            print key
            if key == 'Shift Up' or key == 'Shift Down': self.select_function(key)
        elif args[1].type == gtk.gdk.KEY_RELEASE:
            key = edna_function.get_key_info(args[1])
            if key == 'space': self.select_function(key)
            elif key == 'Right': self.chdir_new()
            elif key == 'Return': self.Enter_key()
            elif (key == 'BackSpace' or key == 'Left') and self.OOF.Path != '/': self.back_dir()
            else:
                try: self.Hotkeys_Function[edna_function.key_name_in_rc[key]]()
                except KeyError: pass
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
                
    def deleting(self):
        y = question_window(self.OOF.selection_add())
        
    def properties_file(self):
        '''
        Свойства файла
        '''
        y = properties_file_window(self.OOF.Cursor_Position)
        
    def show_hide_file(self):
        '''
        показать скрытые файлы
        '''
        edna_function.rc_dict['style']['show_hide_files'] = str(int(not int(edna_function.rc_dict['style']['show_hide_files'])))
        self.return_panel_pile().relist_panel()
        
    def copys(self):
        '''
        Копирование
        '''
        remove_after = False
        y = question_window_copy(self.return_panel_pile().get_path_in_panel_opponent(self.Number_this_list), self.OOF.Path, self.OOF.selection_add(), remove_after)
    
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
            sel_col = edna_function.rc_dict['style']['sel_row_fg']
        else:
            sel_col = edna_function.rc_dict['style']['even_row_fg']
        self.OOF.Table_of_File[path][self.OOF.Foreground_Index] = sel_col
        print type(model.get_model())
        model.get_model().set(iter1, self.OOF.Foreground_Index, self.OOF.Table_of_File[path][self.OOF.Foreground_Index])
            
        cellse = edna_function.Sum_cell
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
            self.path_entry.set_text(self.OOF.Path.get_path())
            self.__set_custom_cursor()
                    
    def chdir_new(self):
        '''
        Действие при активации пункта списка
        '''
        selection = self.get_selection()
        model, iter = selection.get_selected()        
        dp = model.get_value(iter, self.OOF.Path_Index)
        self.OOF.gio_activation(dp)
        self.set_model(self.OOF.Model)
        self.path_entry.set_text(self.OOF.Path.get_path())
        edna_function.rc_dict['config']['panel_history%s' % self.Number_this_list] = self.OOF.Path.get_path()
        self.__set_custom_cursor()
        
    def change_dir(self, path):
        self.OOF.gio_activation('file://' + path)
        self.set_model(self.OOF.Model)
        self.path_entry.set_text(self.OOF.Path.get_path())
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
        u = edna_function.Sum_cell
        for i in xrange(self.OOF.len_Sum_cell):
            alg = [float(edna_function.rc_dict['style']['%s_alignment_h' % u[i]]), float(edna_function.rc_dict['style']['%s_alignment_v' % u[i]])]
            if u[i] == 'cell_name':
                column = gtk.TreeViewColumn()
                column.set_title(Name_Colum[u[i]])
                renderer = gtk.CellRendererPixbuf()
                renderer.set_alignment(alg[0], alg[1])
                column.pack_start(renderer, False)
                column.set_sort_column_id(self.OOF.Sort_Index)
                column.set_attributes(renderer, pixbuf=0)
            else:
                #column = gtk.TreeViewColumn(Name_Colum[u[i]], renderer, text=i + 1, background=self.OOF.Background_Index, foreground=self.OOF.Foreground_Index)
                column = gtk.TreeViewColumn(Name_Colum[u[i]], renderer, text=i + 1, foreground=self.OOF.Foreground_Index)
                column.set_sort_column_id(i + 1)  
            column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
            column.expand = True
            column.set_min_width(int(edna_function.rc_dict['style']['%s_size' % u[i]]))
            
            renderer = gtk.CellRendererText()
            #renderer.set_data(Name_Colum[u[i]], i)
            renderer.set_alignment(alg[0], alg[1])
            #renderer.set_property('background-set' , True)
            renderer.set_property('foreground-set' , True)
            renderer.set_property('font-desc' , pango.FontDescription(edna_function.rc_dict['style']['font_cell_text']))
            
            if u[i] == 'cell_name':
                column.pack_start(renderer, True)
                #column.set_attributes(renderer, text=i + 1, background=self.OOF.Background_Index, foreground=self.OOF.Foreground_Index)
                column.set_attributes(renderer, text=i + 1, foreground=self.OOF.Foreground_Index)
                
            itk = int(edna_function.rc_dict['style']['%s_expand' % u[i]])
            column.set_expand(itk)
            #column.set_sort_indicator(True)
            self.append_column(column)
