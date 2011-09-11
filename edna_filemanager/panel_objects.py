# -*- coding: utf-8 -*-

'''
Объекты панели
'''

import gtk
from widgets import list_widgets
from widgets import drive_panel

class Panel_Widget(gtk.VBox):
    '''
    Класс панели содержащей списки файлов
    '''
    def __init__(self, number_of_panel, n, return_path_cell):
        gtk.VBox.__init__(self, False, 3)
        self.n = n
        self.return_path_cell = return_path_cell
        #self.Cursor = 0
        self.Focus_State = True
        self.number_of_panel = number_of_panel
        ####################################
        self.scrol = gtk.ScrolledWindow()
        self.scrol.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        self.scrol.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        ###################################
        self.drive_info_label = gtk.Label('drive')
        ###################################
        self.path_entry = gtk.Label()
        self.evtb = gtk.EventBox()
        self.evtb.add(self.path_entry)
        self.evtb.set_border_width(3)
        
        self.path_entry.set_alignment(0.0, 0.5)
        ###################################
        self.treeview = list_widgets.File_List_Widget(self.number_of_panel, n, return_path_cell, self.path_entry)
        self.info_label = gtk.Label('info')
        self.drive_panel = drive_panel.DrivePanel(self.__drive_panel_callback__)
        self.drive_panel.set_border_width(0)
        ###################################
        self.scrol.add(self.treeview)
        self.upData()
        self.pack_start(self.drive_panel, False)
        self.pack_start(self.evtb, False)
        self.pack_start(self.scrol)
        self.pack_start(self.info_label, False)
        self.set_focus_chain((self.treeview, ))
        #self.Timer_func = threading.Timer(0, self.timer_refresh)
        #self.Timer_func.start()
        
    def __drive_panel_callback__(self, event):
        '''
        Метод-коллбек, который вызывается при кликах на драйв-панели
        '''
        if event.type == drive_panel.DriveEvent.TYPE_CD:
            self.treeview.change_dir(event.path)
        elif event.type == drive_panel.DriveEvent.TYPE_UNMOUNT:
            if self.treeview.OOF.Path.get_path().startswith(event.path):
                self.treeview.change_dir('/')
            self.return_path_cell().get_panel_opponent(self.n).treeview.OOF.Path.get_path()
            if self.return_path_cell().get_panel_opponent(self.n).treeview.OOF.Path.get_path().startswith(event.path):
                self.return_path_cell().get_panel_opponent(self.n).treeview.change_dir('/')
                
    def get_number_top_list(self):
        '''
        Функция возвращает номер текущего списка (так как будующем будут
        созданы вкладки с списками
        '''
        return self.treeview.OOF.Path
        
    def upData(self):
        self.evtb.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(edna_function.rc_dict['style']['even_row_bg']))
        self.evtb.modify_font(pango.FontDescription(edna_function.rc_dict['style']['font_cell_text']))
        self.path_entry.modify_fg(gtk.STATE_NORMAL, gtk.gdk.Color(edna_function.rc_dict['style']['even_row_fg']))
        self.treeview.Cells_Refresh()

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
    
