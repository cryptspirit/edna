#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       drive_panel.py
#       
#       Copyright 2011 Sevka <sevka@ukr.net>
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
import gtk
import gio
import pynotify
import os

class Drive():
    '''
    Класс для драйвов драйвов типа / и ~.
    Возможно в настройках можно будет добавлять какие-то кастомные драйвы
    '''
    def __init__(self, name, path):
        self.name = name
        self.path = path
        
class DriveEvent():
    '''
    Класс события происходящего на драйв-панели. 
    TYPE_CD - смена каталога
    TYPE_UNMOUNT - отмонтирование устройства (еще не реализовано)
    '''
    TYPE_CD = 1
    TYPE_UNMOUNT = 2
    
    def __init__(self, type, param):
        self.type = type
        if type == self.TYPE_CD:
            self.path = param
        
class DrivePanel(gtk.Toolbar):
    '''
    Виджет драйв-панели
    '''
    def __init__(self, callback):
        '''
        Конструктор панели
        :param callback: Метод-коллбек, который будет вызван при возникновении 
            события. В качестве параметра будет передан объект DriveEvent
        '''
        gtk.Toolbar.__init__(self)
        self.callback = callback
        self.set_style(gtk.TOOLBAR_BOTH_HORIZ)
        self.set_icon_size(gtk.ICON_SIZE_MENU)
        self.vm = gio.VolumeMonitor()
        self.vm.connect('volume-added', self.volume_changed)
        self.vm.connect('volume-removed', self.volume_changed)
        self.vm.connect('mount-added', self.volume_changed)
        self.vm.connect('mount-removed', self.volume_changed)        
        self.refresh(self.vm)
        
    def volume_changed(self, vm, volume):
        '''
        Метод вызывается при любом изменении устройств (отмонтирование, примонтирование)
        '''
        self.refresh(self.vm)
        image = gtk.Image()
        image.set_from_gicon(volume.get_icon(),gtk.ICON_SIZE_MENU)
        
    def refresh(self, vm):
        '''
        Полная перерисовка кнопок на драйв-панели
        '''
        for child in self.get_children():
            self.remove(child)
        uris = []
        # рут и хоум
        b = gtk.ToolButton(gtk.STOCK_HARDDISK)
        b.set_label('/')
        b.connect('clicked', self.clicked, Drive('/','/'))
        self.insert(b, self.get_n_items())
        
        b = gtk.ToolButton(gtk.STOCK_HOME)
        b.set_label('~')
        b.connect('clicked', self.clicked, Drive('Home', os.path.expanduser('~')))
        self.insert(b, self.get_n_items())
        
        # volumes
        volumes = vm.get_volumes()
        for volume in volumes:
            mount = volume.get_mount()
            if mount:
                uri = mount.get_root().get_uri()
                uris.append(uri)
            else:
                uri = None
            image = gtk.Image()
            image.set_from_gicon(volume.get_icon(),gtk.ICON_SIZE_MENU)
            b = gtk.ToolButton(image, volume.get_name())
            b.set_is_important(True)
            b.connect('clicked', self.clicked, volume)
            self.insert(b, self.get_n_items())
            
        #mounts
        mounts = vm.get_mounts()
        for mount in mounts:
            if mount.get_root().get_uri() not in uris:
                image = gtk.Image()
                image.set_from_gicon(mount.get_icon(),gtk.ICON_SIZE_MENU)
                b = gtk.ToolButton(image, mount.get_name())
                b.set_is_important(True)
                b.connect('clicked', self.clicked, mount)
                self.insert(b, self.get_n_items())
        
        self.show_all()
        
    def async_result_callback(self, volume, response):
        '''
        Коллбек, который вызывается при завершении монтирования
        '''
        print self, volume, response
        if volume.get_mount():
            self.clicked(self, volume)
            
    def clicked(self, sender, item):
        '''
        Клик по кнопке
        '''
        m = None
        path = None
        if isinstance(item, gio.Volume):
            m = item.get_mount()
            if not m and item.can_mount():
                item.mount(gio.MountOperation(), self.async_result_callback)
        elif isinstance(item, gio.Mount):
            m = item
        else:
            path = item.path
        if m:
            path = m.get_root().get_path()
        if path:    
            self.callback(DriveEvent(DriveEvent.TYPE_CD, path))

def main():
    d = DrivePanel(None)
    w = gtk.Window()
    vbox = gtk.VBox(False, 10)
    vbox.pack_start(d, False, False)
    w.add(vbox)
    w.set_position(gtk.WIN_POS_CENTER)
    w.set_default_size(800,500)
    w.show_all()
    gtk.main()
    return 0

if __name__ == '__main__':
    main()

