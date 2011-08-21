# -*- coding: utf-8 -*-

import gtk
        
def main():
    gtk.gdk.threads_init()
    edna_window = root_window.Dwindow()
    edna_window.show_all()
    gtk.gdk.threads_enter()
    gtk.main()
    gtk.gdk.threads_leave()
    return 0
