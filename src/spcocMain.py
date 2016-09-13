import webapp2

import spcoc
import os
import jinja2
import check

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)  


class MainPage(webapp2.RequestHandler):
    
    def get(self):
                
        template_values = {}
        template = JINJA_ENVIRONMENT.get_template('index.html')        
        self.response.write(template.render(template_values))
        
        
class NextPage(webapp2.RequestHandler):
    
    def get(self):
        
        journees = spcoc.matchDeLaSemaine()
        journees = spcoc.replaceSPCOCDomExt(journees)
        
        template_values = {
            'data': journees,            
        }
        
        template = JINJA_ENVIRONMENT.get_template('next.html')        
        self.response.write(template.render(template_values))
        
        
class LastPage(webapp2.RequestHandler):
    
    def get(self):
        
        journees = spcoc.LastResult()
        
        journees = spcoc.replaceSPCOC(journees)
        template_values = {
            'data': journees,            
        }
        
        template = JINJA_ENVIRONMENT.get_template('last_NEW.html')        
        self.response.write(template.render(template_values))


class AdminPage(webapp2.RequestHandler):
    
    def get(self):
        
        journees = spcoc.AllMatchesAtHome()
        
        journees = spcoc.replaceSPCOC(journees)
        template_values = {
            'data': journees,            
        }
        
        template = JINJA_ENVIRONMENT.get_template('admin.html')        
        self.response.write(template.render(template_values))

        
class DeletePage(webapp2.RequestHandler):
    
    def get(self):        
        journees = spcoc.cleanDB()
        self.response.out.write("Delete Done")


class InitPage(webapp2.RequestHandler):
    
    def get(self):
        journees = spcoc.cleanDB()        
        journees = spcoc.addAllMatchInDB()
        self.redirect("/")
        #self.response.out.write("Init matches Done.")
        
class UpdatePage(webapp2.RequestHandler):
    
    def get(self):
        #journees = spcoc.cleanDB()        
        #journees = spcoc.addAllMatchInDB()
        
        gueriniere = self.request.get("gueriniere")
        cat = self.request.get("category")
        journee = self.request.get("journee")
        
        spcoc.update(gueriniere, cat, journee)
        
        self.redirect("/admin")
        #self.response.out.write("Init matches Done.")        
        
        
class StatsPage(webapp2.RequestHandler):
    
    def get(self):
        #journees = spcoc.cleanDB()        
        #journees = spcoc.addAllMatchInDB()
        
       
        
         self.response.write(spcoc.stats())
        
        
        #self.response.out.write("Init matches Done.")
        
        
class Check(webapp2.RequestHandler):
    
    def get(self):
        check.check()
        self.response.write("done")
        
                        
        
class TestPage(webapp2.RequestHandler):
    
    def get(self):        
        journees = spcoc.addAllMatchInDB()
        self.response.out.write("Init matches Done.")


app = webapp2.WSGIApplication([('/', MainPage),
                               ('/delete', DeletePage),
                               ('/init', InitPage),
                               ('/next', NextPage),
                               ('/dernierResultat', LastPage),
                               ('/admin', AdminPage),
                               ('/update', UpdatePage),
                               ('/stats', StatsPage),
                               ('/check', Check) ]
                              , debug=True)



