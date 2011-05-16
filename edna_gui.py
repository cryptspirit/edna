#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#       edna_gui.py
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
import edna_function
import pango
import os
import re
import subprocess
import threading
import time
import filecmp
import gettext
import gio

gettext.install('edna', unicode=True)
###############################################################################
self_name = 'Edna'

Name_Colum = {'cell_name': _('Name'), 
            'cell_type': _('Type'), 
            'cell_size': _('Size'), 
            'cell_datec': _('Created'), 
            'cell_datem': _('Changed'), 
            'cell_user': _('User'), 
            'cell_group': _('Group'), 
            'cell_atr': _('Attribute')}

keys_not_follow = ['Shift Shift_L', 'Shift Shift_R', 'Alt Alt_L', 'Alt Alt_R', 'Escape',
                    'Return', 'Ctrl Control_L', 'Ctrl Control_R', 'Caps_Lock',
                    'Alt ISO_Prev_Group', 'Alt ISO_Next_Group', 'Ctrl Shift_R',
                    'Ctrl Shift_L', 'Shift Control_R', 'Shift Control_L', 'Shift_L',
                    'Shift_R', 'Alt_R', 'Alt_L', 'Control_R', 'Control_L', 'Tab', 
                    'Left', 'Up', 'Right', 'Down', 'minus', 'equal', 'Shift plus',
                    'Home', 'End', 'Page_Up', 'Page_Down', 'space',
                    'Menu', 'grave', 'Insert', 'semicolon', 'comma', 'period',
                    'slash', 'backslash', 'BackSpace']

keys_not_follow += map(str, xrange(10))
keys_not_follow += map(chr, xrange(65, 123))
###############################################################################

###############################  Gui class (begin) ############################
class miss_window(gtk.Window):
    '''
    Класс окна ошибке доступа к файлу
    '''
    def __init__(self, text):
        gtk.Window.__init__(self)
        self.connect('destroy', self.destr)
        self.connect('key-release-event', self.key_event)
        self.set_resizable(False)
        self.set_border_width(5)
        self.set_modal(True)
        self.set_icon(edna_function.get_theme.load_icon('gtk-dialog-info', 20, 0))
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_title(_('Error! I not can read file'))
        
        if os.path.exists(text):
            f1 = _('Exists')
            f2 = edna_function.get_file_size(text)
            f3 = edna_function.get_file_attr(text)
            f4 = edna_function.get_custom_mimetype(path)
            if os.path.islink(text):
                f5 = _('Link')
                f6 = os.readlink(text)
            else:
                f5 = _('Not link')
                f6 = '--'
        else:
            f1 = _('Not exists')
            f2 = '--'
            f3 = '--'
            f4 = '--'
            f5 = '--'
            f6 = '--'
        
        vbox = gtk.VBox(False, 8)
        hbox1 = gtk.HBox(False)
        vbox2 = gtk.VBox(False, 2)
        vbox3 = gtk.VBox(False, 2)
        
        hbox2 = gtk.HBox(False)
        hbox3 = gtk.HBox(False)
        hbox4 = gtk.HBox(False)
        hbox5 = gtk.HBox(False)
        hbox6 = gtk.HBox(False)
        hbox7 = gtk.HBox(False)
        
        bbox = gtk.HButtonBox()
        
        bbox.set_border_width(5)
        bbox.set_layout(gtk.BUTTONBOX_SPREAD)
        bbox.set_spacing(0)
        
        self.butt_miss = gtk.Button(_('_Miss'))
        self.butt_again = gtk.Button(_('_Repeat'))
        self.butt_miss_all = gtk.Button(_('Miss _All'))
        self.butt_cancel = gtk.Button(stock='gtk-cancel')
        
        bbox.add(self.butt_miss)
        bbox.add(self.butt_again)
        bbox.add(self.butt_miss_all)
        bbox.add(self.butt_cancel)
        
        self.label_mesage = gtk.Label()
        self.label_mesage.set_text(_('Error! I not can read file'))
        self.label_mesage.set_alignment(0.0, 0.5)
        self.label_mesage.set_size_request(350, -1)
        
        self.label_file = gtk.Label()
        self.label_file.set_text(text)
        self.label_file.set_alignment(0.0, 0.5)
        self.label_file.set_size_request(350, -1)
        
        hbox2.pack_start(self.labe_s(_('File'), 0.0))
        hbox2.pack_start(gtk.VSeparator())
        hbox2.pack_start(self.labe_s(f1, 1.0))
        
        hbox3.pack_start(self.labe_s(_('Size'), 0.0))
        hbox3.pack_start(gtk.VSeparator())
        hbox3.pack_start(self.labe_s(f2, 1.0))
        
        hbox4.pack_start(self.labe_s(_('Attributes'), 0.0))
        hbox4.pack_start(gtk.VSeparator())
        hbox4.pack_start(self.labe_s(f3, 1.0))
        
        hbox5.pack_start(self.labe_s(_('Type'), 0.0))
        hbox5.pack_start(gtk.VSeparator())
        hbox5.pack_start(self.labe_s(f4, 1.0))
        
        hbox6.pack_start(self.labe_s(f5, 0.0))
        hbox7.pack_start(self.labe_s(f6, 0.5))
        
        vbox3.pack_start(gtk.HSeparator())
        vbox3.pack_start(hbox2)
        vbox3.pack_start(gtk.HSeparator())
        vbox3.pack_start(hbox3)
        vbox3.pack_start(gtk.HSeparator())
        vbox3.pack_start(hbox4)
        vbox3.pack_start(gtk.HSeparator())
        
        vbox2.pack_start(gtk.HSeparator())
        vbox2.pack_start(hbox5)
        vbox2.pack_start(gtk.HSeparator())
        vbox2.pack_start(hbox6)
        vbox2.pack_start(gtk.HSeparator())
        vbox2.pack_start(hbox7)
        vbox2.pack_start(gtk.HSeparator())
        l = gtk.Label()
        l.set_size_request(30, -1)
        hbox1.pack_start(gtk.VSeparator(), False)
        hbox1.pack_start(vbox3, False)
        hbox1.pack_start(gtk.VSeparator(), False)
        hbox1.pack_start(l, False)
        hbox1.pack_start(gtk.VSeparator(), False)
        hbox1.pack_start(vbox2, True)
        hbox1.pack_start(gtk.VSeparator(), False)
        vbox.pack_start(self.label_mesage)
        vbox.pack_start(self.label_file)
        vbox.pack_start(hbox1)
        vbox.pack_start(bbox)
        self.add(vbox)

    def labe_s(self, text, r):
        lb = gtk.Label()
        if text == None: text = 'none'
        lb.set_text(text)
        lb.set_alignment(r, 0.5)
        lb.set_size_request(100, -1)
        return lb 
        
    def destr(self, *args):
        self.hide()
        self.Exit = True
        self.destroy
    
    def key_event(self, *args):
        key = edna_function.get_key_info(args[1])
        if key == 'Escape': self.destr()
        
        
