'''
Created on 27 sept. 2015

@author: Pascal
'''
import operator
import datetime
import collections


from spcocModel import Equipe

from google.appengine.ext.db import Key
from google.appengine.ext import ndb
from gettext import Catalog

JOUR_DE_LA_SEMAINE = ("Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche")

 

matchesURL = { 
			   "SF"   : "http://resultats.ffbb.com/championnat/equipe/division/b5e6211e37bfb5e6211ef46527b5.html" ,
			   "SM 1" : "http://resultats.ffbb.com/championnat/equipe/division/b5e6211e38bab5e6211ef62f27b5.html" ,
			   "SM 2" : "http://resultats.ffbb.com/championnat/equipe/division/b5e6211e42adb5e6211f0c7f27b5.html" ,
			   
			   
			   
               "U17" : "http://resultats.ffbb.com/championnat/equipe/division/b5e6211e4d4fb5e6211f1d8227b5.html" ,
               
               "U15 M1" : "http://resultats.ffbb.com/championnat/equipe/division/b5e6211e4d78b5e6211f1e4b27b5.html" ,
               "U15 M2" : "http://resultats.ffbb.com/championnat/equipe/division/b5e6211e4d84b5e6211f1ea727b5.html" ,
               "U15 F" : "http://resultats.ffbb.com/championnat/equipe/division/b5e6211e4c67b5e6211f1bb227b5.html" ,
                              
               "U13 M" : "http://resultats.ffbb.com/championnat/equipe/division/b5e6211e4d83b5e6211f1ea627b5.html" ,
               
               "U11" : "http://resultats.ffbb.com/championnat/equipe/division/b5e6211e4d8ab5e6211f1eaf27b5.html" 			   
			   
			   
#               "U17" : "http://resultats.ffbb.com/championnat/equipe/division/b5e6211e41b3b5e6211f09d727b5.html" ,
               
#               "U15 M1" : "http://resultats.ffbb.com/championnat/equipe/division/b5e6211e41a3b5e6211f09af27b5.html" ,
#               "U15 M2" : "http://resultats.ffbb.com/championnat/equipe/division/b5e6211e41a7b5e6211f09b827b5.html" ,
#               "U15 F" : "http://resultats.ffbb.com/championnat/equipe/division/b5e6211e42d0b5e6211f0cb827b5.html" ,
                              
#               "U13 M" : "http://resultats.ffbb.com/championnat/equipe/division/b5e6211e41aeb5e6211f09c327b5.html" ,
               
#               "U11" : "http://resultats.ffbb.com/championnat/equipe/division/b5e6211e434fb5e6211f0d6127b5.html" 
                
               }



#               "SM 2" : "http://resultats.ffbb.com/championnat/equipe/division/b5e6211e0e61b5e6211eb7cf27b5.html" ,
#               "SF"   : "http://resultats.ffbb.com/championnat/equipe/division/b5e6211e0f9eb5e6211ebb7627b5.html" ,
               
#              "U17 M"   : "http://resultats.ffbb.com/championnat/equipe/division/b5e6211e1a60b5e6211ecea927b5.html" ,
#               "U17 F"   : "http://resultats.ffbb.com/championnat/equipe/division/b5e6211e19a7b5e6211eccd527b5.html" ,
#               "U15"   : "http://resultats.ffbb.com/championnat/equipe/division/b5e6211e1a67b5e6211eceb027b5.html" ,
#               "U13 M1"   : "http://resultats.ffbb.com/championnat/equipe/division/b5e6211e1a6cb5e6211eceb827b5.html" ,
#               "U13 M2"   : "http://resultats.ffbb.com/championnat/equipe/division/b5e6211e1a9fb5e6211ecefe27b5.html" ,
#               "U13 F"   : "http://resultats.ffbb.com/championnat/equipe/division/b5e6211e19b0b5e6211ecce327b5.html" ,               
#               "U11 1"   : "http://resultats.ffbb.com/championnat/equipe/division/b5e6211e1aa2b5e6211ecf0327b5.html" ,
#               "U11 2"   : "http://resultats.ffbb.com/championnat/equipe/division/b5e6211e1aa3b5e6211ecf0527b5.html" ,               
               
