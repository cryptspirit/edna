# -*- coding: utf-8 -*-

'''
Объекты панели
'''

import __builtin__

edna_builtin = __builtin__.edna_builtin

import gtk
import gio
from edna_filemanager.widgets import drive_panel
from edna_filemanager.widgets import list_widgets
from edna_filemanager.widgets import path_panel
import pango

class Panel_Widget(gtk.VBox):
    '''
    Класс панели содержащей списки файлов
    '''
    def __init__(self, number_of_panel, n, return_path_cell):
        gtk.VBox.__init__(self, False, 3)
        self.n = n
        self.return_path_cell = return_path_cell
        self.number_of_panel = number_of_panel
        self.__conteiner_create__()
        self.__widgets_create__()
        self.__widgets_pack__()
        self.upData()
      
    def __callback_from_fileslist__(self, gioFile):
        '''
        Функция которую запускает список файлов при изминении текущего каталога
        '''
        path = gioFile.get_path()
        self.path_panel.refresh(path)
        if self.get_top_fileslist():
            self.fileslist_pile.set_tab_label_text(self.get_top_fileslist(), path)
        else:
            self.fileslist_pile.set_tab_label_text(self.fileslist_pile.get_nth_page(0), path)
      
    def get_top_fileslist(self):
        '''
        Получение активного списка файлов
        '''
        current_page = self.fileslist_pile.get_current_page()
        return self.fileslist_pile.get_nth_page(current_page)
        
    def __fileslist_add__(self, start_path):
        '''
        Добавление списка файлов
        '''
        #self.fileslist_container.append()
        self.fileslist_pile.append_page(list_widgets.File_List_Widget(start_path, self.__callback_from_fileslist__))
        
    def __fileslist_remove__(self):
        '''
        Удаление списка файлов
        '''
    def __widgets_pack__(self):
        '''
        Упаковка виджетов
        '''
        path_aligment = gtk.Alignment()
        path_aligment.set_padding(0,0,5,5)
        path_aligment.add(self.path_panel)
        
        self.hbox1.pack_start(self.drive_info_label, True)
        self.hbox1.pack_start(self.button_root, False)
        self.hbox1.pack_start(self.button_home, False)
        
        self.hbox2.pack_start(path_aligment, True)
        self.hbox2.pack_start(self.button_history, False)
        self.hbox2.pack_start(self.button_mark, False)
        
        self.pack_start(self.drive_panel, False)
        self.pack_start(self.hbox1, False)
        self.pack_start(self.hbox2, False)
        
        self.pack_start(self.fileslist_pile)
        self.pack_start(self.info_label, False)
        
    def __widgets_create__(self):
        '''
        Создание виджетов
        '''
        self.button_root = gtk.Button(' / ')
        self.button_home = gtk.Button('~/')
        self.button_history = gtk.Button('H')
        self.button_mark = gtk.Button('+')
        self.info_label = gtk.Label('info')
        self.drive_info_label = gtk.Label('drive')
        self.path_panel = path_panel.PathPanel(self.__path_panel_callback__)
        self.info_label = gtk.Label('info')
        self.drive_panel = drive_panel.DrivePanel(self.__drive_panel_callback__)
        self.drive_panel.set_border_width(0)
        self.fileslist_pile = gtk.Notebook()
        self.__fileslist_add__(gio.File('/'))
        self.set_focus_chain((self.fileslist_pile, ))
        
    def __conteiner_create__(self):
        '''
        Создание контейнеров
        '''
        self.hbox1 = gtk.HBox(False, 2)
        self.hbox2 = gtk.HBox(False, 2)
        
        
    def get_action_file_list(self):
        '''
        Возвращает активный список файлов
        '''
        # Метод создается в спешке. его необходимо доработать и расширить
        return self.treeview
        
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
    
    def __path_panel_callback__(self, event):
        '''
        Метод-коллбек, который вызывается при кликах на path-панели
        '''
        if event.type == path_panel.PathEvent.TYPE_CD:
            top_fileslist = self.get_top_fileslist()
            top_fileslist.change_dir(event.path)
    
    def get_number_top_list(self):
        '''
        Функция возвращает номер текущего списка (так как будующем будут
        созданы вкладки с списками
        '''
        return self.treeview.OOF.Path
        
    def upData(self):
        for i in self.fileslist_container:
            i.treeview.Cells_Refresh()

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
        Возвращает панель по имени
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
    
    def where_the_focus(self):
        '''
        Возвращает активную панель и ее имя
        '''
        for i in self.Panel_Box.keys():
            if self.Panel_Box[i].get_focus_child():
                return self.Panel_Box[i], i
            
    def get_panel_opponent(self, Panel_Name):
        '''
        Возвращает соседнюю панель
        '''
        return self.Panel_Box[self.__find_name_panel_opponent(Panel_Name)]
    
