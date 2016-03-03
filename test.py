#!/usr/bin/python
import gi
import isolist
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
from gi.repository import GdkPixbuf
import bootable

imageWidth=200
imageHeight=200
maxColumns=5
GTK_RESPONSE_ACCEPT=1
GTK_RESPONSE_REJECT=0
GTK_RESPONSE_INFO=2
DEVICE = "/dev/null"
SURE_TEXT = "Please make sure that the usb drive is inserted"

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

		dialog = gtk.MessageDialog(self)
		dialog.add_button("Cancel",GTK_RESPONSE_REJECT)
		dialog.add_button("More Info",GTK_RESPONSE_INFO)
		dialog.add_button("Yes",GTK_RESPONSE_ACCEPT)
		dialog.format_secondary_text(iso.description+"\n\n"+SURE_TEXT)
		dialog.props.text = "Proceed to Install?" 

		result = dialog.run()
		if(result==GTK_RESPONSE_ACCEPT):
			dialog.close()
			self.progressStep(iso)
		elif(result==GTK_RESPONSE_INFO):
			infoDialog = gtk.MessageDialog(dialog)
			infoDialog.format_secondary_text(iso.longdescription)
			infoDialog.add_button("OK",GTK_RESPONSE_ACCEPT)
			infoDialog.run()
			infoDialog.close()
		else:
			dialog.close()

	def progressStep(self,iso):
		self.progressBar = gtk.ProgressBar()
		self.progressDialog = gtk.Dialog()
		self.progressDialog.add(self.progressBar)
		installIso(self,iso.filename)

	def updateProgress(self,progress):
		self.progressBar.set_fraction(progress)
		print(str(progress*100)+"%")

def installIso(window,fileName):
	isoFile="iso/"+fileName
	bootable.createbootable(window,isoFile,DEVICE,window.updateProgress)

def main():
		isoList = isolist.getIsoList()
		win = Window("FREEDOM TOASTER",isoList)
		win.connect("delete-event",gtk.main_quit)
		win.show_all()
		gtk.main()	

if __name__=="__main__":
	main()
