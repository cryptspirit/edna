# -*- coding: utf-8 -*-

'''
Created on 21 сент. 2011

@author: sevka
'''
import gtk
import os

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
    
    def refresh(self, path):
        '''
        Перерисовка панели при смене активного каталога
        :param path: новый каталог
        '''
        for child in self.get_children():
            self.remove(child)
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
            eventBox.connect('button-press-event', self.path_clicked, pathToCD)
            eventBox.connect('enter-notify-event', self.mouse_enter, k)
            eventBox.connect('leave-notify-event', self.mouse_leave, k)
            self.pack_start(eventBox, False, False)
            k += 1
        if self.longest_common_path and len(self.longest_common_path) > len(path):
            items2 = self.longest_common_path.split('/')
            i = 0
            for item in items2:
                i += 1
                if i > len(items):
                    pathToCD = os.path.join(pathToCD, item)
                    eventBox = gtk.EventBox()
                    label = gtk.Label('/' + item)
                    label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.Color('#c0c0c0'))
                    eventBox.add(label)
                    eventBox.connect('button-press-event', self.path_clicked, pathToCD)
                    eventBox.connect('enter-notify-event', self.mouse_enter, k)
                    eventBox.connect('leave-notify-event', self.mouse_leave, k)
                    self.pack_start(eventBox, False, False)
                    k += 1
        self.path = path
        self.show_all()
        
    def path_clicked(self, sender, b, path):
        self.callback(PathEvent(PathEvent.TYPE_CD, path))
    
    def mouse_enter(self, sender, b, n):
        children = self.get_children()
        for i in range(0,n+1):
            children[i].get_children()[0].modify_fg(gtk.STATE_PRELIGHT, gtk.gdk.Color('#ff0000'))
            children[i].get_children()[0].set_state(gtk.STATE_PRELIGHT)
    
    def mouse_leave(self, sender, b, n):
        children = self.get_children()
        for i in range(0,n+1):
            pass
            children[i].get_children()[0].set_state(gtk.STATE_NORMAL)
            