#              "U17 M - old"   : "http://resultats.ffbb.com/championnat/equipe/division/b5e6211e0e5fb5e6211eb7cc27b5.html" ,
#               "U17 F - old"   : "http://resultats.ffbb.com/championnat/equipe/division/b5e6211e0ef2b5e6211eb97727b5.html" ,
#               "U15 - old"   : "http://resultats.ffbb.com/championnat/equipe/division/b5e6211e0ee1b5e6211eb95527b5.html" ,
#               "U13 M1 - old"   : "http://resultats.ffbb.com/championnat/equipe/division/b5e6211e0ee8b5e6211eb96827b5.html" ,
#               "U13 M2 - old"   : "http://resultats.ffbb.com/championnat/equipe/division/b5e6211e0ee9b5e6211eb96a27b5.html" ,
#               "U13 F - old"   : "http://resultats.ffbb.com/championnat/equipe/division/b5e6211e1340b5e6211ec27527b5.html" ,               
#               "U11 1 - old"   : "http://resultats.ffbb.com/championnat/equipe/division/b5e6211e0eebb5e6211eb96d27b5.html" ,
#               "U11 2 - old"   : "http://resultats.ffbb.com/championnat/equipe/division/b5e6211e0eecb5e6211eb96f27b5.html" ,                                          
#              }

STRING_LOCAL = ["SAINT PAUL LA COLLE OLYMPIQUE CB", "EN - SAINT PAUL LA COLLE OLYMPIQUE CB"]

ABREV = "SPCOC"

# 0 : Pas de vainqueur
# 1 : Domicile  
# 2 : Visiteur
def findVainqueur(score):
    vainqueur = 0
    index = score.index('-')

    if (index > 0):
        score1S = score[:index-1]
        score2S = score[index+2:]
        
        if (int(score1S) > (int(score2S))):
           vainqueur = 1
        else :
           vainqueur = 2
    return vainqueur


def score(score):
    print score
    score1S = -1;    
    score2S = -1;
    index = score.index('-')

    if (index > 0):
        score1S = score[:index-1]
        score2S = score[index+2:]
    print score1S
    print score2S
    return int(score1S) , int(score2S)


class MatchGueriniere(ndb.Model):
    category = ndb.StringProperty()
    journee = ndb.StringProperty()
    
    
class Match(ndb.Model):

    category = ndb.StringProperty()
    journee = ndb.StringProperty()
    date = ndb.DateProperty()        
    locaux = ndb.StringProperty()
    visiteur = ndb.StringProperty()
    isDomicile = ndb.BooleanProperty()
    fullDate = ndb.DateTimeProperty()
    
    arbitre =  ndb.StringProperty()
    score =  ndb.StringProperty()
    plan = ndb.StringProperty()
    
    vainqueur = ndb.IntegerProperty() 
    
    gueriniere = False




def initEquipe():
    
    ndb.delete_multi(Equipe.query().fetch(keys_only=True))
    for key in matchesURL.keys():
        e = Equipe()
        e.nom = key
        e.url = matchesURL[key]
        e.put()
        
    
def addMatchInDB(category, data, referee,plan):
              
    m = Match()
    m.category = category
    m.journee = data[0]
    m.fullDate = datetime.datetime.strptime(data[1] +" " + data[2], "%d/%m/%Y %H:%M")
    m.locaux = data[3]
    m.visiteur = data[4]
    m.isDomicile = (data[3] in STRING_LOCAL)
    m.date = datetime.datetime.strptime(data[1], "%d/%m/%Y")
    m.score = data[5]
    m.arbitre = referee
    m.plan = "http://resultats.ffbb.com/here/here_popup.php?id=" + plan[21:-2]
    m.vainqueur = findVainqueur(data[5])
    m.put()    
    
