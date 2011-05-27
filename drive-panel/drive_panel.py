#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       search_gui_class.py
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

class DrivePanel(gtk.Toolbar):
    def __init__(self):
        gtk.Toolbar.__init__(self)
        self.set_style(gtk.TOOLBAR_BOTH_HORIZ)
        self.set_icon_size(gtk.ICON_SIZE_MENU)
        self.vm = gio.VolumeMonitor()
        self.vm.connect('volume-added', self.volume_changed)
        self.vm.connect('volume-removed', self.volume_changed)
        self.vm.connect('mount-added', self.volume_changed)
        self.vm.connect('mount-removed', self.volume_changed)        
        self.refresh(self.vm)
        
    def volume_changed(self, vm, volume):
        self.refresh(self.vm)
        image = gtk.Image()
        image.set_from_gicon(volume.get_icon(),gtk.ICON_SIZE_MENU)

        
    def refresh(self, vm):
        for child in self.get_children():
            self.remove(child)
        
        volumes = vm.get_volumes()
        
        #print volumes
        b = gtk.ToolButton(gtk.STOCK_HARDDISK)
        b.set_is_important(True)
        b.set_label('/')
        self.insert(b, 0)            
        b = gtk.ToolButton(gtk.STOCK_HOME)
        self.insert(b, 1)
        uris = []
        for volume in volumes:
            image = gtk.Image()
            image.set_from_gicon(volume.get_icon(),gtk.ICON_SIZE_MENU)
            b = gtk.ToolButton(image, volume.get_name())
            b.set_is_important(True)
            b.connect('clicked', self.callback, volume)
            self.insert(b, self.get_n_items())
            m = volume.get_mount()
            if m:
                uris.append(volume.get_mount().get_root().get_uri())
        
        mounts = vm.get_mounts()
        print mounts
        for mount in mounts:
            if mount.get_root().get_uri() not in uris:
                image = gtk.Image()
                image.set_from_gicon(mount.get_icon(),gtk.ICON_SIZE_MENU)
                b = gtk.ToolButton(image, mount.get_name())
                b.set_is_important(True)
                b.connect('clicked', self.callback, mount)
                self.insert(b, self.get_n_items())
        self.show_all()
            
    def callback(self, sender, item):
        if isinstance(item, gio.Volume):
            m = item.get_mount()
        else:
            m = item
        if m:
            print m.get_root().get_uri()

def main():
    d = DrivePanel()
    w = gtk.Window()
    vbox = gtk.VBox(False, 10)
    vbox.pack_start(d, False, False)
    #vbox.pack_start(gtk.Button(), True, True)
    w.add(vbox)
    w.set_position(gtk.WIN_POS_CENTER)
    w.set_default_size(800,500)
    w.show_all()
    gtk.main()
    return 0

if __name__ == '__main__':
    help(type(pynotify.Notification))
    main()

