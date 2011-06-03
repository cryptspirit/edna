#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       search_gui_class.py
#       
#       Copyright 2011 Sevka <sevka@ukr.net>
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
import os
import gettext
from search_thread_class import SearchThread, SearchParams
gettext.install('edna', unicode=True)

class SearchWindow(gtk.Window):
    '''
    Класс окна поиска
    '''
    folder = None    
    paused = False
    
    def addFiles(self,files):
        for file in files:
            self.addFile(file)
        
    def addFile(self,file):
        self.liststore.append((file,))        
    
    def getSearchParams(self):
        '''
        Метод возвращает объект параметров для поиска
        :return: SearchParams
        '''
        params = SearchParams()
        
        params.file_name = self.fileNameEntry.get_text()
        params.file_type = self.fileTypeCombo.get_active()
        params.file_exact = self.exactCB.get_active()
        params.file_case_sensitive = self.caseCB.get_active()
        params.file_regex = self.regexCB.get_active()
        
        params.folder = self.fileChooser.get_current_folder()
        params.folder_recursive = self.folderRecursiveCB.get_active()
        
        params.text_text = self.textEntry.get_text()
        params.text_case_sensitive = self.textCaseCB.get_active()
        params.text_regex = self.textRegexCB.get_active()
        
        #additional
        params.file_hidden = self.hiddenCB.get_active()
        params.use_locate = self.useLocateCB.get_active()
        params.follow_links = self.linksCB.get_active()
        
        return params
        
    def startSearch(self,sender):
        '''
        Запуск поиска
        '''
        self.buttonStart.set_sensitive(0)    
        self.buttonStop.set_sensitive(1)
        self.buttonPause.set_sensitive(1)
        self.buttonPause.set_active(0)        
        self._startSpinner()
        self.statusBox.set_visible(True)
        
        self.liststore = gtk.ListStore(str)
        self.treeview.set_model(self.liststore)
         
        self.searchThread = SearchThread(self.getSearchParams())
        self.searchThread.subscribe(self.update)
        self.searchThread.start() 
        
    def update(self,event):
        '''
        Коллбек, который вызывается SearchThread'ом при возникновении события
        '''
        if event.type == event.TYPE_FILE_FOUND:
            #print event.files
            self.addFiles(event.files)
        elif event.type == event.TYPE_END:
            self.stopSearch()
        elif event.type == event.TYPE_NOTICE:
            self.updateStatus(event.message)
    
    def stopSearch(self,sender = None):
        '''
        Остановка поиска
        '''
        self.buttonStart.set_sensitive(1)    
        self.buttonStop.set_sensitive(0)
        self.buttonPause.set_sensitive(0)
        self.buttonPause.set_active(0)        
        self._stopSpinner()
        self.statusBox.set_visible(False)
        self.searchThread.stop() 
    
    def pauseSearch(self,sender):
        '''
        Поставить поиск на паузу
        '''
        self.paused = not self.paused
        if self.paused:
            self._stopSpinner()
            self.buttonPause.set_label(_('Continue search'))
            self.searchThread.pause() 
        else:
            self._startSpinner()
            self.buttonPause.set_label(_('Pause search'))
            self.searchThread.contin() 
            
    def _startSpinner(self):
        self.spinner.start()
    
    def _stopSpinner(self):
        self.spinner.stop()
            
    def updateStatus(self, message):
        '''
        Обновить статус
        '''
        self.statusLabel.set_label(message)
    
    def regexCBClick(self,sender):
        self.exactCB.set_sensitive(not self.regexCB.get_active())
    
    def __init__(self, folder):
        '''
        Конструктор
        :param folder: Папка, в которой будет осуществляться поиск
        :type folder: string
        '''
        gtk.gdk.threads_init()
        if os.path.exists(folder):
            self.folder = folder
            
        gtk.Window.__init__(self)
        
        self.set_title(_('File search'))
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_default_size(800,500)
        vbox = gtk.VBox(False, 10)
        
        self.tooltips = gtk.Tooltips()
        
        #main params
        mainParamsVBox = gtk.VBox(False,10)

        hbox1 = gtk.HBox(False,0)
        label1 = gtk.Label(_('File name'))
        label1.set_alignment(0,0.5)
        self.fileNameEntry = gtk.Entry()
        self.exactCB = gtk.CheckButton(_('Exact'))
        self.caseCB = gtk.CheckButton(_('Case sensitive'))
        self.regexCB = gtk.CheckButton(_('Regex'))
        self.fileTypeCombo = gtk.combo_box_new_text()
        self.fileTypeCombo.append_text(_('Files and folders'))
        self.fileTypeCombo.append_text(_('Files only'))
        self.fileTypeCombo.append_text(_('Folders only'))
        self.fileTypeCombo.set_active(0)
        hbox1.pack_start(label1, False, False, 10)
        hbox1.pack_start(self.fileNameEntry, True, True)
        hbox1.pack_start(self.fileTypeCombo, False, False,10)
        hbox1.pack_start(self.exactCB, False, False,10)
        hbox1.pack_start(self.caseCB, False, False,10)
        hbox1.pack_start(self.regexCB, False, False,10)
        
        self.regexCB.connect('clicked',self.regexCBClick)

        hbox2 = gtk.HBox(False,0)
        label2 = gtk.Label(_('Search in folder'))
        label2.set_alignment(0,0.5)
        self.fileChooser = gtk.FileChooserButton(_('Select folder'))
        self.fileChooser.set_action(gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)
        if self.folder:
            self.fileChooser.set_current_folder(self.folder)
        self.folderRecursiveCB = gtk.CheckButton(_('Recursive'))
        self.folderRecursiveCB.set_active(True)
        hbox2.pack_start(label2, False, False, 10)
        hbox2.pack_start(self.fileChooser, True, True)
        hbox2.pack_start(self.folderRecursiveCB, False, False, 10)

        hbox3 = gtk.HBox(False,0)
        label3 = gtk.Label(_('Search for text'))
        label3.set_alignment(0,0.5)
        self.textEntry = gtk.Entry()
        self.textCaseCB = gtk.CheckButton(_('Case sensitive'))
        self.textRegexCB = gtk.CheckButton(_('Regex'))
        hbox3.pack_start(label3, False, False, 10)
        hbox3.pack_start(self.textEntry, True, True)
        hbox3.pack_start(self.textCaseCB, False, False, 10)
        hbox3.pack_start(self.textRegexCB, False, False, 10)

        mainParamsVBox.pack_start(hbox1)
        mainParamsVBox.pack_start(hbox2)
        mainParamsVBox.pack_start(hbox3)

        #additional params
        addParamsExpander = gtk.Expander(_('Additional parameters'))
        addParamsHBox = gtk.HBox()

        addParamsVBox1 = gtk.VBox()
        
        self.useLocateCB = gtk.CheckButton(_('Use UNIX \'locate\' command'))
        self.useLocateCB.set_active(True)
        self.tooltips.set_tip(self.useLocateCB, 'Possibly slow for text search')        
        self.hiddenCB = gtk.CheckButton(_('Process hidden files and folders'))
        self.linksCB = gtk.CheckButton(_('Follow simlinks'))
        self.tooltips.set_tip(self.linksCB, 'Attention! Dead locks possible! ') 
        self.linksCB.set_active(True)
        addParamsVBox1.pack_start(self.useLocateCB, False, False)
        addParamsVBox1.pack_start(self.hiddenCB, False, False)
        addParamsVBox1.pack_start(self.linksCB, False, False)
        
        addParamsHBox.pack_start(addParamsVBox1,False, False, 10)

        addParamsExpander.add(addParamsHBox)

        #treeview
        
        self.treeview = gtk.TreeView()
        r = gtk.CellRendererText()
        self.treeview.insert_column_with_attributes(-1, "File name", r, text=0)

        #status box
        self.statusBox = gtk.HBox(False,10)
        self.spinner = gtk.Spinner()
        #self.spinner.set_sensitive(0)

        self.statusLabel = gtk.Label('')
