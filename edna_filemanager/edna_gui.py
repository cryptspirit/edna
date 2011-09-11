# -*- coding: utf-8 -*-

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
import app_choose
import drive_panel

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
        self.set_icon(edna_function.icon_load_try('gtk-dialog-info', 20))
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
            self.set_icon(edna_function.icon_load_try('gtk-cut', 20))
        else:
            self.set_icon(edna_function.icon_load_try('gtk-copy', 20))
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
                    again = self.custom_copy(args[i][0], p1, args[i][1], 1000)
                
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
        self.set_icon(edna_function.icon_load_try('gtk-clear', 20))
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
        list = [[gio.File(i[0]).get_path(), i[1]] for i in list]
        self.set_resizable(False)
        self.set_modal(True)
        vbox = gtk.VBox(False, 2)
        vbox.set_spacing(3)
        self.set_border_width(5)
        hbox = gtk.HBox(False, 2)
        hbox.set_spacing(10)
        self.set_title(self_name)
        self.icon_image = gtk.Image()
        pix = edna_function.icon_load_try('gtk-help', 50)
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
        text = _('You want to delete') + '\n%s%s' % (target, unicode(target_list, 'utf8'))
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
        self.remove_after = remove_after
        self.set_modal(True)
        self.destpath = destpath.get_path()
        self.connect('destroy', self.destr)
        self.connect('key-release-event', self.key_event)
        if self.remove_after:
            self.set_icon(edna_function.icon_load_try('gtk-cut', 20))
        else:
            self.set_icon(edna_function.icon_load_try('gtk-copy', 20))
        self.set_resizable(False)
        vbox = gtk.VBox(False, 2)
        vbox.set_spacing(3)
        self.set_border_width(5)
        self.list = [[gio.File(i[0]).get_path(), i[1]] for i in list]
        self.current_path = current_path.get_path()
        self.set_title(self_name)
        self.set_position(gtk.WIN_POS_CENTER)
        text = _('To copy %s files/folders in' % len(list))
        label_question = gtk.Label(text)
        label_question.set_alignment(0.0, 0.0)
        self.entry1 = gtk.Entry()
        #self.connect('key-release-event', self.key_event)
        self.entry1.set_size_request(250, -1)
        self.entry1.set_text(self.destpath)
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
        self.get_modal()
        self.path_to_file = path_to_file.get_path()
        self.is_file = os.path.isfile(self.path_to_file)
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
        
        icon_image1.connect('clicked', self.__show_app_choose_windows__)
        
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
        
    def __show_app_choose_windows__(self, *args):
        '''
        Запуск окна выбора приложения
        '''
        choose_app_window = app_choose.Apps_Choose_Window(self.info_about_file['Type'])
        choose_app_window.show_all()
        
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
        

    
    
    

################################  Gui class (end) #############################
def main():
    h = properties_file_window(['/home/mort/Box', False])
    #h = miss_window('/home/mort/.bashrc')
    h.show_all()
    gtk.main()
    return 0

if __name__ == '__main__':
    main()