from HTMLParser import HTMLParser

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    
    def __init__ (self):
        HTMLParser.__init__(self)
        self.encours = False
        self.data = []
        self.referee = None
        
        self.nextIsReferee = False
        self.dataReferee = False
        
        self.matches = []
        self.category = None
        
        self.plan = None
    
    def handle_starttag(self, tag, attrs):        
        if (tag == 'tr') :
            displayNone = False
            # and 'class' in attrs and (attrs['class'] == "altern-2" or attrs['class'] == "no-altern-2") ) :
            for a in attrs :               
                if  a[0] == "class" and ( a[1] == "altern-2" or a[1] == "no-altern-2"):                      
                    self.encours = True
                    
                #if  a[0] == "style" and ( a[1] == "display:none"):
                #    displayNone = True
                            
                if  a[0] == "id" and ( a[1][0:5] == "trOff"):                    
                    self.nextIsReferee = True
                    
                if  a[0] == "class" and ( a[1][0:3] == "tit"):                    
                    self.encours = False
                
            #if (displayNone) : # Hack for the referee
            #    self.encours = False
                
        if (tag == 'td' and self.nextIsReferee) :
            for a in attrs :
                if  a[0] == "class" and ( a[1] == "infos_complementaires"):                      
                    self.dataReferee = True
                    
        if (self.encours):
            if (tag == 'a') :
                for a in attrs :
                    if  (a[0] == "href"):                      
                        self.plan = a[1]
                    
    def handle_endtag(self, tag):        
        if (tag == 'tr' and self.nextIsReferee):                             
            if (len(self.data)> 0):                                   
                if (self.category):                    
                    addMatchInDB(self.category, self.data, self.referee, self.plan)
                    
            self.data = []
            self.referee = None
            self.dataReferee  = False
            self.nextIsReferee = False
            self.plan = None
        
#        if (self.encours and tag == 'tr' ):
#            nextIsReferee = False
#            self.referee = None
            
    def handle_data(self, data):
        if (self.encours):
            self.data.append(data)
        if (self.dataReferee):            
            self.referee = data
        
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
def returnComingMatch(date = datetime.datetime.now(),  end =  7 ):
    
    query = Match.query(ndb.AND(Match.fullDate >= date),
            Match.fullDate < date + datetime.timedelta(days=end)).order(Match.fullDate)
    
    return query.fetch()

# Return list of match from date to date + end
def returnPreviousMatch(date = datetime.datetime.now(),  beginning =  7 ):
    
    #query = Match.query(ndb.AND(Match.fullDate <= date),
    #        Match.fullDate > date + datetime.timedelta(days=beginning*-1)).order(Match.fullDate)
            
    query = Match.query(Match.fullDate <= date).order(-Match.fullDate)
    
    return query.fetch(10)


def returnAllMatches(date = datetime.datetime.now()):    
    query = Match.query(Match.fullDate >= date).order(-Match.fullDate)    
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
    

def removeExempt(list):
	newList = []
	for a in list :
		if (a.visiteur != 'Exempt' and a.locaux != 'Exempt'):
			newList.append(a)
	return newList


def matchDeLaSemaine(matchesURL = matchesURL):

    
    journee = {}
    
    filteredReturnComingMatch = removeExempt(returnComingMatch()) 

    for m in filteredReturnComingMatch :
        m = updateGueriniere(m)
        if journee.has_key(m.date) :
            domicile , gueriniere, exterieur = journee[m.date]
        else :
            domicile = []
            exterieur = []
            gueriniere = []
        
        if m.isDomicile and not m.gueriniere:
            domicile.append(m)
        elif m.isDomicile and m.gueriniere :
            gueriniere.append(m)
        else :
            exterieur.append(m)
        journee[m.date] = ( domicile , gueriniere, exterieur )
            
     
    #return journee
    return collections.OrderedDict(sorted(journee.items())) 


def LastResult(matchesURL = matchesURL):

    
    journee = {}
    

    for m in returnPreviousMatch() :
        if journee.has_key(m.date) :
            matches = journee[m.date]
        else :
            matches = []        
        if (m.score != "-"):    
            matches.append(m)        
            journee[m.date] = ( matches )
            
     
    
    return collections.OrderedDict(sorted(journee.items(), reverse=True)) 

