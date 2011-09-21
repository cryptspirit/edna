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
        self.refresh('/home/sevka/projects')
    
    def refresh(self, path):
        for child in self.get_children():
            self.remove(child)
        pathToCD = '/'
        if path == '/':
            items = ['']
        else:
            items = path.split('/')
        for item in items:
            pathToCD = os.path.join(pathToCD, item)
            if item != '' or len(items) == 1:
                item = '/' + item
            eventBox = gtk.EventBox()
            eventBox.add(gtk.Label(item))
            eventBox.connect('button-press-event', self.path_clicked, pathToCD)
            self.pack_start(eventBox, False, False)
        self.show_all()
        
    def path_clicked(self, sender, b, path):
        self.callback(PathEvent(PathEvent.TYPE_CD, path))
            