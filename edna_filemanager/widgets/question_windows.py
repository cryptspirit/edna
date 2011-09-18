# -*- coding: utf-8 -*-

'''
Классы окон вопросов
'''

from __builtin__ import edna_builtin

import gtk
import gio
from edna_filemanager.tools import icons_work
from edna_filemanager.tools import keybind

class Question_to_Copy(gtk.Window):
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
            self.set_icon(icons_work.icon_load_try('gtk-cut', 20))
        else:
            self.set_icon(icons_work.icon_load_try('gtk-copy', 20))
        self.set_resizable(False)
        vbox = gtk.VBox(False, 2)
        vbox.set_spacing(3)
        self.set_border_width(5)
        self.list = [[gio.File(i[0]).get_path(), i[1]] for i in list]
        self.current_path = current_path.get_path()
        self.set_title(edna_builtin['project name'])
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
                        buf = function.get_full_size(i[0], True)
                        k += buf[1]
                        siz += buf[0]
        self.hide()
        r = copy_window(self.list, k, self.destpath, self.current_path, siz, self.remove_after)
        self.destr()
    
    def destr(self, *args):
        self.hide()
        self.destroy
        
    def key_event(self, *args):
        key = keybind.get_key_info(args[1])
        if key == 'Escape': self.destr()
        if key == 'Return': self.ok_button_click()
