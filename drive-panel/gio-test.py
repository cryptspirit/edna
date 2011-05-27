import gio
import time
import gtk

def changed(vm, d):
	drives = vm.get_connected_drives()
	volumes = vm.get_volumes()
	mounts = vm.get_mounts()
	print "----------------------------------------------------------------"
	print d
	#"Changed: " + d.get_name() + "\n"
	
	print "\nDrives:"
	for drive in drives:
		print drive.get_name()
	
	print "\nVolumes:"
	for volume in volumes:
		print volume.get_name()
	
	print "\nMounts:"
	for mount in mounts:
		print mount.get_name()
	

vm = gio.VolumeMonitor()

changed(vm, None)

#vm.connect('drive-connected', changed)
vm.connect('mount-added', changed)
vm.connect('volume-added', changed)
#vm.connect('drive-disconnected', changed)
vm.connect('mount-removed', changed)
vm.connect('volume-removed', changed)
'''
vm.connect('drive-changed', changed)
vm.connect('mount-changed', changed)
vm.connect('volume-changed', changed)
'''


gtk.gdk.threads_init()
gtk.main()