#        statusLabel.set_justify(gtk.JUSTIFY_LEFT)
        self.statusLabel.set_alignment(0,0)
        self.statusLabel.set_width_chars(120)
        self.statusBox.pack_start(self.spinner,False,False,10)
        self.statusBox.pack_start(self.statusLabel, False, False,10)
        
        #button box
        buttonBox = gtk.HButtonBox()
        buttonBox.set_border_width(10)
        self.buttonStart = gtk.Button(_('Start search'))
        self.buttonStop = gtk.Button(_('Stop search'))
        self.buttonPause = gtk.ToggleButton(_('Pause search'))
        self.buttonPause.set_mode(True)
        self.buttonClose = gtk.Button(_('Close'))
        buttonBox.add(self.buttonStart)
        buttonBox.add(self.buttonStop)
        buttonBox.add(self.buttonPause)
        buttonBox.add(self.buttonClose)

        self.buttonClose.connect('clicked', progexit)
        self.buttonStart.connect('clicked', self.startSearch)
        self.buttonStop.connect('clicked', self.stopSearch)
        self.buttonPause.connect('clicked',self.pauseSearch)
        
        self.buttonStop.set_sensitive(0)
        self.buttonPause.set_sensitive(0)        
        
        vbox.pack_start(mainParamsVBox, False, True, 10)
        vbox.pack_start(addParamsExpander, False, True, 0)
        scrolled = gtk.ScrolledWindow()
        scrolled.add(self.treeview)
        vbox.pack_start(scrolled, True, True, 0)
        vbox.pack_start(self.statusBox, False, True, 0)
        vbox.pack_start(buttonBox, False, True, 0)
        self.add(vbox)

        self.connect('destroy',progexit)

        self.show_all()
        maxLabelWidth = max(label1.get_allocation()[2], label2.get_allocation()[2], label3.get_allocation()[2])
        label1.set_size_request(maxLabelWidth,-1)
        label2.set_size_request(maxLabelWidth,-1)
        label3.set_size_request(maxLabelWidth,-1)
        self.statusBox.set_visible(False)
        
def progexit(*args):
    gtk.main_quit()

def main():
    searchWindow = SearchWindow('/home/sevka')
    gtk.main()
    return 0

if __name__ == '__main__':
    main()
