#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       gui_class_rc.py
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
import gtk
import gobject
import pango

import rc_modul


gf = [1.0, 0.5, 0.0]

class Rc_Window(gtk.Window):
    def __init__(self, locale_dict):
        gtk.Window.__init__(self)
        self.locale_dict = locale_dict
        self.set_title(self.locale_dict['Rc_Title'])
        self.set_position(gtk.WIN_POS_CENTER)
        #self.set_resizable(False)
        self.set_default_size(400, 500)
        
        vbox1 = gtk.VBox(False)
        hbox1 = gtk.HButtonBox()
        hbox1.set_layout(gtk.BUTTONBOX_END)
        self.note = gtk.Notebook()
        self.note.set_tab_pos(gtk.POS_LEFT)
        self.button_ok = gtk.Button(stock='gtk-ok')
        self.button_cancel = gtk.Button(stock='gtk-cancel')
        self.button_apply = gtk.Button(stock='gtk-apply')
        vbox1.set_border_width(3)
        vbox1.pack_start(self.note, True)
        hbox1.add(self.button_ok)
        hbox1.add(self.button_cancel)
        hbox1.add(self.button_apply)
        vbox1.pack_start(hbox1, False)
        
        self.fill_note()
        
        self.add(vbox1)
        self.show_all()
    
    def fill_note(self):
        self.all_page()
        self.tab_page()
        self.tab_style()
    def all_page(self):
        vbox2 = gtk.VBox()
        
        self.note.append_page(vbox2, gtk.Label(self.locale_dict['Rc_All_Page']))
        
    def tab_style(self):
        vbox2 = gtk.VBox(False)
        vbox2.set_border_width(3)
        hbox1 = gtk.HBox(False)
        hbox1.set_border_width(3)
        tab1 = gtk.Table(1, 1, False)
        tab1.set_row_spacings(5)
        tab1.set_col_spacings(5)
        lab = gtk.Label(self.locale_dict['Colors'])
        lab.modify_font(pango.FontDescription('bold'))
        #lab.set_justify(gtk.JUSTIFY_LEFT)
        lab.set_alignment(0.0, 0.5)
        l = ['even_row', 'odd_row', 'sel_row']
        p = ['fg', 'bg']
        bt = {}
        for i in l:
            for j in p:
                bt[i + '_' + j] = gtk.Button()
                bt[i + '_' + j].set_size_request(30, 30)
                bt[i + '_' + j].connect('clicked', self.color_click, i + '_' + j)
                bt[i + '_' + j].modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(rc_modul.rc_dict['style']['%s_%s' % (i, j)]))
                bt[i + '_' + j].modify_bg(gtk.STATE_PRELIGHT, gtk.gdk.Color(rc_modul.rc_dict['style']['%s_%s' % (i, j)]))
                #bt[i + '_' + j].modify_bg(gtk.STATE_ACTIVE, gtk.gdk.Color(rc_modul.rc_dict['style']['%s_%s' % (i, j)]))
                bt[i + '_' + j].modify_bg(gtk.STATE_SELECTED, gtk.gdk.Color(rc_modul.rc_dict['style']['%s_%s' % (i, j)]))
        tab1.attach(gtk.Label(self.locale_dict['Row_FG']), 1, 2, 0, 1)
        tab1.attach(gtk.Label(self.locale_dict['Row_BG']), 2, 3, 0, 1)
        for i in xrange(len(l)):
            lbb = gtk.Label(self.locale_dict[l[i]] + ':')
            lbb.set_alignment(0.0, 0.5)
            tab1.attach(lbb, 0, 1, i + 1, i + 2)
            for j in xrange(len(p)):
                tab1.attach(bt[l[i] + '_' + p[j]], j + 1, j + 2, i + 1, i + 2)
        
        self.font_label_text = gtk.Label(self.locale_dict['Font_Label_Text'])
        self.font_label_text.modify_font(pango.FontDescription(rc_modul.rc_dict['style']['font_cell_text']))
        self.font_button_text = gtk.Button(self.locale_dict['Font_Button_Text'])
        self.font_button_text.connect('clicked', self.font_click, self.font_label_text)
        
        hbox1.pack_start(self.font_label_text, True)
        hbox1.pack_start(self.font_button_text, False)
        vbox2.pack_start(lab, False)
        vbox2.pack_start(tab1, False)
        vbox2.pack_start(hbox1, False)
        self.note.append_page(vbox2, gtk.Label(self.locale_dict['Rc_Cell_Appearance']))
        
    def font_click(self, *args):
        dialog = gtk.FontSelectionDialog("Changing color")
        dialog.set_transient_for(self)
        fontsel = dialog.fontsel
        fontsel.set_font_name(rc_modul.rc_dict['style']['font_cell_text'])
        response = dialog.run()

        if response == gtk.RESPONSE_OK:
            rc_modul.rc_dict['style']['font_cell_text'] = fontsel.get_font_name()
            args[1].modify_font(pango.FontDescription(rc_modul.rc_dict['style']['font_cell_text']))

        dialog.destroy()
        
    def color_click(self, *args):
        dialog = gtk.ColorSelectionDialog("Changing color")
        dialog.set_transient_for(self)
        colorsel = dialog.colorsel
        
        colorsel.set_previous_color(gtk.gdk.Color(rc_modul.rc_dict['style'][args[1]]))
        colorsel.set_current_color(gtk.gdk.Color(rc_modul.rc_dict['style'][args[1]]))
        colorsel.set_has_palette(True)

        response = dialog.run()

        if response == gtk.RESPONSE_OK:
            rc_modul.rc_dict['style'][args[1]] = str(colorsel.get_current_color())
            args[0].modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(rc_modul.rc_dict['style'][args[1]]))
            args[0].modify_bg(gtk.STATE_PRELIGHT, gtk.gdk.Color(rc_modul.rc_dict['style'][args[1]]))
            args[0].modify_bg(gtk.STATE_SELECTED, gtk.gdk.Color(rc_modul.rc_dict['style'][args[1]]))

        dialog.destroy()
            
    def tab_page(self):
        vvbox1 = gtk.VBox(False, 10)
        vvbox1.set_border_width(3)
        vvbox2 = gtk.VBox(False)
        vvbox3 = gtk.VBox(False, 5) #######
        vvbox2.set_border_width(3)
        hhbox1 = gtk.HBox(False)
        hhbox2 = gtk.HBox(False)#############
        hhbox1.set_border_width(3)
        tb1 = gtk.Table(2, 2, True)
        
        ###########Rc_Cell_Cell###################
        button1 = gtk.Button(stock='gtk-go-up')
        button2 = gtk.Button(stock='gtk-go-down')
        label1 = gtk.Label(self.locale_dict['Rc_Cell_Cell'])
        label1.modify_font(pango.FontDescription('bold'))
        label1.set_justify(gtk.JUSTIFY_LEFT)
        cel_sort = listen_cel(self.locale_dict)
        cel_sort.renderer.connect('toggled', self.fixed_toggled, cel_sort.model)
        button1.connect('clicked', self.downup, cel_sort, True)
        button2.connect('clicked', self.downup, cel_sort, False)
        
        #########################################
        
        #############Rc_Cell_Appearance##########
        label2 = gtk.Label(self.locale_dict['Rc_Cell_Appearance'])
        label2.modify_font(pango.FontDescription('bold'))
        #chkb1 = gtk.CheckButton()
        #tb1.attach()
        #########################################
        vvbox2.pack_start(button1, True)
        vvbox2.pack_start(button2, True)
        
        vvbox1.pack_start(label1, False)
        hhbox1.pack_start(cel_sort, True)
        hhbox1.pack_start(vvbox2, False)
        vvbox1.pack_start(hhbox1, False)
        
        vvbox1.pack_start(label2, False)
        tb1.attach(gtk.Label(self.locale_dict['Cell_Cell_Expand']), 0, 1, 0, 1)
        tb1.attach(gtk.Label(self.locale_dict['Cell_Cell_Min_Size']), 1, 2, 0, 1)
        tb1.attach(gtk.Label(self.locale_dict['Cell_Cell_Alignment_H']), 2, 3, 0, 1)
        tb1.attach(gtk.Label(self.locale_dict['Cell_Cell_Alignment_V']), 3, 4, 0, 1)
        
        for i in xrange(len(rc_modul.mc)):
            cheak = gtk.CheckButton(None)
            cheak.cl = '%s_expand' % rc_modul.mc[i]
            cheak.set_active(int(rc_modul.rc_dict['style'][cheak.cl]))
            cheak.connect('toggled', self.toggled)
            
            sp2 = gtk.SpinButton(gtk.Adjustment(0, 0, 100, 1, -1))
            sp2.cl = '%s_size' % rc_modul.mc[i]
            sp2.set_value(int(rc_modul.rc_dict['style'][sp2.cl]))
            sp2.connect('value_changed', self.spin)
            
            chkH1 = gtk.combo_box_new_text()
            for j in gf:
                chkH1.append_text(self.locale_dict['Cell_Cell_Alignment_H_' + str(j)])
            chkH1.nm = '%s_alignment_h' % rc_modul.mc[i]
            chkH1.set_active(gf.index(float(rc_modul.rc_dict['style'][chkH1.nm])))
            chkH1.connect('changed', self.chk_c)
            
            chkV1 = gtk.combo_box_new_text()
            for j in gf:
                chkV1.append_text(self.locale_dict['Cell_Cell_Alignment_V_%s' % j])
            chkV1.nm = '%s_alignment_v' % rc_modul.mc[i]
            chkV1.set_active(gf.index(float(rc_modul.rc_dict['style'][chkV1.nm])))
            chkV1.connect('changed', self.chk_c)
            
            tb1.attach(cheak, 0, 1, i + 1, i + 2)
            tb1.attach(sp2, 1, 2, i + 1, i + 2)
            tb1.attach(chkH1, 2, 3, i + 1, i + 2)
            tb1.attach(chkV1, 3, 4, i + 1, i + 2)
            
        lb = gtk.Label(self.locale_dict['Rc_Cell_Cell'])
        vvbox3.pack_start(lb, True)
        for i in xrange(len(rc_modul.mc)):
            lb = gtk.Label(self.locale_dict[rc_modul.mc[i]])
            lb.set_alignment(0.0, 0.5)
            vvbox3.pack_start(lb, True)
        
        
        hhbox2.pack_start(vvbox3, True)
        hhbox2.pack_start(tb1, False)
        vvbox1.pack_start(hhbox2, False)
        
        hbox2 = gtk.HBox(False, 10)
        label1 = gtk.Label(self.locale_dict['Cell_Cell_DateC_Format'])
        label1.set_alignment(0.0, 0.5)
        entry1 = gtk.Entry()
        entry1.set_text(rc_modul.rc_dict['style']['cell_datec_format'])
        entry1.connect('changed', self.on_changed, 'cell_datec_format')
        
        hbox2.pack_start(label1, True)
        hbox2.pack_start(entry1, False)
        
        hbox3 = gtk.HBox(False, 10)
        label2 = gtk.Label(self.locale_dict['Cell_Cell_DateM_Format'])
        label2.set_alignment(0.0, 0.5)
        entry2 = gtk.Entry()
        entry2.set_text(rc_modul.rc_dict['style']['cell_datem_format'])
        entry2.connect('changed', self.on_changed, 'cell_datem_format')        
        
        hbox3.pack_start(label2, True)
        hbox3.pack_start(entry2, False)
        
        hbox4 = gtk.HBox(False, 3)
        
        chk1 = gtk.combo_box_new_text()
        for i in xrange(3):
            chk1.append_text(self.locale_dict['List_Size_Format_%s' % i])
        chk1.set_active(int(rc_modul.rc_dict['style']['cell_size_format']))
        chk1.connect('changed', self.chk1_c)
        label3 = gtk.Label(self.locale_dict['Cell_Cell_Size_Format'])
        label3.set_alignment(0.0, 0.5)
        
        hbox5 = gtk.HBox(False, 3)
        
        chk2 = gtk.combo_box_new_text()
        for i in xrange(2):
            chk2.append_text(self.locale_dict['Cell_Atr_Format_' + str(i)])
        chk2.set_active(int(rc_modul.rc_dict['style']['cell_atr_format']))
        chk2.connect('changed', self.chk2_c)
        label4 = gtk.Label(self.locale_dict['Cell_Cell_Atr_Format'])
        label4.set_alignment(0.0, 0.5)
        
        hbox4.pack_start(label3, True)
        hbox4.pack_start(chk1, False)
        hbox5.pack_start(label4, True)
        hbox5.pack_start(chk2, False)
        
        vvbox1.pack_start(hbox2, False)
        vvbox1.pack_start(hbox3, False)
        vvbox1.pack_start(hbox4, False)
        vvbox1.pack_start(hbox5, False)
        self.note.append_page(vvbox1, gtk.Label(self.locale_dict['Rc_Tab_Page']))
        
    def chk_c(self, *args):
        rc_modul.rc_dict['style'][args[0].nm] = str(gf[args[0].get_active()])        
        
    def chk1_c(self, *args):
        rc_modul.rc_dict['style']['cell_size_format'] = str(args[0].get_active())
        
    def chk2_c(self, *args):
        rc_modul.rc_dict['style']['cell_atr_format'] = str(args[0].get_active())
            
    def downup(self, *args):
        selection = args[1].treeview.get_selection()
        model, iter = selection.get_selected()
        args[1].treeview.set_drag_dest_row(3, gtk.TREE_VIEW_DROP_AFTER)
        #print model.get_value(iter, 2)
        #model.move_after(iter, None)
        #args[1].treeview.set_model(model)
        
    def on_changed(self, *args):
        text = args[0].get_text()#.strip()
        args[0].set_text(''.join([i for i in text if i in 'YMDhsm/-.: ']))
        rc_modul.rc_dict['style'][args[1]] = args[0].get_text() 

    def spin(self, *args):
        rc_modul.rc_dict['style'][args[0].cl] = str(int(args[0].get_value()))
        
    def toggled(self, *args):
        rc_modul.rc_dict['style'][args[0].cl] = str(int(args[0].get_active()))

             
    def fixed_toggled(self, cell, path, model):
        iter = model.get_iter((int(path),))
        fixed = model.get_value(iter, 0)
        fixed = not fixed
        rc_modul.rc_dict['style'][model.get_value(iter, 2)] = str(int(fixed))
        model.set(iter, 0, fixed)


        
