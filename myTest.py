

import urllib
import re

urlPrefix = "http://resultats.ffbb.com/organisation/engagements/" 
code = "27b5"
url = urlPrefix + code + ".html"


def retrieveCorrectUrl(cat,url):
    part1, part2 =  re.findall('r=(.*)&d=(.*)', url)[0]
    u = urlPrefix + url
    h1 = hex(int(part1))[2:]
    h2 = hex(int(part2))[2:]
    value = "%s%s%s" %(h1,h2,code)
  
    return "http://resultats.ffbb.com/championnat/equipe/division/%s.html" %value
      
f = urllib.urlopen(url)               
html = f.read()
        
#parser.createMatchInDB(html,equipe)
pattern = '<a class="menu" href="(.*?)" target="_parent">(.*?)</a>'


result = re.findall(pattern , html)

for a in result[:]:
    (url, cat) = a
    if (cat.find("BRASSAGE") == -1):
        print " %s => %s" %(cat, retrieveCorrectUrl(cat,url))

