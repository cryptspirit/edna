#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#       gui_class_main.py
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
import rc_modul
import edna_function
import pango
import os
import re
import gio
import subprocess
import threading
import time
import filecmp
import mimetypes

self_name = 'Edna'

class miss_window(gtk.Window):
    def __init__(self, text):
        gtk.Window.__init__(self)
        self.connect('destroy', self.destr)
        self.connect('key-release-event', self.key_event)
        self.set_resizable(False)
        self.set_border_width(5)
        self.set_icon(edna_function.get_theme.load_icon('gtk-dialog-info', 20, 0))
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_title(rc_modul.locale['Error_Read_File'])
        
        if os.path.exists(text):
            f1 = rc_modul.locale['Exists']
            f2 = edna_function.get_file_size(text)
            f3 = edna_function.get_file_attr(text)
            f4 = mimetypes.guess_type(text)[0]
            if os.path.islink(text):
                f5 = rc_modul.locale['Link']
                f6 = os.readlink(text)
            else:
                f5 = rc_modul.locale['Notlink']
                f6 = '--'
        else:
            f1 = rc_modul.locale['Notexists']
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
        
        self.butt_miss = gtk.Button(rc_modul.locale['Button_Miss'])
        self.butt_again = gtk.Button(rc_modul.locale['Button_Again'])
        self.butt_miss_all = gtk.Button(rc_modul.locale['Button_Miss_All'])
        self.butt_cancel = gtk.Button(stock='gtk-cancel')
        
        bbox.add(self.butt_miss)
        bbox.add(self.butt_again)
        bbox.add(self.butt_miss_all)
        bbox.add(self.butt_cancel)
        
        self.label_mesage = gtk.Label()
        self.label_mesage.set_text(rc_modul.locale['Error_Read_File'])
        self.label_mesage.set_alignment(0.0, 0.5)
        self.label_mesage.set_size_request(350, -1)
        
        self.label_file = gtk.Label()
        self.label_file.set_text(text)
        self.label_file.set_alignment(0.0, 0.5)
        self.label_file.set_size_request(350, -1)
        
        hbox2.pack_start(self.labe_s(rc_modul.locale['File'], 0.0))
        hbox2.pack_start(gtk.VSeparator())
        hbox2.pack_start(self.labe_s(f1, 1.0))
        
        hbox3.pack_start(self.labe_s(rc_modul.locale['Cell_Size'], 0.0))
        hbox3.pack_start(gtk.VSeparator())
        hbox3.pack_start(self.labe_s(f2, 1.0))
        
        hbox4.pack_start(self.labe_s(rc_modul.locale['Cell_Atr'], 0.0))
        hbox4.pack_start(gtk.VSeparator())
        hbox4.pack_start(self.labe_s(f3, 1.0))
        
        hbox5.pack_start(self.labe_s(rc_modul.locale['Cell_Type'], 0.0))
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
    def __init__(self, dest, list, ref_list, destpath, current_path, siz, remove_after):
        gtk.Window.__init__(self)
        self.connect('destroy', self.destr)
        self.connect('key-release-event', self.key_event)
        self.Exit = False
        self.Pause = False
        self.Miss = False
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
        self.ref_list = ref_list
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
        self.butt_ps = gtk.Button(rc_modul.locale['Pause'])
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
            args[0].set_label(rc_modul.locale['Pause'])
            self.timer = threading.Timer(0, self.copy_timer)
            self.timer.start()
        else:
            args[0].set_label(rc_modul.locale['Start'])
        self.Pause = not self.Pause
            
    def copy_timer(self):
        if self.count < len(self.list) + 1:
            self.cp_l(self.list, self.count)
            self.cp_l(self.dest, 0)
        else:
            self.cp_l(self.dest, self.count - len(self.list))
        if self.Pause != True:
            self.hide()
            self.destr()
            self.ref_list()
            
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
    def __init__(self, dest, list, ref_list):
        gtk.Window.__init__(self)
        self.connect('destroy', self.destr)
        self.connect('key-release-event', self.key_event)
        self.set_resizable(False)
        vbox = gtk.VBox(False, 5)
        self.set_border_width(5)
        self.Exit = False
        self.Pause = False
        self.set_title(rc_modul.locale['Remove'])
        self.set_icon(edna_function.get_theme.load_icon('gtk-clear', 20, 0))
        self.set_position(gtk.WIN_POS_CENTER)
        self.ref_list = ref_list
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
        self.butt_ps = gtk.Button(rc_modul.locale['Pause'])
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
            self.ref_list()
            
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
            args[0].set_label(rc_modul.locale['Pause'])
            self.timer = threading.Timer(0, self.copy_timer)
            self.timer.start()
        else:
            args[0].set_label(rc_modul.locale['Start'])
        self.Pause = not self.Pause
        
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
    def __init__(self, list, ref_list):
        gtk.Window.__init__(self)
        self.connect('destroy', self.destr)
        self.connect('key-release-event', self.key_event)
        self.set_resizable(False)
        vbox = gtk.VBox(False, 2)
        vbox.set_spacing(3)
        self.set_border_width(5)
        hbox = gtk.HBox(False, 2)
        hbox.set_spacing(10)
        self.ref_list = ref_list
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
            target = rc_modul.locale['Files'] + '/' + rc_modul.locale['Folders'] + ' (' + str(len(list)) + ' ' + rc_modul.locale['Counts'] + ')' + '?:\n'
        else:
            if list[0][1]:
                target = rc_modul.locale['File'] + ' '
            else:
                target = rc_modul.locale['Folder'] + ' '
            p = list[0][0][len(os.path.dirname(list[0][0])):]
            if p[0] == '/': p = p[1:]
            target_list += p + '?'
        text = rc_modul.locale['Remove_Question'] + '\n' + target + target_list
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
        r = remove_window(args[1], k, self.ref_list)
        self.destr()
    
    def destr(self, *args):
        self.hide()
        self.destroy
        
    def key_event(self, *args):
        key = edna_function.get_key_info(args[1])
        if key == 'Escape': self.destr()
        
        
