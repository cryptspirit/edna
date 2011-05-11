import threading
import observer
import time

class SearchParams():
	FILE_TYPE_BOTH = 0
	FILE_TYPE_FILES_ONLY = 1
	FILE_TYPE_FOLDERS_ONLY = 2

	folder = None
	folderRecursive = True
	
	fileName = None
	fileType = 0
	fileExact = False
	fileCaseSensitive = False
	fileRegEx = False
	

class SearchThread(threading.Thread,observer.Observable):
	
	STATUS_STOPPED = 0
	STATUS_RUNNED = 1
	STATUS_PAUSED = 2
	
	status = 0
		
	def __init__(self, params):
		threading.Thread.__init__(self)
		observer.Observable.__init__(self)
		self.params = params
		
	def run(self):
		print 'Start search'
		print self.params.folder + " " + str(self.params.fileType)
		self.status = self.STATUS_RUNNED
		while 1:
			e = observer.Event()
			e.message = "Bla-bla-bla"
			self.notifyObservers(e)
			time.sleep(1)
			if (self.status == self.STATUS_PAUSED):
				while 1:
					if self.status != self.STATUS_PAUSED:
						break
					time.sleep(1)
			if(self.status == self.STATUS_STOPPED):
				break
	
	def pause(self):
		self.status = self.STATUS_PAUSED
		
	def contin(self):
		self.status = self.STATUS_RUNNED
	
	def stop(self):
		self.status = self.STATUS_STOPPED
