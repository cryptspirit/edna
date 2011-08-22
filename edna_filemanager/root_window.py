# -*- coding: utf-8 -*-


import gobject
import gtk
import pygtk
import os
import sys
import time
import edna_gui
import edna_config
import edna_function
import gettext
import glib
from edna_filemanager.search.search_gui_class import SearchWindow

gettext.install('edna', unicode=True)

class Dwindow(gtk.Window):
    search = None
    def __init__(self):
        gtk.Window.__init__(self)
        self.connect('destroy', self.exitt)
        self.__set_window_properties_from_configfile__()
        self.set_title('Edna')
        try: self.set_icon_from_file('%s/share/pixmaps/edna.svg' % sys.prefix)
        except: pass
        # Widget#########################
        hdlbox = gtk.HandleBox()
        hdlbox.add(self.create_menu())
        self.vbox1 = gtk.VBox(False, 0)
        self.hpannel1 = gtk.HBox(True,5)
        self.hpannel1.set_border_width(5)
        self.panel_pile = edna_function.Panel_Pile()
        self.panel_pile.add_panel(edna_gui.listen_cell('0', '0', self.return_panel_pile), '0')
        self.panel_pile.add_panel(edna_gui.listen_cell('1', '1', self.return_panel_pile), '1')
       # self.set_focus(self.panel_pile.get_panel('0').treeview)
        self.set_focus_chain((self.panel_pile.get_panel("0"), self.panel_pile.get_panel("1"), ))
        #################################
        #BOX############################
        for i in xrange(2):
            self.hpannel1.pack_start(self.panel_pile.get_panel(str(i)))
        self.vbox1.pack_start(hdlbox, False)

        self.vbox1.pack_start(self.hpannel1)
        ################################
        #self.connect('key-release-event', self.key_c)
        #self.connect('key-press-event', self.key_c)
        self.add(self.vbox1)
        
    def create_menu(self):
        ui_string = """<ui>
        <menubar>
            <menu name='Commands' action='Commands'>
                <menuitem action='Search'/>
                <menuitem action='RunTerminal'/>
            </menu>
            <menu name='Configurations' action='Configurations'>
                <menuitem action='Config'/>
            </menu>
            <placeholder name='OtherMenus'/>
            <menu name='HelpMenu' action='HelpMenu'>
                <menuitem action='HelpAbout'/>
            </menu>
        </menubar>
        </ui>
        """
        actions = [
            ('Commands', None, '_Commands'),
            ('Search', gtk.STOCK_FIND, None, None, None, self.search_window),
            ('RunTerminal', gtk.STOCK_EXECUTE, _("Run terminal"), None, None, self.run_terminal),
            ('Configurations', None, '_Configurations'),
            ('Config', gtk.STOCK_PREFERENCES, None, None, None, self.config_window),
            ('HelpMenu', gtk.STOCK_HELP),
            ('HelpAbout', None, 'A_bout', None, None, self.help_about),
            ]
        self.ag = gtk.ActionGroup('edit')
        self.ag.add_actions(actions)
        self.ui = gtk.UIManager()
        self.ui.insert_action_group(self.ag, 0)
        self.ui.add_ui_from_string(ui_string)
        self.add_accel_group(self.ui.get_accel_group())
        return self.ui.get_widget('/menubar')
    
    def __set_window_properties_from_configfile__(self):
        """
        Применение свойств окна из конфигурационного файла
        """
        if int(edna_function.rc_dict['style']['window_maximize']):
            self.maximize()
        else:
            self.unmaximize()
            
        window_size = map(int, edna_function.rc_dict['style']['window_size'].split(','))
        self.resize(gtk.gdk.screen_width() - window_size[0], gtk.gdk.screen_height() - window_size[1])
        #print edna_function.rc_dict['style']['window_position']
        #self.move
        #self.set_position(gtk.WIN_POS_CENTER)
        
    
    def __get_window_properties_to_configfile__(self):
        """
        Запись свойств окна для конфигурационного файла
        """
        edna_function.rc_dict['style']['window_size'] = ', '.join(map(str, self.get_size()))
        edna_function.rc_dict['style']['window_maximize'] = str(self.maximize_initially)
        #print self.get_position() # не работает без оконного декоратора (проверить)
        edna_function.save_rc()
    
    def run_terminal(self, folder, command = None):
        current_panel = self.panel_pile.get_panel('0') if self.panel_pile.get_panel('0').treeview.has_focus() else self.panel_pile.get_panel('1')
        os.system("gnome-terminal --working-directory \"" + current_panel.treeview.OOF.Path.get_path() + "\"")
        
    def config_window(self, *args):
        rrr = edna_config.Rc_Window()
        rrr.button_ok.connect('clicked', self.upData, rrr, True)
    
    def search_window(self, *args):
        current_panel = self.panel_pile.get_panel('0') if self.panel_pile.get_panel('0').treeview.has_focus() else self.panel_pile.get_panel('1')
        if not self.search:
            
            self.search = SearchWindow(current_panel.treeview.OOF.Path.get_path())
        self.search.show_all(current_panel.treeview.OOF.Path.get_path())
    
    def help_about(self, *args):
        pass
    
    def return_panel_pile(self):
        '''
        Возвращает объект обработки панелей
        '''
        return self.panel_pile
        
    def upData(self, *args):
        print args
        edna_function.save_rc()
        self.cel[0].upData()
        self.cel[1].upData()
        
    def exitt(self, *args):
        #for i in self.cel: i.Exit_State = True
        self.__get_window_properties_to_configfile__()
        args[0].hide()
        gtk.main_quit()
