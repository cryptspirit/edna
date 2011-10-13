# -*- coding: utf-8 -*-

import gettext

gettext.install('edna', unicode=True)

'''
Переводы имен столбцов списка файлов
'''
Colums_Names = {'cell_name': _('Name'), 
            'cell_type': _('Type'), 
            'cell_size': _('Size'), 
            'cell_datec': _('Created'), 
            'cell_datem': _('Changed'), 
            'cell_user': _('User'), 
            'cell_group': _('Group'), 
            'cell_atr': _('Attribute')}

'''
Клавиши которые необходимо игнорировать в системе горячих клавиш
'''
keys_not_follow = ['<Shift>Shift_L', '<Shift>Shift_R', '<Alt>Alt_L', '<Alt>Alt_R', 'Escape',
                    'Return', '<Control>Control_L', '<Control>Control_R', 'Caps_Lock',
                    '<Alt>ISO_Prev_Group', '<Alt>ISO_Next_Group', '<Control>Shift_R',
                    '<Control>Shift_L', '<Shift>Control_R', '<Shift>Control_L', 'Shift_L',
                    'Shift_R', 'Alt_R', 'Alt_L', 'Control_R', 'Control_L', 'Tab', 
                    'Left', 'Up', 'Right', 'Down', 'minus', 'equal', '<Shift>plus',
                    'Home', 'End', 'Page_Up', 'Page_Down', 'space',
                    'Menu', 'grave', 'Insert', 'semicolon', 'comma', 'period',
                    'slash', 'backslash', 'BackSpace']


keys_not_follow += map(str, xrange(10))
keys_not_follow += map(chr, xrange(65, 123))

'''
Переводы имен функций и команд
'''
hotkeys_function_name = {'action_1': _('Copy'),
                        'action_2': _('Remove'),
                        'action_3': _('Properties'),
                        'action_4': _('Rename'),
                        'action_5': _('Make directory'),
                        'action_6': _('Open terminal'),
                        'action_7': _('View'),
                        'action_8': _('Show hide files'),
                        'action_9': _('Enter path')}

def return_project_structures():
    dict = {}
    dict['colums name'] = Colums_Names
    dict['keys not follow'] = keys_not_follow
    dict['hotkeys function names'] = hotkeys_function_name
    return dict
