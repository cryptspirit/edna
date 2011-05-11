import gtk
import os
from search_thread_class import SearchThread, SearchParams

class SearchWindow(gtk.Window):
	folder = None	
	paused = False
	
	def getSearchParams(self):
		params = SearchParams()
		
		params.fileName = self.fileNameEntry.get_text()
		params.fileType = self.fileTypeCombo.get_active()
		params.fileExact = self.exactCB.get_active()
		params.fileCaseSensitive = self.caseCB.get_active()
		params.fileRegEx = self.regexCB.get_active()
		
		params.folder = self.fileChooser.get_current_folder()
		params.folderRecursive = self.folderRecursiveCB.get_active()
		return params
		
	def startSearch(self,sender):
		
		self.buttonStart.set_sensitive(0)	
		self.buttonStop.set_sensitive(1)
		self.buttonPause.set_sensitive(1)
		self.buttonPause.set_active(0)		
		self._startSpinner()
		self.statusBox.set_visible(True)
		
		self.searchThread = SearchThread(self.getSearchParams())
		self.searchThread.subscribe(self.update)
		self.searchThread.start() 
		
	def update(self,event):
		print event.message
	
	def stopSearch(self,sender):
		self.buttonStart.set_sensitive(1)	
		self.buttonStop.set_sensitive(0)
		self.buttonPause.set_sensitive(0)
		self.buttonPause.set_active(0)		
		self._stopSpinner()
		self.statusBox.set_visible(False)
		self.searchThread.stop() 
	
	def pauseSearch(self,sender):
		self.paused = not self.paused
		if self.paused:
			self._stopSpinner()
			self.buttonPause.set_label('Continue search')
			self.searchThread.pause() 
		else:
			self._startSpinner()
			self.buttonPause.set_label('Pause search')			
			self.searchThread.contin() 
			
	def _startSpinner(self):
		self.spinner.start()
	
	def _stopSpinner(self):
		self.spinner.stop()	
	
	def __init__(self, folder):
		gtk.gdk.threads_init()
		if os.path.exists(folder):
			self.folder = folder
			
		gtk.Window.__init__(self)
		
		self.set_title('File search')
		self.set_position(gtk.WIN_POS_CENTER)
		self.set_default_size(800,500)
		vbox = gtk.VBox(False, 10)
		
		#main params
		mainParamsVBox = gtk.VBox(False,10)

		hbox1 = gtk.HBox(False,0)
		label1 = gtk.Label('File name')
		self.fileNameEntry = gtk.Entry()
		self.exactCB = gtk.CheckButton('Exact')
		self.caseCB = gtk.CheckButton('Case sensitive')
		self.regexCB = gtk.CheckButton('Regex')
		self.fileTypeCombo = gtk.combo_box_new_text()
		self.fileTypeCombo.append_text('Files and folders')
		self.fileTypeCombo.append_text('Files only')
		self.fileTypeCombo.append_text('Folders only')
		self.fileTypeCombo.set_active(0)
		hbox1.pack_start(label1, False, False, 10)
		hbox1.pack_start(self.fileNameEntry, True, True)
		hbox1.pack_start(self.fileTypeCombo, False, False,10)
		hbox1.pack_start(self.exactCB, False, False,10)
		hbox1.pack_start(self.caseCB, False, False,10)
		hbox1.pack_start(self.regexCB, False, False,10)


		hbox2 = gtk.HBox(False,0)
		label2 = gtk.Label('Search in folder')
		self.fileChooser = gtk.FileChooserButton('ChooseFolder')
		self.fileChooser.set_action(gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)
		if self.folder:
			self.fileChooser.set_current_folder(self.folder)
		self.folderRecursiveCB = gtk.CheckButton('Recursive')
		self.folderRecursiveCB.set_active(True)
		hbox2.pack_start(label2, False, False, 10)
		hbox2.pack_start(self.fileChooser, True, True)
		hbox2.pack_start(self.folderRecursiveCB, False, False, 10)

		mainParamsVBox.pack_start(hbox1)
		mainParamsVBox.pack_start(hbox2)

		#additional params
		addParamsExpander = gtk.Expander('Additional parameters')
		addParamsHBox = gtk.HBox(False,0)

		addParamsVBox1 = gtk.VBox()

		addParamsHBox.pack_start(addParamsVBox1)

		addParamsExpander.add(addParamsHBox)

		#treeview
		treeView = gtk.TreeView()
		
		#status box
		self.statusBox = gtk.HBox(False,10)
		self.spinner = gtk.Spinner()
		#self.spinner.set_sensitive(0)

		statusLabel = gtk.Label('Test')
#		statusLabel.set_justify(gtk.JUSTIFY_LEFT)
		statusLabel.set_alignment(0,0)
		self.statusBox.pack_start(self.spinner,False,False,10)
		self.statusBox.pack_start(statusLabel, True, True,10)
		
		#button box
		buttonBox = gtk.HButtonBox()
		buttonBox.set_border_width(10)
		self.buttonStart = gtk.Button('Start search')
		self.buttonStop = gtk.Button('Stop search')
		self.buttonPause = gtk.ToggleButton('Pause search')
		self.buttonPause.set_mode(True)
		self.buttonClose = gtk.Button('Close')
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
		vbox.pack_start(treeView, True, True, 0)
		vbox.pack_start(self.statusBox, False, True, 0)
		vbox.pack_start(buttonBox, False, True, 0)
		self.add(vbox)

		self.connect('destroy',progexit)

		self.show_all()		
		self.statusBox.set_visible(False)
def progexit(*args):
	gtk.main_quit()
	
searchWindow = SearchWindow('/home/sevka/pub')
gtk.main()
