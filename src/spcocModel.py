from google.appengine.ext import ndb


# Describe a equipe and the URL used to found information 
class Equipe(ndb.Model):
    
    nom = ndb.StringProperty()
    url = ndb.StringProperty()