class question_window_copy(gtk.Window):
    def __init__(self, destpath, current_path, list, ref_list, remove_after):
        gtk.Window.__init__(self)
        self.destpath = destpath
        self.remove_after = remove_after
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
        self.ref_list = ref_list
        self.list = list
        self.current_path = current_path
        self.set_title(self_name)
        self.set_position(gtk.WIN_POS_CENTER)
        text = rc_modul.locale['Copy_Question'] + ' ' + str(len(list)) + ' ' + rc_modul.locale['Files'] + '/' + rc_modul.locale['Folders'] + ' ' + rc_modul.locale['In'] 
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
        r = copy_window(self.list, k, self.ref_list, self.destpath, self.current_path, siz, self.remove_after)
        self.destr()
    
    def destr(self, *args):
        self.hide()
        self.destroy
        
    def key_event(self, *args):
        key = edna_function.get_key_info(args[1])
        if key == 'Escape': self.destr()
        if key == 'Return': self.ok_button_click()
            
class listen_cell(gtk.VBox):
    def __init__(self, n, locale_dict, rc_dict, return_path_cell):
        gtk.VBox.__init__(self, False, 3)
        self.pattern_s = ''
        self.n = n
        self.return_path_cell = return_path_cell
        self.Cursor = 0
        self.Select_List = []
        ####################################
        self.rc_dict = rc_dict
        rc_modul.locale = locale_dict
        self.Current_Path = self.rc_dict['Panel_History' + str(n)]
        ####################################
        self.scrol = gtk.ScrolledWindow()
        self.scrol.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        self.scrol.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        ###################################
        self.drive_info_label = gtk.Label('drive')
        ###################################
        self.path_entry = gtk.Label()
        #self.path_entry.set_size_request(-1, 17)
        self.evtb = gtk.EventBox()
        self.evtb.add(self.path_entry)
        #self.evtb.set_border_width(3)
        self.evtb.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(self.rc_dict['Even_Row_BG']))
        self.path_entry.modify_fg(gtk.STATE_NORMAL, gtk.gdk.Color(self.rc_dict['Even_Row_FG']))
        self.path_entry.set_alignment(0.0, 0.5)
        self.path_entry.set_text(self.Current_Path)
        ###################################
        model = self.__create_model()
        self.treeview = gtk.TreeView(model)
        self.treeview.set_rules_hint(True)
        self.treeview.set_grid_lines(False)
        #self.treeview.style('even-row-color', gtk.gdk.Color('#D51A1A'))
        self.treeview.modify_base(gtk.STATE_NORMAL, gtk.gdk.Color(self.rc_dict['Even_Row_BG']))
        #self.treeview.style.set_property('even-row-color', gtk.gdk.Color('#4A6AA0'))
        #self.treeview.set_property('enable-tree-lines', False)
        self.treeview.get_selection().set_mode(gtk.SELECTION_SINGLE)
        self.treeview.connect('key-release-event', self.key_event)
        self.treeview.connect('key-press-event', self.key_event)
        self.treeview.connect('button-press-event', self.pr)
        self.treeview.connect('focus-in-event', self.focus_trap)
        self.treeview.connect('focus-out-event', self.focus_trap)
        self.__add_columns(self.treeview)
        self.treeview.set_model(model)
        ###################################
        self.info_label = gtk.Label('info')
        ###################################
        self.scrol.add(self.treeview)
        self.upData(self.rc_dict)
        self.pack_start(self.drive_info_label, False)
        self.pack_start(self.evtb, False)
        self.pack_start(self.scrol)
        self.pack_start(self.info_label, False)
        
    def focus_trap(self, *args):
        #self.treeview.set_cursor(self.treeview.is_focus())
        #if self.treeview.is_focus():
        #    self.treeview.set_hover_selection(False)
        #    self.treeview.set_cursor(self.Cursor)
        #else:
        #    self.Cursor = self.treeview.get_cursor()[0]
        #    #self.treeview.set_cursor(0, None, False)
        #    self.treeview.set_hover_selection(True)
        pass
            
    def ch_dir_entry(self, path):
        self.Current_Path = path
        self.Select_List = []
        self.path_entry.set_text(self.Current_Path)
        
    def get_select_now(self):
        return_list = []
        selection = self.treeview.get_selection()
        model_sel, iter_sel = selection.get_selected()
        path = model_sel.get_path(iter_sel)[0]
        model = self.treeview.get_model()
        
        if self.Current_Path != '/':
            nc = 1
        else:
            nc = 0
        now_select_in = True
        for i in xrange(nc, self.len_articles):
            iter = model.get_iter(i)
            if model.get_value(iter, self.len_u + 4) == 'True':
                if path == i: now_select_in = False
                dp = model.get_value(iter, self.len_u)
                return_list.append([dp, os.path.isfile(dp)])
        dp = model_sel.get_value(iter_sel, self.len_u)
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
            if key == 'Right': self.chdir_new()
            if key == 'Return': self.Enter_key()
            if (key == 'BackSpace' or key == 'Left') and self.Current_Path != '/': self.back_dir()
            if key == 'Delete' or key == 'Shift Delete': self.deleting(key)
            if key == 'F5' : self.copys(False)
            
    def Enter_key(self):
        input_list = self.get_select_now()
        model_sel, iter_sel = self.treeview.get_selection().get_selected()
        #u = rc_modul.Sum_cell(self.rc_dict)
        p = model_sel.get_value(iter_sel, self.len_u)
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
                        try:
                            list_lanch.keys().index(ret)
                        except:
                            list_lanch[ret] = ' \'' + i[0]  + '\''
                        else:
                            list_lanch[ret] += ' \'' + i[0]  + '\''
                            
            for i in input_list:
                if i[1] == False:
                    if os.path.isdir(i[0]):
                        self.pattern_s = ''
                        self.ch_dir_entry(i[0])
                        model = self.__create_model()
                        self.treeview.set_model(model)
                        self.treeview.set_cursor(self.return_select)
                    break
            for i in list_lanch.keys():
                subprocess.Popen(i + list_lanch[i], shell=True)
                
    def deleting(self, key):
        y = question_window(self.get_select_now(), self.ref_list)
        
    def copys(self, remove_after):
        y = question_window_copy(self.return_path_cell(self.n), self.Current_Path, self.get_select_now(), self.ref_list, remove_after)
    
    def ref_list(self):
        time.sleep(0.5)
        selection = self.treeview.get_cursor()[0][0]
        model = self.__create_model()
        self.treeview.set_model(model)
        self.treeview.set_cursor(self.return_select)
        if self.return_select == 0:
            self.treeview.set_cursor(selection)
        else:
            self.treeview.set_cursor(self.return_select)
        
    def select_function(self, key):
        selection = self.treeview.get_selection()
        model, iter = selection.get_selected()
        path = model.get_path(iter)[0]
        sel_col = {}
        if model.get_value(iter, self.len_u + 4) == 'True':
            if path % 2:
                ts = 'Odd'
            else:
                ts = 'Even'
                
            sel_col['FG'] = self.rc_dict[ts + '_Row_FG']
            sel_col['BG'] = self.rc_dict[ts + '_Row_BG']
            try: self.Select_List.remove(model.get_value(iter, self.len_u))
            except: pass
            self.articles[path][self.len_u + 4] = 'False'
        else:
            sel_col['FG'] = self.rc_dict['Sel_Row_FG']
            sel_col['BG'] = self.rc_dict['Sel_Row_BG']
            self.articles[path][self.len_u + 4] = 'True'
            self.Select_List.append(model.get_value(iter, self.len_u))
        f = ['FG', 'BG']
        model.set(iter, self.len_u + 4, self.articles[path][self.len_u + 4])
        for i in xrange(len(f)):
            self.articles[path][self.len_u + 2 + i] = sel_col[f[i]]
            model.set(iter, self.len_u + 2 + i, self.articles[path][self.len_u + 2 + i])
        cellse = rc_modul.Sum_cell(self.rc_dict)
        
        if key == 'space':
            try:
                ic = cellse.index('Cell_Size')
            except:
                pass
            else:
                n = model.get_value(iter, self.len_u)
                if os.path.isdir(n):
                    self.articles[path][ic] = edna_function.get_in_format_size(edna_function.get_full_size(n))
                    model.set(iter, ic, self.articles[path][ic])
            
            
    def pr(self, *args):
        if args[1].type == gtk.gdk._2BUTTON_PRESS:
            self.chdir_new()
            
    def back_dir(self):
        self.pattern_s = self.Current_Path
        self.Select_List = []
        self.ch_dir_entry(os.path.dirname(self.Current_Path))
        model = self.__create_model()
        self.treeview.set_model(model)
        self.treeview.set_cursor(self.return_select)
                    
    def chdir_new(self):
        selection = self.treeview.get_selection()
        model, iter = selection.get_selected()
        u = rc_modul.Sum_cell(self.rc_dict)
        dp = model.get_value(iter, len(u))
        if dp == '..':
            self.back_dir()
            
        elif os.path.isdir(dp):
            self.pattern_s = ''
            self.ch_dir_entry(dp)
            model = self.__create_model()
            self.treeview.set_model(model)
            self.treeview.set_cursor(self.return_select)
            
        elif os.path.isfile(dp):
            self.pattern_s = ''
            ret = edna_function.get_launch(dp)
            if ret:
                subprocess.Popen(ret + ' \'' + dp + '\'', shell=True)
            print ret
            
                
    def __add_columns(self, treeview):
        '''
        Создание столбцов
        '''
        model = treeview.get_model()
        u = rc_modul.Sum_cell(self.rc_dict)
        for i in xrange(self.len_u):
            alg = [float(self.rc_dict[u[i] + '_Alignment_H']), float(self.rc_dict[u[i] + '_Alignment_V'])]
            if u[i] == 'Cell_Name':
                column = gtk.TreeViewColumn()
                column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
                column.expand = True
                column.set_min_width(int(self.rc_dict[u[i] + '_Size']))
                column.set_title(rc_modul.locale[u[i]])                
                
                renderer = gtk.CellRendererPixbuf()
                renderer.set_alignment(alg[0], alg[1])
                column.pack_start(renderer, False)
                column.set_attributes(renderer, pixbuf=self.len_u + 1)
                
                renderer = gtk.CellRendererText()
                renderer.set_alignment(alg[0], alg[1])
                renderer.set_property('font-desc' , pango.FontDescription(self.rc_dict['Font_Cell_Text']))
                column.pack_start(renderer, True)
                column.set_attributes(renderer, text=i, background=self.len_u + 3, foreground=self.len_u + 2)
                itk = int(self.rc_dict[u[i] + '_Expand'])
                column.set_expand(itk)
                treeview.append_column(column)
            else:
                renderer = gtk.CellRendererText()
                renderer.set_data(rc_modul.locale[u[i]], i)
                renderer.set_alignment(alg[0], alg[1])
                renderer.set_property('background-set' , True)
                renderer.set_property('foreground-set' , True)
                renderer.set_property('font-desc' , pango.FontDescription(self.rc_dict['Font_Cell_Text']))
                column = gtk.TreeViewColumn(rc_modul.locale[u[i]], renderer, text=i, background=len(u) + 3, foreground=len(u) + 2)
                column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
                column.expand = True
                itk = int(self.rc_dict[u[i] + '_Expand'])
                column.set_expand(itk)
                column.set_min_width(int(self.rc_dict[u[i] + '_Size']))    
                treeview.append_column(column)
            
    def __create_model(self):
        # create list store
        u = rc_modul.Sum_cell(self.rc_dict)
        self.articles, self.return_select = edna_function.get_list_path(self.Current_Path, self.pattern_s, self.Select_List)
        self.len_articles = len(self.articles)
        self.len_u = len(u)
        if self.len_u == 1:
            model = gtk.ListStore(
                                gobject.TYPE_STRING, gobject.TYPE_STRING, 
                                gtk.gdk.Pixbuf, gobject.TYPE_STRING, 
                                gobject.TYPE_STRING, gobject.TYPE_STRING, 
                                gobject.TYPE_STRING, gobject.TYPE_STRING, 
                                gobject.TYPE_STRING, gobject.TYPE_STRING, 
                                gobject.TYPE_STRING, gobject.TYPE_STRING, 
                                gobject.TYPE_STRING, gobject.TYPE_STRING)
        elif self.len_u == 2:
            model = gtk.ListStore(
                                gobject.TYPE_STRING, gobject.TYPE_STRING, 
                                gobject.TYPE_STRING, gtk.gdk.Pixbuf, 
                                gobject.TYPE_STRING, gobject.TYPE_STRING, 
                                gobject.TYPE_STRING, gobject.TYPE_STRING, 
                                gobject.TYPE_STRING, gobject.TYPE_STRING, 
                                gobject.TYPE_STRING, gobject.TYPE_STRING, 
                                gobject.TYPE_STRING, gobject.TYPE_STRING)
        elif self.len_u == 3:
            model = gtk.ListStore(
                                gobject.TYPE_STRING, gobject.TYPE_STRING, 
                                gobject.TYPE_STRING, gobject.TYPE_STRING, 
                                gtk.gdk.Pixbuf, gobject.TYPE_STRING, 
                                gobject.TYPE_STRING, gobject.TYPE_STRING, 
                                gobject.TYPE_STRING, gobject.TYPE_STRING, 
                                gobject.TYPE_STRING, gobject.TYPE_STRING, 
                                gobject.TYPE_STRING, gobject.TYPE_STRING, 
                                gobject.TYPE_STRING, gobject.TYPE_STRING)
        elif self.len_u == 4:
            model = gtk.ListStore(
                                gobject.TYPE_STRING, gobject.TYPE_STRING, 
                                gobject.TYPE_STRING, gobject.TYPE_STRING, 
                                gobject.TYPE_STRING, gtk.gdk.Pixbuf, 
                                gobject.TYPE_STRING, gobject.TYPE_STRING, 
                                gobject.TYPE_STRING, gobject.TYPE_STRING, 
                                gobject.TYPE_STRING, gobject.TYPE_STRING, 
                                gobject.TYPE_STRING, gobject.TYPE_STRING, 
                                gobject.TYPE_STRING, gobject.TYPE_STRING)
        elif self.len_u == 5:
            model = gtk.ListStore(
                                gobject.TYPE_STRING, gobject.TYPE_STRING, 
                                gobject.TYPE_STRING, gobject.TYPE_STRING, 
                                gobject.TYPE_STRING, gobject.TYPE_STRING, 
                                gtk.gdk.Pixbuf, gobject.TYPE_STRING, 
                                gobject.TYPE_STRING, gobject.TYPE_STRING, 
                                gobject.TYPE_STRING, gobject.TYPE_STRING, 
                                gobject.TYPE_STRING, gobject.TYPE_STRING, 
                                gobject.TYPE_STRING, gobject.TYPE_STRING)
        elif self.len_u == 6:
            model = gtk.ListStore(
                                gobject.TYPE_STRING, gobject.TYPE_STRING, 
                                gobject.TYPE_STRING, gobject.TYPE_STRING, 
                                gobject.TYPE_STRING, gobject.TYPE_STRING, 
                                gobject.TYPE_STRING, gtk.gdk.Pixbuf, 
                                gobject.TYPE_STRING, gobject.TYPE_STRING, 
                                gobject.TYPE_STRING, gobject.TYPE_STRING, 
                                gobject.TYPE_STRING, gobject.TYPE_STRING, 
                                gobject.TYPE_STRING, gobject.TYPE_STRING, 
                                gobject.TYPE_STRING, gobject.TYPE_STRING)
        elif self.len_u == 7:
            model = gtk.ListStore(
                                gobject.TYPE_STRING, gobject.TYPE_STRING, 
                                gobject.TYPE_STRING, gobject.TYPE_STRING, 
                                gobject.TYPE_STRING, gobject.TYPE_STRING, 
                                gobject.TYPE_STRING, gobject.TYPE_STRING, 
                                gtk.gdk.Pixbuf, gobject.TYPE_STRING,
                                gobject.TYPE_STRING, gobject.TYPE_STRING, 
                                gobject.TYPE_STRING, gobject.TYPE_STRING, 
                                gobject.TYPE_STRING, gobject.TYPE_STRING, 
                                gobject.TYPE_STRING, gobject.TYPE_STRING, 
                                gobject.TYPE_STRING, gobject.TYPE_STRING)
        elif self.len_u == 8:
            model = gtk.ListStore(
                                gobject.TYPE_STRING, gobject.TYPE_STRING, 
                                gobject.TYPE_STRING, gobject.TYPE_STRING, 
                                gobject.TYPE_STRING, gobject.TYPE_STRING, 
                                gobject.TYPE_STRING, gobject.TYPE_STRING, 
                                gobject.TYPE_STRING, gtk.gdk.Pixbuf,
                                gobject.TYPE_STRING, gobject.TYPE_STRING, 
                                gobject.TYPE_STRING, gobject.TYPE_STRING, 
                                gobject.TYPE_STRING, gobject.TYPE_STRING, 
                                gobject.TYPE_STRING, gobject.TYPE_STRING)
                                
                                
        for item in self.articles:
            iter = model.append()
            model.set(iter)
            for j in xrange(len(item)):
                model.set_value(iter, j, item[j])
        return model
        
    def Step_dir(self):
        pass
            
    def upData(sefl, rc_dict):
        #treeview.set_rules_hint(True)
        
        pass

            
def main():
    #global answer
    #answer = 0
    h = miss_window('/home/mort/.bashrc')
    #h.butt_miss.connect('clicked', lambda *y: buf_def(1))
    #h.butt_again.connect('clicked', answer = 2)
    #h.butt_miss_all.connect('clicked', answer = 3)
    #h.butt_cancel.connect('clicked', answer = 4)
    h.show_all()
    #print answer
    gtk.main()
    return 0

if __name__ == '__main__':
    main()

