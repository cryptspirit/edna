#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
#       edna_config.py
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
import pango
import edna_function
import gettext
import gobject
import edna_gui

gettext.install('edna', unicode=True)


            
gf = [1.0, 0.5, 0.0]
gfH = [_('right'), _('center'), _('left')]
gfV = [_('up'), _('center'), _('down')]

class Rc_Window(gtk.Window):
    class listen_cel(gtk.ScrolledWindow):
        def __init__(self):
            gtk.ScrolledWindow.__init__(self)
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
            for i in xrange(len(edna_function.mc)):
                t = edna_function.mc[int(edna_function.rc_dict['style']['cell_sort'][i])]
                b = bool(int(edna_function.rc_dict['style'][t]))
                self.articles.append([b, edna_gui.Name_Colum[t], t])
            
            model = gtk.ListStore(gobject.TYPE_BOOLEAN, gobject.TYPE_STRING, gobject.TYPE_STRING)
            for item in self.articles:
                iter = model.append()
                model.set(iter, 0, item[0], 1, item[1], 2, item[2])
            return model
            
    class listen_hotkeys(gtk.ScrolledWindow):
        def __init__(self):
            gtk.ScrolledWindow.__init__(self)
            self.set_shadow_type(gtk.SHADOW_ETCHED_IN)
            self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
            model = self.__create_model()
            self.treeview = gtk.TreeView(model)
            #self.treeview.set_headers_visible(False)
            self.treeview.set_size_request(100,-1)
            self.treeview.get_selection().set_mode(gtk.SELECTION_SINGLE)
            self.treeview.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)
            self.__add_columns(self.treeview)
            self.treeview.set_model(model)
            self.add(self.treeview)
            
        def __add_columns(self, treeview):
            #self.model = treeview.get_model()
            
            renderer = gtk.CellRendererText()
            renderer.set_data('', 0)
            column = gtk.TreeViewColumn('', renderer, text=0)
            column.set_min_width(70)
            column.expand = True
            column.set_expand(100)
            column.set_title(_('Action'))
            treeview.append_column(column)
            
            renderer = gtk.CellRendererText()
            renderer.set_data('', 1)
            column = gtk.TreeViewColumn('', renderer, text=1)
            column.set_min_width(150)
            column.set_title(_('Keys'))
            treeview.append_column(column)
            
        def __create_model(self):
            self.articles = []
            yk = edna_function.rc_hotkeys.keys()
            yk.sort()
            for i in yk:
                t = edna_function.rc_dict['hotkeys'][i]
                b = edna_function.hotkeys_function_name[i]
                self.articles.append([b, t, i])
            
            model = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING)
            for item in self.articles:
                iter = model.append()
                model.set(iter, 0, item[0], 1, item[1], 2, item[2])
            return model
        
    def __init__(self):
        gtk.Window.__init__(self)
        self.set_title(_('Configurations'))
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_modal(True)
        #self.set_resizable(False)
        self.Modal = True
        self.set_default_size(400, 500)
        self.set_icon(edna_function.get_theme.load_icon('gtk-preferences', 20, 0))
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
        self.tab_hotkeys()
        
    def all_page(self):
        vbox2 = gtk.VBox()
        self.note.append_page(vbox2, gtk.Label(_('Genaral')))
        
    def tab_style(self):
        vbox2 = gtk.VBox(False)
        vbox2.set_border_width(3)
        hbox1 = gtk.HBox(False)
        hbox1.set_border_width(3)
        tab1 = gtk.Table(1, 1, False)
        tab1.set_row_spacings(5)
        tab1.set_col_spacings(5)
        lab = gtk.Label(_('Colors'))
        lab.modify_font(pango.FontDescription('bold'))
        #lab.set_justify(gtk.JUSTIFY_LEFT)
        lab.set_alignment(0.0, 0.5)
        l = ['even_row', 'odd_row', 'sel_row']
        l_name = [_('Even rows'), _('Odd rows'), _('Select rows')]
        p = ['fg', 'bg']
        bt = {}
        for i in l:
            for j in p:
                bt[i + '_' + j] = gtk.Button()
                bt[i + '_' + j].set_size_request(30, 30)
                bt[i + '_' + j].connect('clicked', self.color_click, i + '_' + j)
                bt[i + '_' + j].modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(edna_function.rc_dict['style']['%s_%s' % (i, j)]))
                bt[i + '_' + j].modify_bg(gtk.STATE_PRELIGHT, gtk.gdk.Color(edna_function.rc_dict['style']['%s_%s' % (i, j)]))
                #bt[i + '_' + j].modify_bg(gtk.STATE_ACTIVE, gtk.gdk.Color(edna_function.rc_dict['style']['%s_%s' % (i, j)]))
                bt[i + '_' + j].modify_bg(gtk.STATE_SELECTED, gtk.gdk.Color(edna_function.rc_dict['style']['%s_%s' % (i, j)]))
        tab1.attach(gtk.Label(_('Foreground')), 1, 2, 0, 1)
        tab1.attach(gtk.Label(_('Background')), 2, 3, 0, 1)
        for i in xrange(len(l)):
            lbb = gtk.Label(l_name[i] + ':')
            lbb.set_alignment(0.0, 0.5)
            tab1.attach(lbb, 0, 1, i + 1, i + 2)
            for j in xrange(len(p)):
                tab1.attach(bt[l[i] + '_' + p[j]], j + 1, j + 2, i + 1, i + 2)
        
        self.font_label_text = gtk.Label(_('Example text'))
        self.font_label_text.modify_font(pango.FontDescription(edna_function.rc_dict['style']['font_cell_text']))
        self.font_button_text = gtk.Button(_('Font button'))
        self.font_button_text.connect('clicked', self.font_click, self.font_label_text)
        
        hbox1.pack_start(self.font_label_text, True)
        hbox1.pack_start(self.font_button_text, False)
        vbox2.pack_start(lab, False)
        vbox2.pack_start(tab1, False)
        vbox2.pack_start(hbox1, False)
        self.note.append_page(vbox2, gtk.Label(_('Appearance')))
        
    def key_ev(self, *args):
        key = edna_function.get_key_info(args[1])
        if key == 'Escape':
            args[0].hide()
            args[0].destroy()
        if key not in keys_not_follow:
            if key not in edna_function.key_name_in_rc.keys():
                edna_function.rc_dict['hotkeys'][args[2].get_value(args[3], 2)] = key
                edna_function.key_name_in_rc[key] = args[2].get_value(args[3], 2)         
                args[2].set(args[3], 1, key)
                args[0].hide()
                args[0].destroy()
            else:
                args[4].set_label(_('The keys are already used') + '\n' + _('enter other keys'))

    def create_winkey(self, *args):
        '''
        Процедура создает окно для введения комбинации клавиш
        '''
        selection = args[0].get_selection()
        model, iter = selection.get_selected()
        w = gtk.Window()
        w.set_title(_('Press keys'))
        w.set_size_request(250, 130)
        w.set_resizable(False)
        w.set_transient_for(self)
        w.set_modal(True)
        l = gtk.Label(_('Press keys'))
        l.modify_font(pango.FontDescription('bold'))
        w.add(l)
        w.connect('key-release-event', self.key_ev, model, iter, l)
        w.show_all()
        
    def tab_hotkeys(self):
        '''
        Процедура создания вкладки горячих клавиш
        '''
        vbox2 = gtk.VBox(False)
        vbox2.set_border_width(3)
        lst_hotkeys = self.listen_hotkeys()
        lst_hotkeys.treeview.connect('row-activated', self.create_winkey, lst_hotkeys) #Двойной щелчок по строке
        
        button1 = gtk.Button(_('Clear'))
        button1.connect('clicked', self.clear_keys, lst_hotkeys)
        
        vbox2.pack_start(lst_hotkeys, True)
        vbox2.pack_start(button1, False)
        self.note.append_page(vbox2, gtk.Label(_('Hotkeys')))

    def clear_keys(self, *args):
        '''
        Процедура очистки операции от горячих клавиш
        '''
        selection = args[1].treeview.get_selection()
        model, iter = selection.get_selected()
        if iter:
            del edna_function.key_name_in_rc[edna_function.rc_dict['hotkeys'][model.get_value(iter, 2)]]
            edna_function.rc_dict['hotkeys'][model.get_value(iter, 2)] = ''
            model.set(iter, 1, '')

    def font_click(self, *args):
        dialog = gtk.FontSelectionDialog("Changing color")
        dialog.set_transient_for(self)
        fontsel = dialog.fontsel
        fontsel.set_font_name(edna_function.rc_dict['style']['font_cell_text'])
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            edna_function.rc_dict['style']['font_cell_text'] = fontsel.get_font_name()
            args[1].modify_font(pango.FontDescription(edna_function.rc_dict['style']['font_cell_text']))
        dialog.destroy()
        
    def color_click(self, *args):
        dialog = gtk.ColorSelectionDialog("Changing color")
        dialog.set_transient_for(self)
        colorsel = dialog.colorsel
        colorsel.set_previous_color(gtk.gdk.Color(edna_function.rc_dict['style'][args[1]]))
        colorsel.set_current_color(gtk.gdk.Color(edna_function.rc_dict['style'][args[1]]))
        colorsel.set_has_palette(True)
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            edna_function.rc_dict['style'][args[1]] = str(colorsel.get_current_color())
            args[0].modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(edna_function.rc_dict['style'][args[1]]))
            args[0].modify_bg(gtk.STATE_PRELIGHT, gtk.gdk.Color(edna_function.rc_dict['style'][args[1]]))
            args[0].modify_bg(gtk.STATE_SELECTED, gtk.gdk.Color(edna_function.rc_dict['style'][args[1]]))
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
        label1 = gtk.Label(_('Columns'))
        label1.modify_font(pango.FontDescription('bold'))
        label1.set_justify(gtk.JUSTIFY_LEFT)
        cel_sort = self.listen_cel()
        cel_sort.renderer.connect('toggled', self.fixed_toggled, cel_sort.model)
        button1.connect('clicked', self.downup, cel_sort, True)
        button2.connect('clicked', self.downup, cel_sort, False)
        #############Rc_Cell_Appearance##########
        label2 = gtk.Label(_('Appearance'))
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
        tb1.attach(gtk.Label(_('Expand')), 0, 1, 0, 1)
        tb1.attach(gtk.Label(_('Min size')), 1, 2, 0, 1)
        tb1.attach(gtk.Label(_('Horizontal')), 2, 3, 0, 1)
        tb1.attach(gtk.Label(_('Vertical')), 3, 4, 0, 1)
        
        for i in xrange(len(edna_function.mc)):
            cheak = gtk.CheckButton(None)
            cheak.cl = '%s_expand' % edna_function.mc[i]
            cheak.set_active(int(edna_function.rc_dict['style'][cheak.cl]))
            cheak.connect('toggled', self.toggled)
            
            sp2 = gtk.SpinButton(gtk.Adjustment(0, 0, 100, 1, -1))
            sp2.cl = '%s_size' % edna_function.mc[i]
            sp2.set_value(int(edna_function.rc_dict['style'][sp2.cl]))
            sp2.connect('value_changed', self.spin)
            
            chkH1 = gtk.combo_box_new_text()
            for j in gfH:
                chkH1.append_text(j)
            chkH1.nm = '%s_alignment_h' % edna_function.mc[i]
            chkH1.set_active(gf.index(float(edna_function.rc_dict['style'][chkH1.nm])))
            chkH1.connect('changed', self.chk_c)
            
            chkV1 = gtk.combo_box_new_text()
            for j in gfV:
                chkV1.append_text(j)
            chkV1.nm = '%s_alignment_v' % edna_function.mc[i]
            chkV1.set_active(gf.index(float(edna_function.rc_dict['style'][chkV1.nm])))
            chkV1.connect('changed', self.chk_c)
            
            tb1.attach(cheak, 0, 1, i + 1, i + 2)
            tb1.attach(sp2, 1, 2, i + 1, i + 2)
            tb1.attach(chkH1, 2, 3, i + 1, i + 2)
            tb1.attach(chkV1, 3, 4, i + 1, i + 2)
            
        lb = gtk.Label(_('Columns'))
        vvbox3.pack_start(lb, True)
        for i in xrange(len(edna_function.mc)):
            lb = gtk.Label(edna_gui.Name_Colum[edna_function.mc[i]])
            lb.set_alignment(0.0, 0.5)
            vvbox3.pack_start(lb, True)
        
        hhbox2.pack_start(vvbox3, True)
        hhbox2.pack_start(tb1, False)
        vvbox1.pack_start(hhbox2, False)
        
        hbox2 = gtk.HBox(False, 10)
        label1 = gtk.Label(_('Format of creation'))
        label1.set_alignment(0.0, 0.5)
        entry1 = gtk.Entry()
        entry1.set_text(edna_function.rc_dict['style']['cell_datec_format'])
        entry1.connect('changed', self.on_changed, 'cell_datec_format')
        
        hbox2.pack_start(label1, True)
        hbox2.pack_start(entry1, False)
        
        hbox3 = gtk.HBox(False, 10)
        label2 = gtk.Label(_('Format of change'))
        label2.set_alignment(0.0, 0.5)
        entry2 = gtk.Entry()
        entry2.set_text(edna_function.rc_dict['style']['cell_datem_format'])
        entry2.connect('changed', self.on_changed, 'cell_datem_format')        
        
        hbox3.pack_start(label2, True)
        hbox3.pack_start(entry2, False)
        
        hbox4 = gtk.HBox(False, 3)
        
        chk1 = gtk.combo_box_new_text()
        chk1.append_text(_('in the bytes'))
        chk1.append_text(_('with a floating point Kb, Mb'))
        chk1.append_text(_('with a floating point Kb, Mb, Gb'))
        chk1.set_active(int(edna_function.rc_dict['style']['cell_size_format']))
        chk1.connect('changed', self.chk1_c)
        label3 = gtk.Label(_('Size format'))
        label3.set_alignment(0.0, 0.5)
        
        hbox5 = gtk.HBox(False, 3)
        
        chk2 = gtk.combo_box_new_text()
        chk2.append_text(_('numerical'))
        chk2.append_text(_('string'))
        
        chk2.set_active(int(edna_function.rc_dict['style']['cell_atr_format']))
        chk2.connect('changed', self.chk2_c)
        label4 = gtk.Label(_('Attribute format'))
        label4.set_alignment(0.0, 0.5)
        
        hbox4.pack_start(label3, True)
        hbox4.pack_start(chk1, False)
        hbox5.pack_start(label4, True)
        hbox5.pack_start(chk2, False)
        
        vvbox1.pack_start(hbox2, False)
        vvbox1.pack_start(hbox3, False)
        vvbox1.pack_start(hbox4, False)
        vvbox1.pack_start(hbox5, False)
        self.note.append_page(vvbox1, gtk.Label(_('Table')))
        
    def chk_c(self, *args):
        edna_function.rc_dict['style'][args[0].nm] = str(gf[args[0].get_active()])        
        
    def chk1_c(self, *args):
        edna_function.rc_dict['style']['cell_size_format'] = str(args[0].get_active())
        
    def chk2_c(self, *args):
        edna_function.rc_dict['style']['cell_atr_format'] = str(args[0].get_active())
            
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
        edna_function.rc_dict['style'][args[1]] = args[0].get_text() 

    def spin(self, *args):
        edna_function.rc_dict['style'][args[0].cl] = str(int(args[0].get_value()))
        
    def toggled(self, *args):
        edna_function.rc_dict['style'][args[0].cl] = str(int(args[0].get_active()))

    def fixed_toggled(self, cell, path, model):
        iter = model.get_iter((int(path),))
        fixed = model.get_value(iter, 0)
        fixed = not fixed
        edna_function.rc_dict['style'][model.get_value(iter, 2)] = str(int(fixed))
        model.set(iter, 0, fixed)


def main():
    r = Rc_Window()
    r.show()
    gtk.main()
    return 0

if __name__ == '__main__':
    main()

