#!/usr/bin/python2
# -*- coding: utf-8 -*-
#
#       Edna.py
#       
#       Copyright 2011 CryptSpirit <cryptspirit@gmail.com>
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

import gobject
import gtk
import os
import sys
import time
import gui_class_main
import edna_function
import rc_modul
import hotkeys
import profile
import gettext

gettext.install('edna', unicode=True)

class Dwindow(gtk.Window):
    def __init__(self):
        gtk.Window.__init__(self)
        self.connect('destroy', self.exitt)
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_default_size(900, 500)
        self.set_title('Edna')
        # Widget#########################
        self.vbox1 = gtk.VBox(True, 5)
        self.hpannel1 = gtk.HBox(True,5)
        self.hpannel1.set_border_width(5)
        self.cel = []
        self.cel.append(gui_class_main.listen_cell(0, self.return_path_cell))
        self.cel.append(gui_class_main.listen_cell(1, self.return_path_cell))
        self.set_focus(self.cel[0].treeview)
        self.foc_c = True
        #################################
        #BOX############################
        for i in xrange(2):
            self.hpannel1.pack_start(self.cel[i])
        self.vbox1.pack_start(self.hpannel1)
        ################################
        #self.connect('key-release-event', self.key_c)
        #self.connect('key-press-event', self.key_c)
        self.add(self.vbox1)
        self.foc = self.is_focus()
        self.connect('focus', self.focuss)
        
    def return_path_cell(self, index):
        return self.cel[not index].Current_Path

        
    def upData(sefl):
        self.cel1.upData()
        self.cel2.upData()
        
    def focuss(self, *args):
        if self.foc != self.is_focus():
            self.foc = self.is_focus()
            for i in self.cel: i.Focus_State = self.is_focus()
        
    def exitt(self, *args):
        for i in self.cel: i.Exit_State = True
        args[0].hide()
        gtk.main_quit()
        
def main():
    gtk.gdk.threads_init()
    d = Dwindow()
    d.show_all()
    gtk.main()
    return 0

if __name__ == '__main__':
    #profile.run('main()')
    main()
