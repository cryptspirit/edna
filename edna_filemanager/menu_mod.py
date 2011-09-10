# -*- coding: utf-8 -*-

import gtk

'''
Отдельный модуль для контекстных меню
'''

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

