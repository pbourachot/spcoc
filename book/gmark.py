
import os,re

FILENAME = "gbookmarks.html"
FILEOUT = "gbookmarks_lite.html"


class Site:
    
    def __init__(self, desc, url):
        self.desc = desc
        self.url = url
        
        
fullSites = {}



fileIn = open(FILENAME,'r')
data = fileIn.readlines()

fileOut = open(FILEOUT,'w')


for line in data:
    pattern = '<A HREF="(.*?)" ADD_DATE="1511359390000000">(.*?)</A>'
    result = re.findall(pattern , line)
    addLine = True
    if (len(result) > 0 ):
        
        a = result[0]
        
        if (a[1] in fullSites.keys()):
            if (a[0] == fullSites[a[1]].url):
                #print "Identical %s"  %a[1]
                addLine = False
            else :
                print "Strange %s %s => %s %s" %(a[1], a[0], fullSites[a[1]].url , fullSites[a[1]].desc)
        else :
            fullSites[a[1]] = Site(a[1],a[0])
    
    if addLine :    
        fileOut.write(line)


fileOut.close()
fileIn.close()


'''
pattern = '<A HREF="(.*?)" ADD_DATE="1511359390000000">(.*?)</A>'

result = re.findall(pattern , data)


for a in  result:
    #print '%s => %s' %(a[1] , a[0])
    fullSites.append(Site(a[1], a[0]))
    
print len(fullSites)


numOfDuplicate = 0
entries = {}

def findDuplicate(a, numOfDuplicate):
    if ( a.url in entries.keys()):
        numOfDuplicate = numOfDuplicate + 1
    entries[a.url] = "1"
    return numOfDuplicate

for a in fullSites:
    numOfDuplicate = findDuplicate(a, numOfDuplicate)
    
print numOfDuplicate
'''