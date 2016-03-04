#!/usr/bin/env python3	
import sys
import time
import signal
from subprocess import Popen, PIPE
from decimal import Decimal, localcontext, ROUND_DOWN
import gi
import os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
from gi.repository import GObject as gobject
window = gtk.Window()

def createbootable(self,fileName,device):
		Popen(['umount',device],stderr=PIPE)
		os.system('mkfs.fat -I '+device)
		fileSize = getSize(fileName)
		dd = Popen(['dd'] + ['if='+fileName,'of='+device], stderr=PIPE, stdout=PIPE)
		print("Started Install")
		while dd.poll() is None:
			time.sleep(.3)
			dd.send_signal(signal.SIGUSR1)
			while 1:
				l = dd.stderr.readline()
				if b'bytes' in l:
					done = int(l[:l.index(b'bytes')-1])
					if(fileSize!=0):
						progress=done/fileSize
						progress=truncFloat(progress)
						copyText = "Copying Files " + str(progress*100) + "%"
						if(progress==1):
							copyText = "Completed"
						gobject.idle_add(self.updateProgress, progress, copyText)
					break
		print("Completed Install")

def truncFloat(floatNumber):
	with localcontext() as context:
		context.rounding = ROUND_DOWN
		return Decimal(floatNumber).quantize(Decimal('0.01'))

def getSize(fileName):
	file = open(fileName, 'rb')
	file.seek(0,2)
	size = file.tell()
	return int(size)