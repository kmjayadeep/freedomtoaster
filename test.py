#!/usr/bin/python
import gi
import json
import isolist
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
class Window(gtk.Window):
	def __init__(self,myTitle):
		gtk.Window.__init__(self,title=myTitle)
		button=gtk.Button("click")
		button.connect("clicked",self.onButtonClick)
		self.add(button)

	def onButtonClick(self,widget):
		print("clicked")

isoList = isolist.getIsoList()
for iso in isoList:
	iso.printDetails()

win = Window("test")
win.connect("delete-event",gtk.main_quit)
win.show_all()
gtk.main()