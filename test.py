#!/usr/bin/python
import gi
import json
import isolist
import inspect
print(inspect.getfile(gi))
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
class Window(gtk.Window):
	def __init__(self,myTitle,isoList):
		self.isoList = isoList
		gtk.Window.__init__(self,title=myTitle)
		self.set_border_width(10)
		self.set_default_size(300, 250)

		header = gtk.HeaderBar(title = myTitle)
		header.set_subtitle("subtitle")
		header.props.show_close_button=True

		
		scrolled = gtk.ScrolledWindow()
		scrolled.set_policy(gtk.PolicyType.NEVER, gtk.PolicyType.AUTOMATIC)
		
		flowbox = gtk.FlowBox()
		flowbox.set_valign(gtk.Align.START)
		flowbox.set_max_children_per_line(30)
		flowbox.set_selection_mode(gtk.SelectionMode.NONE)

		self.addStuff(flowbox)
		scrolled.add(flowbox)


		self.add(scrolled)
		self.show_all()

	def addStuff(self,flowbox):		
		for iso in self.isoList:
			button=gtk.Button(iso.name)
			button.connect("clicked",self.onButtonClick,iso.name)
			flowbox.add(button)


	def onButtonClick(self,widget,name):
		iso = next(x for x in self.isoList if x.name==name)
		

def main():
		isoList = isolist.getIsoList()
		win = Window("test",isoList)
		win.connect("delete-event",gtk.main_quit)
		win.show_all()
		gtk.main()	

main()
