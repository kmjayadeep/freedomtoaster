#!/usr/bin/python
import gi
import isolist
import helper
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
from gi.repository import GdkPixbuf

imageWidth=200
imageHeight=200
maxColumns=5
GTK_RESPONSE_ACCEPT=1
GTK_RESPONSE_REJECT=0
GTK_RESPONSE_INFO=2
SURE_TEXT = "Please make sure that the usb drive is inserted"
installing = False

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
		self.iso = iso
		self.createAssistant()
		
	def createAssistant(self):
		assistant = gtk.Assistant()
		assistant.connect("cancel", cancel_button_clicked)
		assistant.connect("close", cancel_button_clicked)
		pages=self.generatePages(self.iso)
		for page in pages:
			box=page[0]
			title=page[1]
			pagetype=page[2]
			assistant.append_page(box)
			assistant.set_page_type(box, pagetype)
			assistant.set_page_title(box, title)
			assistant.set_page_complete(box, True)
		helper.changePage(assistant)
		assistant.show_all()
		assistant.set_forward_page_func(self.pageForward)


	def pageForward(self,page):
		print(page)
		if page==1:
			helper.installIso(self.iso.filename)
		return page+1

	def generatePages(self,iso):
		pages = []
		boxOne = gtk.Box(orientation=gtk.Orientation.VERTICAL)
		label = gtk.Label(label=iso.description)
		label.set_line_wrap(True)
		boxOne.pack_start(label, True, True, 0)

		boxTwo = gtk.Box(orientation=gtk.Orientation.VERTICAL)
		label = gtk.Label(label="Copying Files")
		label.set_line_wrap(True)
		boxTwo.pack_start(label,True,True,0)
		self.origProgressBar = gtk.ProgressBar()
		self.origProgressBar.set_fraction(0.0)
		boxTwo.pack_start(self.origProgressBar,True,True,0)

		boxThree = gtk.Box(orientation=gtk.Orientation.VERTICAL)
		label = gtk.Label(label="The Bootable disk was created Successfully")
		label.set_line_wrap(True)
		boxThree.pack_start(label, True, True, 0)

		boxFour = gtk.Box(orientation=gtk.Orientation.VERTICAL)
		label = gtk.Label(label=SURE_TEXT)
		label.set_line_wrap(True)
		boxFour.pack_start(label, True, True, 0)
		# self.progressBar = gtk.ProgressBar()
		# self.progressBar.set_fraction(0.0)
		# boxFour.pack_start(self.progressBar,True,True,0)


		pages.append([boxOne,iso.name,gtk.AssistantPageType.INTRO])
		# pages.append([boxFour,"Are you sure?",gtk.AssistantPageType.CONFIRM,self.progressBar])
		pages.append([boxFour,"Are you sure?",gtk.AssistantPageType.CONFIRM])
		# pages.append([boxTwo,"Install",gtk.AssistantPageType.PROGRESS,self.origProgressBar])
		pages.append([boxThree,"Complete",gtk.AssistantPageType.SUMMARY])
		return pages

def cancel_button_clicked(assistant):
	assistant.destroy()

def main():
	isoList = isolist.getIsoList()
	win = Window("Hidden Easter Egg",isoList)
	win.connect("delete-event",gtk.main_quit)
	win.show_all()
	gtk.main()	

if __name__=="__main__":
	main()