def AllMatchesAtHome(matchesURL = matchesURL):

    
    journee = {}
    

    for m in returnAllMatches() :
        
        m = updateGueriniere(m)
        
        if journee.has_key(m.date) :
            matches = journee[m.date]
        else :
            matches = []
        
        if (m.isDomicile) :
            matches.append(m)        
            journee[m.date] = ( matches )
            
     
    
    return collections.OrderedDict(sorted(journee.items())) 


def addAllMatchInDB():
    for equipe in matchesURL :
        parser = MyHTMLParser()
        f = urllib.urlopen(matchesURL[equipe])               
        html = f.readline()
        parser.listOfMatches2(html,equipe)
        f.close()
        parser.close()


def deleteEquipe(equipe):
    print "done"
    #query = Equipe.query(Equipe.nom = equipe)
    #equipes = query.fetch()
    #for e in equipes :
    #    e.key.delete()
    
    #Key(equipe).delete()
    
def addEquipe():
    e = Equipe()
    e.nom = "Nom"
    e.url = "URL FFBB"
    e.put()
    

def cleanDB():
    ndb.delete_multi(Match.query().fetch(keys_only=True))
    
    
def replaceSPCOCDomExt(journees):
    
    for k in journees.keys():
        dom,gue, ext = journees[k]
        
        for m in dom :
            
            if (m.locaux in STRING_LOCAL):
                m.locaux = ABREV + " " + m.category
            if (m.visiteur in STRING_LOCAL):
                m.visiteur = ABREV + " " + m.category
        
        for m in gue :
            
            if (m.locaux in STRING_LOCAL):
                m.locaux = ABREV + " " + m.category
            if (m.visiteur in STRING_LOCAL):
                m.visiteur = ABREV + " " + m.category
        
                
        for m in ext :
            
            if (m.locaux in STRING_LOCAL):
                m.locaux = ABREV + " " + m.category
            if (m.visiteur in STRING_LOCAL):
                m.visiteur = ABREV + " " + m.category
                
    return journees
    
    
def replaceSPCOC(journees):
    
    for k in journees.keys():
        matches = journees[k]
        for m in matches :
            
            if (m.locaux in STRING_LOCAL):
                m.locaux = ABREV + " " + m.category
            if (m.visiteur in STRING_LOCAL):
                m.visiteur = ABREV + " " + m.category
                  
    return journees



def update(gueriniere, cat, journee):
    
    if (gueriniere == "1"):
        m = MatchGueriniere()
        m.category = cat
        m.journee = journee        
        m.put()
    else :
    
        matches = findMatchGueriniere(cat, journee)
        for m in matches :
            m.key.delete()

def findMatchGueriniere(cat, journee):
    query = MatchGueriniere.query(ndb.AND(MatchGueriniere.journee == journee,
                                          MatchGueriniere.category == cat))
    
    matches = query.fetch()
    return matches


def equipes():
    query = Equipe.query()
    equipes = query.fetch()
    return equipes


def isGueriniere(cat, journee):    
    return len(findMatchGueriniere(cat, journee)) == 1
                   
                   
def updateGueriniere(m):    
    if isGueriniere(m.category, m.journee):
        print "OKKKKK"
        print m.category
        print m.journee
        m.gueriniere = True
    return m
                       
#display( matchDeLaSemaine())

def stats():
    result = ""
    cat = {}
    
    date = datetime.datetime.now()
    query = Match.query(Match.fullDate < date ).order(Match.fullDate)
    
    m = query.fetch()
    sV = -1
    sL = -1
    match = 0
    laColle = 0
    other = 0
    for mm in m :
        sV = -1
        sL = -1
        
        if (mm.isDomicile) :
            sL, sV = score(mm.score)
        else : 
            sV, sL = score(mm.score)
            
        if (sL != -1):
            print mm
            laColle += sL
            other += sV
            match += 1
            print match
            print laColle
            print other
            
    return " Match " + str(match) + " La colle " + str(laColle) + " - " + str(other)
