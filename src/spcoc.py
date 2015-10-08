'''
Created on 27 sept. 2015

@author: Pascal
'''
import operator
import datetime
import collections

from google.appengine.ext import ndb

JOUR_DE_LA_SEMAINE = ("Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche")
 

matchesURL = {"Senior M 1" : "http://resultats.ffbb.com/championnat/equipe/division/b5e6211e0979b5e6211eae1127b5.html" ,
              
               "Senior M 2" : "http://resultats.ffbb.com/championnat/equipe/division/b5e6211e0e61b5e6211eb7cf27b5.html" ,
               "Senior F"   : "http://resultats.ffbb.com/championnat/equipe/division/b5e6211e0f9eb5e6211ebb7627b5.html" ,
                            
                            
               "U17 M"   : "http://resultats.ffbb.com/championnat/equipe/division/b5e6211e0e5fb5e6211eb7cc27b5.html" ,
               "U17 F"   : "http://resultats.ffbb.com/championnat/equipe/division/b5e6211e0ef2b5e6211eb97727b5.html" ,
               "U15"   : "http://resultats.ffbb.com/championnat/equipe/division/b5e6211e0ee1b5e6211eb95527b5.html" ,
               "U13 M1"   : "http://resultats.ffbb.com/championnat/equipe/division/b5e6211e0ee8b5e6211eb96827b5.html" ,
               "U13 M2"   : "http://resultats.ffbb.com/championnat/equipe/division/b5e6211e0ee9b5e6211eb96a27b5.html" ,
               "U11 1"   : "http://resultats.ffbb.com/championnat/equipe/division/b5e6211e0eebb5e6211eb96d27b5.html" ,
               "U11 2"   : "http://resultats.ffbb.com/championnat/equipe/division/b5e6211e0eecb5e6211eb96f27b5.html" ,
                                          
              }

STRING_LOCAL = ["SAINT PAUL LA COLLE OLYMPIQUE CB", "EN - SAINT PAUL LA COLLE OLYMPIQUE CB"]



    
class Match(ndb.Model):

    category = ndb.StringProperty()
    journee = ndb.StringProperty()
    date = ndb.DateProperty()    
    #time = ndb.TimeProperty()
    locaux = ndb.StringProperty()
    visiteur = ndb.StringProperty()
    isDomicile = ndb.BooleanProperty()
    fullDate = ndb.DateTimeProperty() 

            
    
def addMatchInDB(category, data):           
    m = Match()
    m.category = category
    m.journee = data[0]
    m.fullDate = datetime.datetime.strptime(data[1] +" " + data[2], "%d/%m/%Y %H:%M")
    m.locaux = data[3]
    m.visiteur = data[4]
    m.isDomicile = (data[3] in STRING_LOCAL)
    m.date = datetime.datetime.strptime(data[1], "%d/%m/%Y")
    #print data[2]
    #m.time =  time.mktime(datetime.datetime.strptime(data[1] +" " + data[2], "%d/%m/%Y %H:%M").timetuple()) #time.strptime(data[2], "%H:%M")
    m.put()    
    
from HTMLParser import HTMLParser

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    
    def __init__ (self):
        HTMLParser.__init__(self)
        self.encours = False
        self.data = []
        self.matches = []
        self.category = None
    
    def handle_starttag(self, tag, attrs):        
        if (tag == 'tr') :
            displayNone = False
            # and 'class' in attrs and (attrs['class'] == "altern-2" or attrs['class'] == "no-altern-2") ) :
            for a in attrs :               
                if  a[0] == "class" and ( a[1] == "altern-2" or a[1] == "no-altern-2"):                      
                    self.encours = True
                    
                if  a[0] == "style" and ( a[1] == "display:none"):
                    displayNone = True
            
            if (displayNone) : # Hack for the referee
                self.encours = False
                    
    def handle_endtag(self, tag):        
        if (self.encours and tag == 'tr' ):
            self.encours = False                 
            if (len(self.data)> 0):                                   
                if (self.category):                
                    addMatchInDB(self.category, self.data)
                    
            self.data = []
            
    def handle_data(self, data):
        if (self.encours):
            self.data.append(data)
        
    def listOfMatches(self, html):
        
        self.feed(html)
        return self.matches[:]
    
    def listOfMatches2(self, html, category):
        self.category = category
        self.feed(html)
        
        


import urllib

def matchesFromDate(date, matches):
    resultDomicile = []
    resultExterieur = []
    for category in matches :                
        for m in matches[category] :
            if m.dt.timetuple()[7] == date.timetuple()[7]: 
                if (m.isDomicile) :                               
                    resultDomicile.append((category, m.heure, m))
                else :
                    resultExterieur.append((category, m.heure, m))
    return resultDomicile, resultExterieur




# Return list of match from date to date + end
def returnWeekMatch(date = datetime.datetime.now(),  end =  7 ):
    
    query = Match.query(ndb.AND(Match.fullDate >= date),
            Match.fullDate < date + datetime.timedelta(days=end)).order(Match.fullDate)
    
    return query.fetch()

        
def display(result):
    output = ""
    for (day,matchDomiciles, matchExterieurs ) in result:        
            
        if matchDomiciles  or matchExterieurs:
            output += "=========\n"            
            output += JOUR_DE_LA_SEMAINE[day.weekday()] + "  "  + day.__str__() + "\n"
            output += "=========\n"
            if (matchDomiciles):
                matchDomiciles = sorted(matchDomiciles, key=operator.itemgetter(1))
                output += "== A Domicile ==" + "\n"
                for matchTuple in matchDomiciles :
                    output += matchTuple[0]  + "\n"
                    output += matchTuple[2].__str__() + "\n"
                    
            if (matchExterieurs):
                matchExterieurs = sorted(matchExterieurs, key=operator.itemgetter(1))
                output += "== A l'exterieur ==" + "\n"
                for matchTuple in matchExterieurs :
                    output += matchTuple[0]  + "\n"
                    output += matchTuple[2].__str__() + "\n"
                    
    print output                
    return output
    

def matchDeLaSemaine(matchesURL = matchesURL):

    
    journee = {}
    

    for m in returnWeekMatch() :
        if journee.has_key(m.date) :
            domicile , exterieur = journee[m.date]
        else :
            domicile = []
            exterieur = []
        
        if m.isDomicile :
            domicile.append(m)
        else :
            exterieur.append(m)
        journee[m.date] = ( domicile , exterieur )
            
     
    #return journee
    return collections.OrderedDict(sorted(journee.items())) 


def addAllMatchInDB():
    for equipe in matchesURL :
        parser = MyHTMLParser()
        f = urllib.urlopen(matchesURL[equipe])               
        html = f.readline()
        parser.listOfMatches2(html,equipe)
        f.close()
        parser.close()

def cleanDB():
    ndb.delete_multi(Match.query().fetch(keys_only=True))    
#display( matchDeLaSemaine())