class copy_window(gtk.Window):
    '''
    Класс окна копирования
    '''
    def __init__(self, dest, list, destpath, current_path, siz, remove_after):
        gtk.Window.__init__(self)
        self.connect('destroy', self.destr)
        self.connect('key-release-event', self.key_event)
        self.Exit = False
        self.Pause = False
        self.Miss = False
        self.set_modal(True)
        self.set_resizable(False)
        vbox = gtk.VBox(False, 2)
        self.set_border_width(5)
        self.remove_after = remove_after
        if self.remove_after:
            self.set_icon(edna_function.get_theme.load_icon('gtk-cut', 20, 0))
        else:
            self.set_icon(edna_function.get_theme.load_icon('gtk-copy', 20, 0))
        self.set_position(gtk.WIN_POS_CENTER)
        self.current_path = current_path
        self.destpath = destpath
        self.dest = dest
        self.list = list
        self.list.reverse()
        self.n = len(list) + len(dest)
        self.count = 0
        self.siz = siz
        self.siz_count = 0
        self.s_count = 0
        self.progress1 = gtk.ProgressBar()
        self.progress1.set_text('0')
        self.progress1.set_size_request(450, -1)
        if len(self.dest) > 1 or os.path.isdir(self.dest[0][0]):
            self.multi = True
            self.progress2 = gtk.ProgressBar()
            self.progress2.set_text('0')
            self.progress2.set_size_request(450, -1)
        else:
            self.multi = False
        self.label_progres = gtk.Label()
        self.label_progres.set_size_request(450, -1)
        self.label_src = gtk.Label()
        self.label_src.set_alignment(0.0, 0.5)
        self.label_src.set_size_request(450, -1)
        self.label_dest = gtk.Label()
        self.label_dest.set_alignment(0.0, 0.5)
        self.label_dest.set_size_request(450, -1)
        tab = gtk.Table(1, 3, True)
        tab.set_col_spacings(30)
        self.butt_cen = gtk.Button(stock='gtk-cancel')
        self.butt_cen.connect('clicked', self.but_destr)
        self.butt_ps = gtk.Button(_('Pause'))
        self.butt_ps.connect('clicked', self.restart)
        tab.attach(gtk.Label(), 0, 1, 0, 1)
        tab.attach(self.butt_cen, 1, 2, 0, 1)
        tab.attach(self.butt_ps, 2, 3, 0, 1)
        vbox.pack_start(self.label_progres)
        vbox.pack_start(gtk.HSeparator())
        vbox.pack_start(self.label_src)
        vbox.pack_start(self.label_dest)
        vbox.pack_start(self.progress1)
        if self.multi:
            vbox.pack_start(self.progress2)
        vbox.pack_start(tab)
        self.add(vbox)
        self.show_all()
        self.timer = threading.Timer(0, self.copy_timer)
        self.timer.start()
        
    def restart(self, *args):
        if self.Pause:
            args[0].set_label(_('Pause'))
            self.timer = threading.Timer(0, self.copy_timer)
            self.timer.start()
        else:
            args[0].set_label(_('Start'))
        self.Pause = not self.Pause
        if self.get_modal():
            self.set_modal(False)
        
    def copy_timer(self):
        if self.count < len(self.list) + 1:
            self.cp_l(self.list, self.count)
            self.cp_l(self.dest, 0)
        else:
            self.cp_l(self.dest, self.count - len(self.list))
        if self.Pause != True:
            self.hide()
            self.destr()
            
    def cp_l(self, args, n):
        if len(args) > 0:
            for i in xrange(n, len(args)):
                if self.Exit == True or self.Pause == True: break
                p = args[i][0][len(self.current_path) + 1:]
                p1 = os.path.join(self.destpath, p)
                gtk.gdk.threads_enter()
                self.label_src.set_text(p)
                self.label_dest.set_text(p1)
                gtk.gdk.threads_leave()
                again = True
                while again:
                    again = self.custom_copy(args[i][0], p1, args[i][1], 10)
                
    def custom_copy(self, src, dst, flag, n):
        '''
        Непосредственно функция копирования
        '''
        if flag:
            src_file, answer = edna_function.save_open(src, 'rb', self.Miss)
            if src_file == None:
                if self.Miss:
                    return False
                else:
                    if answer == 1:
                        return False
                    elif answer == 2:
                        return True
                    elif answer == 3:
                        self.Miss = True
                        return False
                    elif answer == 4:
                        self.but_destr()
                        return False
            
            if os.path.exists(os.path.dirname(dst)) == False: os.makedirs(os.path.dirname(dst))
            if self.s_count > 0:
                dst_file = open(dst, 'ab')
            else:
                dst_file = open(dst, 'wb')
            len_src = os.path.getsize(src)
            block_size = os.statvfs(dst)[0]
            src_file.seek(self.s_count * (block_size * n), 0)
            for i in xrange(self.s_count, len_src // (block_size * n)):
                if self.Exit == True or self.Pause == True: break
                if i % 2 != 0: start_time = time.time()
                dst_file.write(src_file.read(block_size * n))
                if i % 2 != 0: copy_speed = ((block_size * n) / (time.time() - start_time)) // 1024 ** 2
                self.s_count = i + 1
                #time_remain = (self.siz - self.siz_count) / copy_speed
                #if time_remain > 59 and time_remain < 3600:
                #    time_remain = str(round((time_remain / 60), 2)) + ' min'
                #elif time_remain >= 3600:
                #    time_remain = str(round((time_remain / 3600), 2)) + ' hour'
                #else:
                #    time_remain = str(time_remain) + ' sec'
                if i % 2 != 0: 
                    gtk.gdk.threads_enter()  
                    self.label_progres.set_text(str(copy_speed) + ' Kb/c, ')
                    gtk.gdk.threads_leave()
                ds = os.path.getsize(dst)
                self.siz_count += block_size * n
                if self.multi:
                    v1 = ds * 1.00 / len_src
                    v2 = self.siz_count * 1.0 / self.siz
                    v22 = str(int(v2 * 100)) + ' %'
                    gtk.gdk.threads_enter()
                    self.progress2.set_text(str(int(v1 * 100)) + ' %')
                    self.progress2.set_fraction(v1)
                    self.set_title(v22)
                    self.progress1.set_text(v22)
                    self.progress1.set_fraction(v2)
                    gtk.gdk.threads_leave()
                else:
                    v2 = ds * 1.00 / len_src
                    v22 = str(int(v2 * 100)) + ' %'
                    gtk.gdk.threads_enter()
                    self.set_title(v22)
                    self.progress1.set_text(v22)
                    self.progress1.set_fraction(v2)
                    gtk.gdk.threads_leave()
            if self.Exit == False and self.Pause == False:        
                if src_file.tell() != len_src:
                    self.siz_count += len_src - os.path.getsize(dst)
                    dst_file.write(src_file.read())
                self.s_count = 0
                self.count += 1
            src_file.close()
            dst_file.close()
            del src_file
            del dst_file
            return False
        else:
            if os.path.exists(dst) == False:
                try: os.makedirs(dst)
                except: pass
            return False
                
    def but_destr(self, *args):
        self.Exit = True
        if self.Pause: self.destr()
        
    def destr(self, *args):
        self.hide()
        self.Exit = True
        self.destroy
    
    def key_event(self, *args):
        key = edna_function.get_key_info(args[1])
        if key == 'Escape': self.destr()
        
        
class remove_window(gtk.Window):
    '''
    Класс окна удаления
    '''
    def __init__(self, dest, list):
        gtk.Window.__init__(self)
        self.connect('destroy', self.destr)
        self.connect('key-release-event', self.key_event)
        self.set_resizable(False)
        self.set_modal(True)
        vbox = gtk.VBox(False, 5)
        self.set_border_width(5)
        self.Exit = False
        self.Pause = False
        self.set_title(_('Delete'))
        self.set_icon(edna_function.get_theme.load_icon('gtk-clear', 20, 0))
        self.set_position(gtk.WIN_POS_CENTER)
        self.dest = dest
        self.list = list
        self.list.reverse()
        self.n = len(list) + len(dest)
        self.count = 0
        self.progress1 = gtk.ProgressBar()
        self.progress1.set_text('0')
        self.progress1.set_size_request(450, -1)
        self.label_progres = gtk.Label()
        self.label_src = gtk.Label()
        self.label_src.set_size_request(450, -1)
        tab = gtk.Table(1, 3, True)
        tab.set_col_spacings(30)
        self.butt_cen = gtk.Button(stock='gtk-cancel')
        self.butt_cen.connect('clicked', self.but_destr)
        self.butt_ps = gtk.Button(_('_Pause'))
        self.butt_ps.connect('clicked', self.restart)
        tab.attach(gtk.Label(), 0, 1, 0, 1)
        tab.attach(self.butt_cen, 1, 2, 0, 1)
        tab.attach(self.butt_ps, 2, 3, 0, 1)
        vbox.pack_start(self.label_progres)
        vbox.pack_start(gtk.HSeparator())
        vbox.pack_start(self.label_src)
        vbox.pack_start(self.progress1)
        vbox.pack_start(tab)
        self.timer = threading.Timer(0, self.copy_timer)
        self.add(vbox)
        self.show_all()
        self.timer.start()
        
    def copy_timer(self):
        if self.count < len(self.list) + 1:
            self.del_l(self.list, self.count)
            self.del_l(self.dest, 0)
        else:
            self.del_l(self.dest, self.count - len(self.list))
        if self.Pause != True:
            self.hide()
            self.destr()
            
    def del_l(self, args, n):
        if len(args) > 0:
            for i in xrange(n, len(args)):
                if self.Exit == True or self.Pause == True: break
                gtk.gdk.threads_enter()
                self.label_src.set_text(args[i][0])
                gtk.gdk.threads_leave()
                edna_function.deleting_files_folders(args[i][0], args[i][1])
                self.count += 1
                gtk.gdk.threads_enter()
                self.progress1.set_text(str(int((self.count * 1.00 / self.n) * 100)) + ' %')
                self.progress1.set_fraction(self.count * 1.0 / self.n)
                gtk.gdk.threads_leave()
                
    def restart(self, *args):
        if self.Pause:
            args[0].set_label(_('_Pause'))
            self.timer = threading.Timer(0, self.copy_timer)
            self.timer.start()
        else:
            args[0].set_label(_('_Start'))
        self.Pause = not self.Pause
        if self.get_modal():
            self.set_modal(False)
        
    def del_l(self, args, n):
        if len(args) > 0:
            for i in xrange(n, len(args)):
                if self.Exit == True or self.Pause == True: break
                gtk.gdk.threads_enter()
                self.label_src.set_text(args[i][0])
                gtk.gdk.threads_leave()
                edna_function.deleting_files_folders(args[i][0], args[i][1])
                self.count += 1
                gtk.gdk.threads_enter()
                self.progress1.set_text(str(int((self.count * 1.00 / self.n) * 100)) + ' %')
                self.progress1.set_fraction(self.count * 1.0 / self.n)
                gtk.gdk.threads_leave()
        
    def but_destr(self, *args):
        self.Exit = True
        if self.Pause: self.destr()
        
    def destr(self, *args):
        self.hide()
        self.Exit = True
        self.destroy
        
    def key_event(self, *args):
        key = edna_function.get_key_info(args[1])
        if key == 'Escape': self.destr()        
        
        
class question_window(gtk.Window):
    '''
    Класс окна вопроса перед удалением
    '''
    def __init__(self, list):
        gtk.Window.__init__(self)
        self.connect('destroy', self.destr)
        self.connect('key-release-event', self.key_event)
        self.set_resizable(False)
        self.set_modal(True)
        vbox = gtk.VBox(False, 2)
        vbox.set_spacing(3)
        self.set_border_width(5)
        hbox = gtk.HBox(False, 2)
        hbox.set_spacing(10)
        self.set_title(self_name)
        self.icon_image = gtk.Image()
        pix = edna_function.get_theme.load_icon('gtk-help', 50, 0)
        self.icon_image.set_from_pixbuf(pix)
        self.set_icon(pix)
        self.set_position(gtk.WIN_POS_CENTER)
        target_list = ''
        if len(list) > 1:
            if len(list) > 4:
                for i in xrange(4):
                    p = list[i][0][len(os.path.dirname(list[0][0])):] + '\n'
                    if p[0] == '/': p = p[1:]
                    target_list += p
                target_list += '...'
            else:
                for i in xrange(len(list)):
                    p = list[i][0][len(os.path.dirname(list[0][0])):] + '\n'
                    if p[0] == '/': p = p[1:]
                    target_list += p
            target = _('files/folders (%d th.)?:\n' % len(list))
        else:
            if list[0][1]:
                target = _('file') + ' '
            else:
                target = _('folder') + ' '
            p = list[0][0][len(os.path.dirname(list[0][0])):]
            if p[0] == '/': p = p[1:]
            target_list += p + '?'
        text = _('You want to delete') + '\n%s%s' % (target, target_list)
        self.label_question = gtk.Label(text)
        self.label_question.set_alignment(0.0, 0.0)
        hbbox = gtk.HButtonBox()
        hbbox.set_layout(gtk.BUTTONBOX_SPREAD)
        #hbbox.set_spacings(10)
        self.butt_ok = gtk.Button(stock='gtk-ok')
        self.butt_cancel = gtk.Button(stock='gtk-cancel')
        self.butt_ok.connect('clicked', self.ok_button_click, list)
        self.butt_cancel.connect('clicked', self.destr)
        hbbox.pack_start(self.butt_ok)
        hbbox.pack_start(self.butt_cancel)
        hbox.pack_start(self.icon_image)
        hbox.pack_start(self.label_question)
        vbox.pack_start(hbox)
        vbox.pack_start(hbbox)
        self.add(vbox)
        self.show_all()
        
    def ok_button_click(self, *args):
        k = []
        for i in args[1]:
                if i[1] == False:
                    if os.path.isdir(i[0]):
                        k += edna_function.get_full_size(i[0], True)[1]
        self.hide()
        r = remove_window(args[1], k)
        self.destr()
    
    def destr(self, *args):
        self.hide()
        self.destroy
        
    def key_event(self, *args):
        key = edna_function.get_key_info(args[1])
        if key == 'Escape': self.destr()
        
        
class question_window_copy(gtk.Window):
    '''
    Класс окна вопроса перед копированием
    '''
    def __init__(self, destpath, current_path, list, remove_after):
        gtk.Window.__init__(self)
        self.destpath = destpath
        self.remove_after = remove_after
        self.set_modal(True)
        self.connect('destroy', self.destr)
        self.connect('key-release-event', self.key_event)
        if self.remove_after:
            self.set_icon(edna_function.get_theme.load_icon('gtk-cut', 20, 0))
        else:
            self.set_icon(edna_function.get_theme.load_icon('gtk-copy', 20, 0))
        self.set_resizable(False)
        vbox = gtk.VBox(False, 2)
        vbox.set_spacing(3)
        self.set_border_width(5)
        self.list = list
        self.current_path = current_path
        self.set_title(self_name)
        self.set_position(gtk.WIN_POS_CENTER)
        text = _('To copy %s files/folders in' % len(list))
        label_question = gtk.Label(text)
        label_question.set_alignment(0.0, 0.0)
        self.entry1 = gtk.Entry()
        #self.connect('key-release-event', self.key_event)
        self.entry1.set_size_request(250, -1)
        self.entry1.set_text(destpath)
        hbbox = gtk.HButtonBox()
        hbbox.set_layout(gtk.BUTTONBOX_SPREAD)
        #hbbox.set_spacings(10)
        self.butt_ok = gtk.Button(stock='gtk-ok')
        self.butt_cancel = gtk.Button(stock='gtk-cancel')
        self.butt_ok.connect('clicked', self.ok_button_click)
        self.butt_cancel.connect('clicked', self.destr)
        hbbox.pack_start(self.butt_ok)
        hbbox.pack_start(self.butt_cancel)
        vbox.pack_start(label_question)
        vbox.pack_start(self.entry1)
        vbox.pack_start(hbbox)
        self.add(vbox)
        self.show_all()
        
    def ok_button_click(self, *args):
        k = []
        siz = 0
        for i in self.list:
                if i[1]:
                    siz += os.path.getsize(i[0])
                else:
                    if os.path.isdir(i[0]):
                        buf = edna_function.get_full_size(i[0], True)
                        k += buf[1]
                        siz += buf[0]
        self.hide()
        r = copy_window(self.list, k, self.destpath, self.current_path, siz, self.remove_after)
        self.destr()
    
    def destr(self, *args):
        self.hide()
        self.destroy
        
    def key_event(self, *args):
        key = edna_function.get_key_info(args[1])
        if key == 'Escape': self.destr()
        if key == 'Return': self.ok_button_click()
            
            
class properties_file_window(gtk.Window):
    '''
    Класс окна "свойства файла"
    '''
    class info_row(gtk.HBox):
        '''
        Информационная строка 
        '''
        def __init__(self, head_text, text):
            gtk.HBox.__init__(self, False, 10)
            head_label = gtk.Label(head_text + ':')
            head_label.modify_font(pango.FontDescription('bold'))
            self.pack_start(head_label, False)
            text_label = gtk.Label(text)
            self.pack_start(text_label, False)
            
    def __init__(self, path_to_file):
        gtk.Window.__init__(self)
        self.path_to_file = path_to_file[0]
        self.is_file = path_to_file[1]
        self.get_info_about_file()
        self.set_size_request(330, 400)
        self.set_border_width(5)
        self.set_title(_('File properties'))
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_resizable(False)
        vbox1 = gtk.VBox(False)
        note1 = gtk.Notebook()
        self.create_properties_tab(note1)
        self.create_access_tab(note1)
        vbox1.pack_start(note1)
        hbox1 = gtk.HButtonBox()
        hbox1.set_layout(gtk.BUTTONBOX_END)
        self.button_ok = gtk.Button(stock='gtk-ok')
        self.button_cancel = gtk.Button(stock='gtk-cancel')
        self.button_apply = gtk.Button(stock='gtk-apply')
        hbox1.add(self.button_ok)
        hbox1.add(self.button_cancel)
        hbox1.add(self.button_apply)
        vbox1.pack_start(hbox1, False)
        self.add(vbox1)
        self.show_all()
             
    def get_info_about_file(self):
        '''
        Создание списка свойств для отображения
        '''
        self.info_about_file = {}
        k = os.path.dirname(self.path_to_file)
        if k != '/': null_p = 1
        else: null_p = 0
        self.info_about_file['Path'] = self.path_to_file
        self.info_about_file['Name'] = self.path_to_file[len(k) + null_p:]
        self.info_about_file['File'] = self.is_file
        self.info_about_file['Datec'] = edna_function.get_file_date(self.path_to_file, 'cell_datec_format')
        self.info_about_file['Datem'] = edna_function.get_file_date(self.path_to_file, 'cell_datem_format')
        
        if self.is_file:
            self.info_about_file['Type'] = edna_function.get_mime(self.path_to_file, self.info_about_file['File'])
            self.info_about_file['Icon'] = edna_function.get_ico(self.info_about_file['Type'], False)
            self.info_about_file['Size'] = edna_function.get_file_size(self.path_to_file)
            self.info_about_file['App'] = edna_function.get_launch_apps(self.path_to_file)[0]
            
        else:
            self.info_about_file['Type'] = 'application/octet-stream'
            self.info_about_file['Icon'] = edna_function.get_ico('gtk-directory', False)
            self.info_about_file['Size'] = '0'
            
    def get_size_in_thread(self):
        '''
        Поток определения размера каталога в фоновом режиме
        '''
        print 'fdsf'
        #self.text_label_size_dir.set_text(edna_function.get_in_format_size(edna_function.get_full_size(self.path_to_file)))
        edna_function.get_in_format_size(edna_function.get_full_size_in_thread(self.path_to_file, self.text_label_size_dir))
        
    def create_properties_tab(self, note_object):
        '''
        Создание и заполнение вкладки Свойства
        '''
        vbox2 = gtk.VBox(False, 15)
        vbox2.set_border_width(20)
        hbox1 = gtk.HBox(False, 10)
        vbox3 = gtk.VBox(False, 5)
        vbox4 = gtk.VBox(False, 5)
        
        icon_image = gtk.Image()
        icon_image1 = gtk.Button()
        icon_image.set_from_pixbuf(self.info_about_file['Icon'])
        icon_image1.set_image(icon_image)
        
        entry_name = gtk.Entry()
        entry_name.set_text(self.info_about_file['Name'])
        entry_name.connect('changed', self.change_entry_name)
        vbox3.pack_start(self.info_row(_('Type'), self.info_about_file['Type']), False)
        if self.is_file:
            vbox3.pack_start(self.info_row(_('Size'), self.info_about_file['Size']), False)
        else:
            size_hbox1 = gtk.HBox(False, 10)
            head_label = gtk.Label(_('Size') + ':')
            head_label.modify_font(pango.FontDescription('bold'))
            size_hbox1.pack_start(head_label, False)
            self.text_label_size_dir = gtk.Label(self.info_about_file['Size'])
            size_hbox1.pack_start(self.text_label_size_dir, False)
            vbox3.pack_start(size_hbox1, False)
            self.timer_size = threading.Timer(0, self.get_size_in_thread)
            self.timer_size.start()
        
        vbox4.pack_start(self.info_row(_('Created'), self.info_about_file['Datec']), False)    
        vbox4.pack_start(self.info_row(_('Changed'), self.info_about_file['Datem']), False)    
        hbox1.pack_start(icon_image1, False)
        hbox1.pack_start(entry_name)
        vbox2.pack_start(hbox1, False)
        vbox2.pack_start(gtk.HSeparator(), False)
        vbox2.pack_start(vbox3, False)
        vbox2.pack_start(gtk.HSeparator(), False)
        vbox2.pack_start(vbox4, False)
        note_object.append_page(vbox2, gtk.Label(_('Properties')))
    
    def change_entry_name(self, *args):
        '''
        Изминение виджета entry_name
        '''
        self.info_about_file['Name'] = args[0].get_text()
    
    def create_access_tab(self, note_object):
        '''
        Создание и заполнение вкладки Доступ
        '''
        vbox2 = gtk.VBox(False)
        note_object.append_page(vbox2, gtk.Label(_('Access')))
        
class File_Cells(gtk.TreeView):
    '''
    Класс списка файлов
    '''
    def __init__(self, n, path_entry=gtk.Label):
        gtk.TreeView.__init__(self)
        self.set_rules_hint(True)
        self.set_grid_lines(False)
        self.path_entry = path_entry
        self.Hotkeys_Function = {'key_1': self.copys,
                                'key_2': self.deleting,
                                'key_3': self.properties_file,
                                'key_4': '',
                                'key_5': '',
                                'key_6': '',
                                'key_7': ''}
        self.get_selection().set_mode(gtk.SELECTION_SINGLE)
        self.OOF = edna_function.Object_of_Files()
        self.OOF.add_path(edna_function.rc_dict['config']['panel_history%d' % n])
        self.path_entry.set_text(self.OOF.Path.get_path())
        self.connect('key-release-event', self.key_event)
        self.connect('key-press-event', self.key_event)
        self.connect('button-press-event', self.pr)
        self.connect('cursor-changed', self.cursor_changed)
        
    def Cells_Refresh(self):
        '''
        Обновление списка файлов
        '''
        #self.style('even-row-color', gtk.gdk.Color('#D51A1A'))
        #self.style.set_property('even-row-color', gtk.gdk.Color('#4A6AA0'))
        #self.set_property('enable-tree-lines', False)
        self.set_model(self.OOF.Model)
        self.__add_columns()
        self.modify_base(gtk.STATE_NORMAL, gtk.gdk.Color(edna_function.rc_dict['style']['even_row_bg']))
        #self.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_VERTICAL)
        #self.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)
        
    def cursor_changed(self, *args):
        selection = self.get_selection()
        model_sel, iter_sel = selection.get_selected()
        self.OOF.pattern_s = model_sel.get_value(iter_sel, self.OOF.len_Sum_cell)
        
    def get_select_now(self, only_cursor=False):
        '''
        Создаеться список выделеных файлов и папок
        '''
        return_list = []
        selection = self.get_selection()
        model_sel, iter_sel = selection.get_selected()
        if only_cursor:
            dp = model_sel.get_value(iter_sel, self.OOF.Length_Table)
            if dp != '..':
                return dp, os.path.isfile(dp)
            else:
                return None
        else:
            path = model_sel.get_path(iter_sel)[0]
            model = self.get_model()
            if self.OOF.Path != '/':
                nc = 1
            else:
                nc = 0
            now_select_in = True
            for i in xrange(nc, self.len_articles):
                iter = model.get_iter(i)
                if model.get_value(iter, self.OOF.Length_Table + 4) == 'True':
                    if path == i: now_select_in = False
                    dp = model.get_value(iter, self.OOF.Length_Table)
                    return_list.append([dp, os.path.isfile(dp)])
            dp = model_sel.get_value(iter_sel, self.OOF.Length_Table)
            if now_select_in and dp != '..':
                return_list.append([dp, os.path.isfile(dp)])
            return return_list
            
    def key_event(self, *args):
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
        input_list = self.get_select_now()
        model_sel, iter_sel = self.get_selection().get_selected()
        p = model_sel.get_value(iter_sel, self.OOF.Length_Table)
        if len(input_list) == 1 or p == '..' or os.path.isdir(p) == True:
            self.chdir_new()
        elif len(input_list) == 0:
            self.back_dir()
        else:
            list_lanch = {}
            for i in input_list:
                if i[1]:
                    ret = edna_function.get_launch(i[0])
                    if ret:
                        r_name = ret.get_name()
                        try:
                            list_lanch.keys().index(r_name)
                        except:
                            list_lanch[r_name] = {'app': ret, 'list':[gio.File(i[0]).get_uri()]}
                        else:
                            list_lanch[r_name]['list'].append(gio.File(i[0]).get_uri())
            for i in input_list:
                if i[1] == False:
                    if os.path.isdir(i[0]):
                        self.OOF.add_path(i[0])
                        self.path_entry.set_text(self.OOF.Path)
                        self.set_model(self.OOF.Model)
                        self.set_cursor(self.return_select)
                    break
            for i in list_lanch.keys():
                list_lanch[i]['app'].launch_uris(list_lanch[i]['list'], None)
                #subprocess.Popen(i + list_lanch[i], shell=True)
                
    def deleting(self):
        y = question_window(self.get_select_now())
        
    def properties_file(self):
        '''
        Свойства файла
        '''
        rlist = self.get_select_now(only_cursor=True)
        if rlist:
            y = properties_file_window(rlist)
        
    def copys(self):
        '''
        Копирование
        '''
        remove_after = False
        y = question_window_copy(self.return_path_cell(self.n), self.OOF.Path, self.get_select_now(), remove_after)
    
    def select_function(self, key):
        selection = self.get_selection()
        model, iter = selection.get_selected()
        path = model.get_path(iter)[0]
        sel_col = {}
        if model.get_value(iter, self.OOF.Length_Table + 4) == 'True':
            if path % 2:
                ts = 'odd'
            else:
                ts = 'even'
                
            sel_col['fg'] = edna_function.rc_dict['style']['%s_row_fg' % ts]
            sel_col['bg'] = edna_function.rc_dict['style']['%s_row_bg' % ts]
            try: self.Select_List.remove(model.get_value(iter, self.OOF.Length_Table))
            except: pass
            self.OOF.Table_of_File[path][self.OOF.Length_Table + 4] = 'False'
        else:
            sel_col['fg'] = edna_function.rc_dict['style']['sel_row_fg']
            sel_col['bg'] = edna_function.rc_dict['style']['sel_row_bg']
            self.OOF.Table_of_File[path][self.OOF.Length_Table + 4] = 'True'
            self.Select_List.append(model.get_value(iter, self.OOF.Length_Table))
        f = ['fg', 'bg']
        model.set(iter, self.OOF.Length_Table + 4, self.OOF.Table_of_File[path][self.OOF.Length_Table + 4])
        for i in xrange(len(f)):
            self.OOF.Table_of_File[path][self.OOF.Length_Table + 2 + i] = sel_col[f[i]]
            model.set(iter, self.OOF.Length_Table + 2 + i, self.OOF.Table_of_File[path][self.OOF.Length_Table + 2 + i])
        cellse = edna_function.Sum_cell
        if key == 'space':
            try:
                ic = cellse.index('cell_size')
            except:
                pass
            else:
                n = model.get_value(iter, self.OOF.Length_Table)
                if os.path.isdir(n):
                    self.OOF.Table_of_File[path][ic] = edna_function.get_in_format_size(edna_function.get_full_size(n))
                    model.set(iter, ic, self.OOF.Table_of_File[path][ic])
            
    def pr(self, *args):
        if args[1].type == gtk.gdk._2BUTTON_PRESS:
            self.chdir_new()
            
    def back_dir(self):
        if self.OOF.get_curent_path().get_path() != '/':
            self.OOF.gio_activation(self.OOF.Path.get_parent().get_uri())
            self.set_model(self.OOF.Model)
            #self.treeview.set_cursor(self.return_select)
                    
    def chdir_new(self):
        '''
        Действие при активации пункта списка
        '''
        selection = self.get_selection()
        model, iter = selection.get_selected()        
        dp = model.get_value(iter, self.OOF.Path_Index)
        self.OOF.gio_activation(dp)
        self.set_model(self.OOF.Model)
        #self.set_cursor(self.return_select)
            
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
                column.set_attributes(renderer, pixbuf=0)
            else:
                column = gtk.TreeViewColumn(Name_Colum[u[i]], renderer, text=i + 1, background=self.OOF.Background_Index, foreground=self.OOF.Foreground_Index)
            column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
            column.expand = True
            column.set_min_width(int(edna_function.rc_dict['style']['%s_size' % u[i]]))
            
            renderer = gtk.CellRendererText()
            #renderer.set_data(Name_Colum[u[i]], i)
            renderer.set_alignment(alg[0], alg[1])
            renderer.set_property('background-set' , True)
            renderer.set_property('foreground-set' , True)
            renderer.set_property('font-desc' , pango.FontDescription(edna_function.rc_dict['style']['font_cell_text']))
            
            if u[i] == 'cell_name':
                column.pack_start(renderer, True)
                column.set_attributes(renderer, text=i + 1, background=self.OOF.Background_Index, foreground=self.OOF.Foreground_Index)
                
            itk = int(edna_function.rc_dict['style']['%s_expand' % u[i]])
            column.set_expand(itk)
            self.append_column(column)
    
    
    
class listen_cell(gtk.VBox):
    '''
    Класс панели содкржащей списки файлов
    '''
    def __init__(self, n, return_path_cell):
        gtk.VBox.__init__(self, False, 3)
        self.pattern_s = ''
        self.n = n
        self.return_path_cell = return_path_cell
        #self.Cursor = 0
        self.Focus_State = True
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
        self.treeview = File_Cells(n, self.path_entry)
        self.info_label = gtk.Label('info')
        ###################################
        self.scrol.add(self.treeview)
        self.upData()
        self.pack_start(self.drive_info_label, False)
        self.pack_start(self.evtb, False)
        self.pack_start(self.scrol)
        self.pack_start(self.info_label, False)
        #self.Timer_func = threading.Timer(0, self.timer_refresh)
        #self.Timer_func.start()
        
    def upData(self):
        self.evtb.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(edna_function.rc_dict['style']['even_row_bg']))
        self.evtb.modify_font(pango.FontDescription(edna_function.rc_dict['style']['font_cell_text']))
        self.path_entry.modify_fg(gtk.STATE_NORMAL, gtk.gdk.Color(edna_function.rc_dict['style']['even_row_fg']))
        self.treeview.Cells_Refresh()
            
################################  Gui class (end) #############################
def main():
    h = properties_file_window(['/home/mort/Box', False])
    #h = miss_window('/home/mort/.bashrc')
    h.show_all()
    gtk.main()
    return 0

if __name__ == '__main__':
    main()