class listen_cel(gtk.ScrolledWindow):
    def __init__(self, locale_dict):
        gtk.ScrolledWindow.__init__(self)
        self.locale_dict = locale_dict
        self.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        model = self.__create_model()
        self.treeview = gtk.TreeView(model)
        self.treeview.set_headers_visible(False)
        self.treeview.set_size_request(100,100)
        self.treeview.get_selection().set_mode(gtk.SELECTION_SINGLE)

        self.__add_columns(self.treeview)
        self.treeview.set_model(model)
        self.add(self.treeview)
        
    def __add_columns(self, treeview):
        self.model = treeview.get_model()
        self.renderer = gtk.CellRendererToggle()
        self.renderer.set_data('', 0)
        column = gtk.TreeViewColumn('', self.renderer, active=0)
        column.set_fixed_width(50)
        column.set_resizable(True)
        treeview.append_column(column)
        renderer = gtk.CellRendererText()
        renderer.set_data('', 1)
        column = gtk.TreeViewColumn('', renderer, text=1)
        column.set_min_width(70)
        treeview.append_column(column)
        
    def __create_model(self):
        self.articles = []
        for i in xrange(len(rc_modul.mc)):
            t = rc_modul.mc[int(rc_modul.rc_dict['style']['cell_sort'][i])]
            b = bool(int(rc_modul.rc_dict['style'][t]))
            self.articles.append([b, self.locale_dict[t], t])
        
        model = gtk.ListStore(gobject.TYPE_BOOLEAN, gobject.TYPE_STRING, gobject.TYPE_STRING)
        for item in self.articles:
            iter = model.append()
            model.set(iter, 0, item[0], 1, item[1], 2, item[2])
        return model

def sv(*args):
    rc_modul.save_rc()
    gtk.main_quit()

def main():
    lc = rc_modul.locale_rc('.local')
    rrr = Rc_Window(lc)
    rrr.button_ok.connect('clicked', sv)
    
    gtk.main()
    return 0

if __name__ == '__main__':
    main()

