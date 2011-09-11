# -*- coding: utf-8 -*-

import gio
import gtk
import glib
import os

type_ico_load = gtk.ICON_LOOKUP_USE_BUILTIN
get_theme = gtk.icon_theme_get_default()
default_applications_icon = 'applications-internet'


def __get_icon_for_app__(app):
    '''
    Получение иконки в формате gtk.gdk.Pixbuf по имени в теме либо абсолютному пути
    '''
    icon_from_theme = app.get_icon()
    if icon_from_theme:
        if type(icon_from_theme) == gio.FileIcon:
            path_to_icon = icon_from_theme.get_file().get_path()
            if os.path.isfile(path_to_icon):
                return gtk.gdk.pixbuf_new_from_file_at_size(path_to_icon, 24, 24)
            else:
                return icon_load_try(default_applications_icon, 24)
        else:
            return icon_load_try(icon_from_theme.get_names()[0], 24)
    else:
        return icon_load_try(default_applications_icon, 24)    

    
class Apps_Cells(gtk.TreeView):
    '''
    Список для файлов рабочего стола
    '''
    def __init__(self, filetype, apps=False):
        gtk.TreeView.__init__(self)
        self.set_rules_hint(True)
        #self.set_grid_lines(False)
        self.get_selection().set_mode(gtk.SELECTION_BROWSE)
        if apps:
            self.Apps_list = [i for i in gio.app_info_get_all_for_type(filetype) if i != gio.app_info_get_default_for_type(filetype, False)]
        else:
            self.Apps_list = [i for i in gio.app_info_get_all() if i != gio.app_info_get_default_for_type(filetype, False)]
        
    def __get_model__(self):
        '''
        Создание модели
        '''
        model = gtk.ListStore(gtk.gdk.Pixbuf, str, gio.unix.DesktopAppInfo)
        for item in self.Apps_list:
            iter = model.append()
            model.set(iter)
            model.set_value(iter, 0, __get_icon_for_app__(item))
            model.set_value(iter, 1, item.get_name())
            model.set_value(iter, 2, item)
        return model
        
    def __add_columns__(self):
        '''
        Создание столбца
        '''
        model = self.get_model()
        column = gtk.TreeViewColumn()
        column.set_title('Application')
        renderer = gtk.CellRendererPixbuf()
        column.pack_start(renderer, False)
        column.set_attributes(renderer, pixbuf=0)
        #column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        #column.expand = True
        renderer = gtk.CellRendererText()
        column.pack_start(renderer, True)
        column.set_attributes(renderer, text=1)
        
        self.append_column(column)
        
    def cells_refresh(self):
        '''
        Обновление списка
        '''
        self.set_model(self.__get_model__())
        self.__add_columns__()
        try:
            self.set_cursor(0)
        except:
            pass


class App_Box(gtk.Frame):
    '''
    Виджет списков приложений
    '''
    def __init__(self, filetype, flag=False):
        gtk.Frame.__init__(self)
        if flag:
            self.set_label('Default applications for type %s:' % filetype)
        else:
            self.set_label('Proposed default application for type %s:' % filetype)
            
        scrol1 = gtk.ScrolledWindow()
        scrol1.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        scrol1.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        self.apps_list = Apps_Cells(filetype, flag)
        self.apps_list.cells_refresh()
        scrol1.add(self.apps_list)
        vbox3 = gtk.VBox(False, 10)
        vbox3.set_border_width(5)
        vbox3.pack_start(scrol1)
        self.add(vbox3)
        
