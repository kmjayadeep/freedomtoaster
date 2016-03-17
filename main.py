#!/usr/bin/python
import gi
import isolist
import bootable
from threading import Thread
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
from gi.repository import Gdk,GdkPixbuf
Gdk.threads_init()

imageWidth=200
imageHeight=200
maxColumns=5
GTK_RESPONSE_ACCEPT=1
GTK_RESPONSE_REJECT=0
GTK_RESPONSE_INFO=2
SURE_TEXT = "Please make sure that the usb drive is inserted \n The Device will be formatted"
DEVICE = "/dev/sdb"
DEVICE = "/dev/null"
CREDITS = "<big>Credits : </big><b>Nisham, Jayadeep, Balagopal (2017)</b>"

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

		box = gtk.Box()
		box.set_orientation(gtk.Orientation.VERTICAL)
		box.pack_start(scrolled,True,True,0)
		box.pack_start(getCredits(),False,True,10)
		
		self.add(box)
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
		self.assistant = gtk.Assistant()
		self.assistant.connect("cancel", cancel_button_clicked)
		self.assistant.connect("close", cancel_button_clicked)
		self.set_default_size(600,600)
		self.assistant.set_resizable(False)


		pages=self.generatePages(self.iso)
		for page in pages:
			box=page[0]
			title=page[1]
			pagetype=page[2]
			self.assistant.append_page(box)
			self.assistant.set_page_type(box, pagetype)
			self.assistant.set_page_title(box, title)
			self.assistant.set_page_complete(box, True)
			if(len(page)>3):
				self.box = box
				self.assistant.set_page_complete(box,False)

		changePage(self.assistant)
		self.assistant.show_all()
		self.assistant.set_forward_page_func(self.pageForward)


	def pageForward(self,page):
		if page==1:
			installIso(self,self.iso.filename)
		return page+1

	def generatePages(self,iso):
		pages = []
		boxIntro = gtk.Box(orientation=gtk.Orientation.VERTICAL)
		label = gtk.Label(label=iso.description)
		label.set_line_wrap(True)
		boxIntro.pack_start(label, True, True, 0)

		boxConfirm = gtk.Box(orientation=gtk.Orientation.VERTICAL)
		label = gtk.Label(label=SURE_TEXT)
		label.set_line_wrap(True)
		boxConfirm.pack_start(label, True, True, 0)

		boxProgress = gtk.Box(orientation=gtk.Orientation.VERTICAL)
		self.label = gtk.Label(label="Copying Files")
		self.label.set_line_wrap(True)
		boxProgress.pack_start(self.label,True,True,0)
		self.origProgressBar = gtk.ProgressBar()
		self.origProgressBar.set_fraction(0.0)
		boxProgress.pack_start(self.origProgressBar,True,True,0)

		boxSummary = gtk.Box(orientation=gtk.Orientation.VERTICAL)
		label = gtk.Label(label="The Bootable disk was created Successfully")
		label.set_line_wrap(True)
		boxSummary.pack_start(label, True, True, 0)


		pages.append([boxIntro,iso.name,gtk.AssistantPageType.INTRO])
		pages.append([boxConfirm,"Are you sure?",gtk.AssistantPageType.CONFIRM])
		pages.append([boxProgress,"Install",gtk.AssistantPageType.PROGRESS,self.origProgressBar])
		pages.append([boxSummary,"Complete",gtk.AssistantPageType.SUMMARY])
		return pages


	def updateProgress(self,progress,text):
		self.origProgressBar.set_fraction(progress)
		self.label.set_label(text)
		self.assistant.set_page_complete(self.box,progress==1)
		# print(str(progress*100)+"%")

def cancel_button_clicked(assistant):
	assistant.destroy()

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

def getCredits():
	label=gtk.Label();
	label.set_markup(CREDITS)
	label.set_line_wrap(True)
	return label

def main():
	isoList = isolist.getIsoList()
	win = Window("Hidden Easter Egg",isoList)
	win.connect("delete-event",gtk.main_quit)
	win.show_all()
	gtk.main()	

if __name__=="__main__":
	main()
