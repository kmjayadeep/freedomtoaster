import os
import re
from xml.dom.minidom import parse
import xml.dom.minidom

numIsos = 0
class Iso:
    def __init__(self):
        self.name = ''
        self.description = ''
        self.longdescription = ''
        self.image = ''
        self.filename = ''

def getIsoList():    
    numIsos = 0          
    isoList = []
    filelist = os.listdir('iso/')
    filelist.sort()

    # for every file in the directory
    for filename in filelist:
        if re.search('\.xml$', filename):
            iso = Iso()
            DOMTree = parse('iso/'+filename)

            node = DOMTree.documentElement

            name = node.getElementsByTagName('name')
            iso.name = name[0].childNodes[0].data
                    
            name = node.getElementsByTagName('description')
            iso.description = name[0].childNodes[0].data
                    
            name = node.getElementsByTagName('longdescription')
            iso.longdescription = name[0].childNodes[0].data
                    
            name = node.getElementsByTagName('picture')
            iso.image = name[0].childNodes[0].data

            name = node.getElementsByTagName('filename')
            iso.filename = name[0].childNodes[0].data

            isoList.append(iso)
            numIsos += 1

    return isoList

def getNoIsos():
           return numIsos