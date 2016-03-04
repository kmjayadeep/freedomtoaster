import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
import bootable
from threading import Thread

DEVICE = "/dev/null"

def installIso(self,fileName):
	isoFile="iso/"+fileName
	Thread(target=bootable.createbootable, args=(self,isoFile,DEVICE)).start()
	# bootable.createbootable(isoFile,DEVICE)

def changePage(assistant):
	label = gtk.Label('')
	assistant.add_action_widget(label)
	hbox = label.get_parent()
	hbox.remove(label)
	for child in hbox.get_children():
		label = child.get_label()
		if label == '_Apply':
			child.set_label('Start')

