class Event(object):
	pass

class Observable(object):
	def __init__(self):
		self.callbacks = []
		
	def subscribe(self, callback):
		self.callbacks.append(callback)
		
	def notifyObservers(self, event):
		event.source = self
		for fn in self.callbacks:
			fn(event)


