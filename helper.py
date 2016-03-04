import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
import bootable

DEVICE = "/dev/null"

def installIso(fileName):
	isoFile="iso/"+fileName
	bootable.createbootable(isoFile,DEVICE)

def changePage(assistant):
	label = gtk.Label('')
	assistant.add_action_widget(label)
	hbox = label.get_parent()
	hbox.remove(label)
	for child in hbox.get_children():
		label = child.get_label()
		if label == '_Apply':
			child.set_label('Start')

