#!/usr/bin/python
import gi
import json
import isolist
import inspect
from subprocess import PIPE,Popen
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
from gi.repository import GdkPixbuf
import bootable

imageWidth=200
imageHeight=200
maxColumns=5
GTK_RESPONSE_ACCEPT=1
GTK_RESPONSE_REJECT=0
DEVICE = "/dev/null"

class Window(gtk.Window):
	def __init__(self,myTitle,isoList):
		self.isoList = isoList
		gtk.Window.__init__(self,title=myTitle)
		self.set_border_width(10)
		self.set_default_size(300, 300)
		self.fullscreen()

		scrolled = gtk.ScrolledWindow()
		scrolled.set_policy(gtk.PolicyType.NEVER, gtk.PolicyType.AUTOMATIC)
		
		grid=gtk.Grid()
		grid.set_orientation(gtk.Orientation.HORIZONTAL)
		grid.set_column_homogeneous(True)
		self.addButtons(grid)
		scrolled.add(grid)

		self.add(scrolled)
		self.show_all()

	def addButtons(self,grid):
		count=0
		for x in range(1):
			for iso in self.isoList:
				box = self.getBox(iso)
				button=gtk.Button()
				button.add(box)
				button.connect("clicked",self.onButtonClick,iso.name)
				grid.attach(button,count%maxColumns,int(count/maxColumns),1,1)
				count+=1

	def getBox(self,iso):

		label = gtk.Label(iso.name)
        
		pixbuf = GdkPixbuf.Pixbuf().new_from_file("iso/"+iso.image)
		pixbuf.scale_simple(imageWidth,imageHeight,GdkPixbuf.InterpType.BILINEAR)

		image = gtk.Image().new_from_pixbuf(pixbuf)
		
		box = gtk.Box()
		box.set_border_width(10)
		box.set_orientation(gtk.Orientation.VERTICAL)
		box.pack_start(image,True,True,2)
		box.pack_end(label,True,True,2)
		return box
	

	def onButtonClick(self,widget,name):
		iso = next(x for x in self.isoList if x.name==name)

		dialog = gtk.Dialog("Are you sure?")
		dialog.add_button("Cancel",GTK_RESPONSE_REJECT)
		dialog.add_button("Yes",GTK_RESPONSE_ACCEPT)
		dialog.set_transient_for(self)
		result = dialog.run()
		if(result==GTK_RESPONSE_ACCEPT):
			installIso(iso.name)
			dialog.close()
		else:
			dialog.close()

def installIso(name):
	isoFile="iso/"+name+".iso"
	print(isoFile)
	bootable.createbootable(isoFile,DEVICE)

def main():
		isoList = isolist.getIsoList()
		win = Window("FREEDOM TOASTER",isoList)
		win.connect("delete-event",gtk.main_quit)
		win.show_all()
		gtk.main()	


def test():
	installIso("ubuntu-gnome-15.04-desktop-i386")


if __name__=="__main__":
	main()
	# test()
