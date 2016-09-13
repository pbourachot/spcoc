from google.appengine.ext import ndb


# Describe an equipe and the URL used to found information 
class Equipe(ndb.Model):
    
    nom = ndb.StringProperty()
    url = ndb.StringProperty()

