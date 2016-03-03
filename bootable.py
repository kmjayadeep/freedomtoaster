#!/usr/bin/env python3	
import sys
import time
import signal
from subprocess import Popen, PIPE
from decimal import Decimal, localcontext, ROUND_DOWN

def createbootable(fileName,device):
	fileSize = getSize(fileName)
	dd = Popen(['dd'] + ['if='+fileName,'of='+device], stderr=PIPE)
	while dd.poll() is None:
	    time.sleep(.3)
	    dd.send_signal(signal.SIGUSR1)
	    while 1:
	        l = dd.stderr.readline()
	        if b'bytes' in l:
	        	done = int(l[:l.index(b'bytes')-1])
	        	updateProgress(done/fileSize*100)
	        	break

def updateProgress(progress):
	progress=truncFloat(progress)
	print(str(progress) + "%")

def truncFloat(floatNumber):
	with localcontext() as context:
		context.rounding = ROUND_DOWN
		return Decimal(floatNumber).quantize(Decimal('0.01'))

def getSize(fileName):
	file = open(fileName, 'rb')
	file.seek(0,2) # move the cursor to the end of the file
	size = file.tell()
	return int(size)