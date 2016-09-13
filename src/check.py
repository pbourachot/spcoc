from google.appengine.api import mail
from google.appengine.ext import ndb
import urlparse
import httplib


class Receiver(ndb.Model):
    adress = ndb.StringProperty()
    

class Website(ndb.Model):
    url = ndb.StringProperty()



def init():
    m = Receiver()
    m.adress = 'pascal.bourachot@gmail.com'  
    m.put()    
    
    m = Receiver()
    m.adress = 'jacoutot@gmail.com'  
    m.put()
    
    m = Website()
    m.url = 'http://www.scaline.fr'  
    m.put()
    
    m = Website()
    m.url = 'http://lpst.celservice.fr'  
    m.put()
    
    m = Website()
    m.url = 'http://todayresto.com'  
    m.put()
    

def check():
    #init()
    websites = Website.query().fetch()
    statusUrl = checkUrls(websites)

    for m in Receiver.query().fetch():    
        sendMail(statusUrl, m.adress)
        
def siteAvailable(url):

    try :    
        conn = httplib.HTTPConnection(url)
        conn.request("HEAD", "/")
        r1 = conn.getresponse()
        if (r1.status in [200,301]) :
            return 1
        else :        
            return 0
    except :
        return 0
            
        
def checkUrls(urls):    
    result = {}
    
    for u in urls :        
        if (siteAvailable(u.url)):
            result[u.url] = 1
        else :
            result[u.url] = 0
    return result

    
    
    
def sendMail(status, m):
    user_address = m
    sender_address = "Example.com Support <support@example.com>"
    subject = "Website Status"
    body = "Status of following site \n"
    send = False 
    
    for s in status.keys():
        body += " %s = %s" %( s, status[s])
        if (status[s] == 0):
            send = True

    if (send):
        mail.send_mail('pbourachot@gmail.com', user_address, subject, body)