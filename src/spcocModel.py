from google.appengine.ext import ndb

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


def addMatchInDB(category, data):           
    m = Match()
    m.category = category
    m.journee = data[0]
    m.fullDate = datetime.datetime.strptime(data[1] +" " + data[2], "%d/%m/%Y %H:%M")
    m.locaux = data[3]
    m.visiteur = data[4]
    m.isDomicile = (data[3] in STRING_LOCAL)
    m.date = datetime.datetime.strptime(data[1], "%d/%m/%Y")
    m.put()