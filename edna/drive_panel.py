# -*- coding: utf-8 -*-


import gtk
import gio
import os
import pynotify

class Drive():
    '''
    Класс для драйвов драйвов типа / и ~.
    Возможно в настройках можно будет добавлять какие-то кастомные драйвы
    '''
    def __init__(self, name, path):
        self.name = name
        self.path = path
        
class DriveEvent():
    '''
    Класс события происходящего на драйв-панели. 
    TYPE_CD - смена каталога
    TYPE_UNMOUNT - отмонтирование устройства (еще не реализовано)
    '''
    TYPE_CD = 1
    TYPE_UNMOUNT = 2
    
    def __init__(self, type, param):
        self.type = type
        if type in (self.TYPE_CD, self.TYPE_UNMOUNT):
            self.path = param
        
class DrivePanel(gtk.Toolbar):
    '''
    Виджет драйв-панели
    '''
    def __init__(self, callback):
        '''
        Конструктор панели
        :param callback: Метод-коллбек, который будет вызван при возникновении 
            события. В качестве параметра будет передан объект DriveEvent
        '''
        gtk.Toolbar.__init__(self)
        self.set_can_focus(False)
        self.callback = callback
        self.set_style(gtk.TOOLBAR_BOTH_HORIZ)  #TOOLBAR_ICONS
        self.set_icon_size(gtk.ICON_SIZE_SMALL_TOOLBAR)
        self.vm = gio.VolumeMonitor()
        self.vm.connect('volume-added', self.volume_changed)
        self.vm.connect('volume-removed', self.volume_changed)
        self.vm.connect('mount-added', self.volume_changed)
        self.vm.connect('mount-removed', self.volume_changed)        
        self.refresh(self.vm)
        
    def create_menu(self, mount):
        actions = []
        ui_string = """<ui>
        <popup>"""
        if mount.can_unmount():
            ui_string = ui_string + "<menuitem action='Unmount'/>"
            actions.append(('Unmount', gtk.STOCK_CLOSE, 'Unmount', None, None, self.drive_unmount)), #STOCK_GO_TOP
        if mount.can_eject():
            ui_string = ui_string + "<menuitem action='Eject'/>"
            actions.append(('Eject', gtk.STOCK_CLOSE, 'Eject', None, None, self.drive_eject)), #STOCK_GO_TOP
        ui_string = ui_string + """</popup>
        </ui>
        """
        
        self.ag = gtk.ActionGroup('edit')
        self.ag.add_actions(actions, mount)
        self.ui = gtk.UIManager()
        self.ui.insert_action_group(self.ag, 0)
        self.ui.add_ui_from_string(ui_string)
        #self.add_accel_group(self.ui.get_accel_group())
        return self.ui.get_widget('/popup')
    def unmount_callback(self,a,b):
        try:
            a.unmount_finish(b)
        except:
            n = pynotify.Notification('Edna', 'Cannot unmount ' + a.get_root().get_path(), gtk.STOCK_DIALOG_ERROR)
            n.show()
    def eject_callback(self,a,b):
        try:
            a.eject_finish(b)
        except:
            print "Cannot eject"
    def drive_unmount(self, a, mount):
        self.callback(DriveEvent(DriveEvent.TYPE_UNMOUNT, mount.get_root().get_path()))
        if mount.can_unmount():
            mount.unmount(self.unmount_callback)
            
    def drive_eject(self, a, mount):
        self.callback(DriveEvent(DriveEvent.TYPE_UNMOUNT, mount.get_root().get_path()))
        if mount.can_eject():
            mount.eject(self.eject_callback)        
            
    def volume_changed(self, vm, volume):
        '''
        Метод вызывается при любом изменении устройств (отмонтирование, примонтирование)
        '''
        self.refresh(self.vm)
        
    def refresh(self, vm):
        '''
        Полная перерисовка кнопок на драйв-панели
        '''
        for child in self.get_children():
            self.remove(child)
        uris = []
        # рут и хоум
        b = gtk.ToolButton(gtk.STOCK_HARDDISK)
        b.set_label('/')
        b.set_tooltip_text('/') 
        b.connect('clicked', self.clicked, Drive('/','/'))
        self.insert(b, self.get_n_items())
        
        b = gtk.ToolButton(gtk.STOCK_HOME)
        b.set_label('~')
        b.set_tooltip_text(os.path.expanduser('~'))
        b.connect('clicked', self.clicked, Drive('Home', os.path.expanduser('~')))
        self.insert(b, self.get_n_items())
        
        # volumes
        volumes = vm.get_volumes()
        for volume in volumes:
            mount = volume.get_mount()
            if mount:
                uri = mount.get_root().get_uri()
                uris.append(uri)
            else:
                uri = None
            image = gtk.Image()
            image.set_from_gicon(volume.get_icon(),gtk.ICON_SIZE_MENU)
            if volume.get_mount() and (volume.get_mount().can_eject() or volume.get_mount().can_unmount()):
                b = gtk.MenuToolButton(image, volume.get_name())
                b.set_menu(self.create_menu(volume.get_mount()))
            else:
                b = gtk.ToolButton(image, volume.get_name())
            b.set_tooltip_text(volume.get_mount().get_root().get_path() if volume.get_mount() else volume.get_name())
            b.set_is_important(True)
            b.connect('clicked', self.clicked, volume)
            self.insert(b, self.get_n_items())
            
        #mounts
        mounts = vm.get_mounts()
        for mount in mounts:
            if mount.get_root().get_uri() not in uris:
                image = gtk.Image()
                image.set_from_gicon(mount.get_icon(),gtk.ICON_SIZE_MENU)
                if mount.can_eject() or mount.can_unmount():
                    b = gtk.MenuToolButton(image, mount.get_name())
                    b.set_menu(self.create_menu(mount))
                else:
                    b = gtk.ToolButton(image, mount.get_name())
                b.set_tooltip_text(mount.get_root().get_path())
                b.set_is_important(True)
                b.connect('clicked', self.clicked, mount)
                self.insert(b, self.get_n_items())
        
        self.show_all()

    def async_result_callback(self, volume, response):
        '''
        Коллбек, который вызывается при завершении монтирования
        '''
        print self, volume, response
        if volume.get_mount():
            self.clicked(self, volume)
            
    def clicked(self, sender, item):
        '''
        Клик по кнопке
        '''
        m = None
        path = None
        if isinstance(item, gio.Volume):
            m = item.get_mount()
            if not m and item.can_mount():
                item.mount(gio.MountOperation(), self.async_result_callback)
        elif isinstance(item, gio.Mount):
            m = item
        else:
            path = item.path
        if m:
            path = m.get_root().get_path()
        if path:    
            self.callback(DriveEvent(DriveEvent.TYPE_CD, path))

def main():
    d = DrivePanel(None)
    w = gtk.Window()
    vbox = gtk.VBox(False, 10)
    vbox.pack_start(d, False, False)
    w.add(vbox)
    w.set_position(gtk.WIN_POS_CENTER)
    w.set_default_size(800,500)
    w.show_all()
    gtk.main()
    return 0

if __name__ == '__main__':
    main()

