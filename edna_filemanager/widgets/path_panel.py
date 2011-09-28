# -*- coding: utf-8 -*-

'''
Created on 21 сент. 2011

@author: sevka
'''
import gtk
import os
import gio
import gobject
class PathEvent():
    '''
    Класс события происходящего на path-панели. 
    '''
    TYPE_CD = 1
    
    def __init__(self, type, param):
        self.type = type
        if type == self.TYPE_CD:
            self.path = param

class PathPanel(gtk.HBox):
    '''
    Виджет path-панели
    '''
    def __init__(self, callback):
        '''
        Конструктор панели
        :param callback: Метод-коллбек, который будет вызван при возникновении 
            события. В качестве параметра будет передан объект PathEvent
        '''
        gtk.HBox.__init__(self)
        self.callback = callback
        self.longest_common_path = None
        self.path = None
        self.pathHBox = gtk.HBox()
        self.editBtn = gtk.ToggleToolButton(gtk.STOCK_EDIT)
        self.editBtn.connect('clicked', self.__edit_clicked__)
        #self.editBtn.set_size_request(32,32)
        self.pathEntry = gtk.Entry()
        self.completion = gtk.EntryCompletion()
        self.pathEntry.set_completion(self.completion)
        self.pathEntry.hide()
        self.pathEntry.connect('focus-out-event', self.__edit_focus_out__)
        self.pathEntry.connect('key-release-event',self.__edit_key_released__)
        self.historyBtn = gtk.ToolButton(gtk.STOCK_GO_DOWN)
        self.favBtn = gtk.ToolButton(gtk.STOCK_ABOUT)
        self.pack_start(self.editBtn, False, False)
        self.pack_start(self.pathHBox, True,True)
        self.pack_start(self.pathEntry, True,True)
#        self.pack_start(self.historyBtn, False, False)
#        self.pack_start(self.favBtn, False, False)
#        self.historyBtn.show()
#        self.favBtn.show()
        self.set_no_show_all(True)
    
    def __update_completion__(self, path):
        '''
        Метод обновляет список автодополнений для pathEntry, если в списке 
        оказывается один элемент, он попадает в pathEntry
        '''
        self.liststore = gtk.ListStore(str)
        command = "bash -c \"compgen -c '" + path +"'|sort -u\""
        result = os.popen(command).read()
        lines = result.splitlines()
        #print lines
        
        if len(lines) == 1 :#& len(self.pathEntry.get_selection_bounds()) == 0:
            common = os.path.commonprefix([lines[0], path])
            self.pathEntry.set_text(self.pathEntry.get_text() + lines[0][len(common):])
            self.pathEntry.select_region(len(common),-1)
        
        for line in lines:
            self.liststore.append([line])
        self.completion.set_model(self.liststore)
        self.completion.set_text_column(0)
    
    def __edit_clicked__(self, sender):
        '''
        Клик на кнопке 'edit path'
        '''
        if sender.get_active():
            self.pathHBox.hide()
            self.pathEntry.set_text(self.path)
            self.pathEntry.select_region(0, self.pathEntry.get_text_length())
            self.pathEntry.show()
            self.pathEntry.grab_focus()
        else:
            self.pathHBox.show()
            self.pathEntry.hide()
    
    def edit_path(self):
        self.editBtn.set_active(not self.editBtn.get_active())
    
    def __edit_focus_out__(self, widget, event):
        '''
        Метод вызывается при потере фокуса path entry
        '''
        self.pathHBox.show()
        self.pathEntry.hide()
        self.editBtn.set_active(False)
    
    def refresh(self, path):
        '''
        Перерисовка панели при смене активного каталога
        :param path: новый каталог
        '''
        for child in self.pathHBox.get_children():
            self.pathHBox.remove(child)
        pathToCD = '/'
        if path == '/':
            items = ['']
        else:
            items = path.split('/')
        
        if not self.longest_common_path:
            self.longest_common_path = self.path
        else:
            commonPath = os.path.commonprefix([path,self.path])
            commonPath2 = os.path.commonprefix([path,self.longest_common_path])
            if commonPath:
                if len(path) > len(self.longest_common_path) or path != commonPath2:
                    self.longest_common_path = path
            else:
                self.longest_common_path = path
        k = 0
        for item in items:
            pathToCD = os.path.join(pathToCD, item)
            if item != '' or len(items) == 1:
                item = '/' + item
            eventBox = gtk.EventBox()
            eventBox.add(gtk.Label(item))
            eventBox.connect('button-press-event', self.__path_clicked__, pathToCD)
            eventBox.connect('enter-notify-event', self.__mouse_enter__, k)
            eventBox.connect('leave-notify-event', self.__mouse_leave__, k)
            self.pathHBox.pack_start(eventBox, False, False)
            k += 1
        if self.longest_common_path and len(self.longest_common_path) > len(path):
            items2 = self.longest_common_path.split('/')
            i = 0
            for item in items2:
                i += 1
                if i > len(items):
                    pathToCD = os.path.join(pathToCD, item)
                    eventBox = gtk.EventBox()
                    if i == (len(items) + 1) and len(items) == 1 and items[0] == '':
                        label = gtk.Label(item)
                    else:
                        label = gtk.Label('/' + item)
                    label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.Color('#c0c0c0'))
                    eventBox.add(label)
                    eventBox.connect('button-press-event', self.__path_clicked__, pathToCD)
                    eventBox.connect('enter-notify-event', self.__mouse_enter__, k)
                    eventBox.connect('leave-notify-event', self.__mouse_leave__, k)
                    self.pathHBox.pack_start(eventBox, False, False)
                    k += 1
        self.path = path
        self.show()
        self.editBtn.show()
        self.pathEntry.hide()
        self.editBtn.set_active(False)
        self.pathHBox.show_all()

    def __path_clicked__(self, sender, b, path):
        '''
        Метод вызывается при клике на пути
        '''
        self.callback(PathEvent(PathEvent.TYPE_CD, path))
    
    def __edit_key_released__(self, widget, event):
        '''
        Метод ловит все нажатые клавиши во время редактирования пути
        '''
        key = gtk.gdk.keyval_name(event.keyval)
        #print key
        if key == 'Return':
            path = self.pathEntry.get_text()
            if os.path.exists(path) & os.path.isdir(path):
                self.callback(PathEvent(PathEvent.TYPE_CD, path))
            else:
                return
        elif key == 'Escape':
            pass
        elif key in ('BackSpace','Delete','Left','Right','Up','Down','Home','End','Control_L','Control_R','Shift_L','Shift_R'):
            return
        else:
            self.__update_completion__(self.pathEntry.get_text())
            return
        self.__edit_focus_out__(widget, event)
    
    def __mouse_enter__(self, sender, b, n):
        '''
        Метод вызывается при наведении мыши на элемент пути
        '''
        children = self.pathHBox.get_children()
        for i in range(0,n+1):
            children[i].get_children()[0].modify_fg(gtk.STATE_PRELIGHT, gtk.gdk.Color('#ff0000'))
            children[i].get_children()[0].set_state(gtk.STATE_PRELIGHT)
    
    def __mouse_leave__(self, sender, b, n):
        '''
        Метод вызывается при покидании мышью элемента пути 
        '''
        children = self.pathHBox.get_children()
        for i in range(0,n+1):
            children[i].get_children()[0].set_state(gtk.STATE_NORMAL)
            