class App_Info_Box(gtk.Frame):
    '''
    Виджет информации о приложении
    '''
    def __init__(self, promt, filetype):
        gtk.Frame.__init__(self)
        self.filetype = filetype
        self.set_label('%s %s:' % (promt, filetype))
        self.icon_image = gtk.Image()
        self.label_name_app = gtk.Label('Test')
        self.label_name_app.set_alignment(0.0, 0.5)
        self.label_description_app = gtk.Label('Test')
        self.label_description_app.set_alignment(0.0, 0.5)
        self.__set_new_app__(gio.app_info_get_default_for_type(filetype, False))
        
        vbox2 = gtk.VBox(False, 10)
        hbox1 = gtk.HBox(False, 10)
        
        vbox2.pack_start(self.label_name_app)
        vbox2.pack_start(self.label_description_app)
        
        hbox1.set_border_width(5)
        hbox1.pack_start(self.icon_image, False)
        hbox1.pack_start(vbox2)
        self.add(hbox1)
        
    def set_new_app(self, *args):
        '''
        Установка в буфер приложения для ассоциации
        '''
        selection = args[0].get_selection()
        model_sel, iter_sel = selection.get_selected()
        self.__set_new_app__(model_sel.get_value(iter_sel, 2))
        
    def set_app_from_file(self, file):
        '''
        Установка в буфер приложения для ассоциации на основе файла
        '''
        dirpath = os.path.dirname(file)
        in_path = False
        for i in os.getenv('PATH').split(':'):
            if i == dirpath:
                in_path = True
                break
        if in_path: file = os.path.basename(file)
        self.__set_new_app__(gio.AppInfo(file, os.path.basename(file)))
        
    def __set_new_app__(self, app):
        '''
        Установка в буфер приложения для ассоциации
        '''
        self.Default_App = app
        self.icon_image.set_from_pixbuf(__get_icon_for_app__(app))
        description = app.get_description()
        if description: pass
        else: description = ''
        self.label_name_app.set_text(app.get_name())
        self.label_description_app.set_text(description)
    
    def set_app(self):
        '''
        Установка приложения для ассоциации по умолчанию
        '''
        gio.AppInfo.set_as_default_for_type(self.Default_App, self.filetype)
        
class Apps_Choose_Window(gtk.Window):
    
    def __init__(self, filetype):
        gtk.Window.__init__(self)
        self.set_default_size(400, 550)
        self.set_title('Change default application for type')
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_modal(True)
        
        frame1 = App_Info_Box('Default application for type', filetype)
        frame2 = App_Box(filetype, True)
        frame3 = App_Info_Box('Default application for type', filetype)
        frame4 = App_Box(filetype)
        
        frame2.apps_list.connect('cursor-changed', frame3.set_new_app)
        frame4.apps_list.connect('cursor-changed', frame3.set_new_app)
        
        hbox2 = gtk.HBox(False, 10)
        vbox1 = gtk.VBox(False, 10)
        vbox1.set_border_width(5)
        
        button_ok = gtk.Button(stock='gtk-ok')
        button_cancel = gtk.Button(stock='gtk-cancel')
        button_app = gtk.FileChooserButton('')
        button_app.connect('file-set', self.__add_app__, frame3)
        
        button_ok.connect('clicked', self.__change_app__, frame3)
        button_cancel.connect('clicked', lambda w: self.hide())
        self.connect('destroy', lambda w: self.hide())
        
        hbox2.pack_start(button_ok)
        hbox2.pack_start(button_cancel)
        
        vbox1.pack_start(frame1, False)
        vbox1.pack_start(frame2)
        vbox1.pack_start(frame3, False)
        vbox1.pack_start(frame4)
        vbox1.pack_start(button_app, False)
        vbox1.pack_start(hbox2, False)
        self.add(vbox1)
        #self.show_all()
    
    def __add_app__(self, *args):
        args[1].set_app_from_file(args[0].get_file().get_path())
    
    def __change_app__(self, *args):
        args[1].set_app()
        self.hide()
            
            
def icon_load_try(name, size):
    '''
    Безопасная процедура загрузки иконок
    '''
    try:
        return get_theme.load_icon(name, size, type_ico_load)
    except glib.GError:
        return get_theme.load_icon('applications-internet', size, type_ico_load)
            
            
def main():
    file = '/home/mort/Spark/Zheleznyj.rycar.2011.DUAL.BDRip.XviD.AC3.-HQCLUB.avi'
    #file = '/home/mort/Box/N70/API_Reference_for_Python.pdf'
    t = get_mime(file, True)
    w = Apps_choose_window(t)
    gtk.main()
    
    return 0

if __name__ == '__main__':
    main()

