import webapp2

import spcoc
import os
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)  


class MainPage(webapp2.RequestHandler):
    
    def get(self):
        
        journees = spcoc.matchDeLaSemaine()
        template_values = {
            'data': journees,            
        }
        
        template = JINJA_ENVIRONMENT.get_template('index.html')        
        self.response.write(template.render(template_values))
        
class DeletePage(webapp2.RequestHandler):
    
    def get(self):        
        journees = spcoc.cleanDB()
        self.response.out.write("Delete Done.")


class InitPage(webapp2.RequestHandler):
    
    def get(self):        
        journees = spcoc.addAllMatchInDB()
        self.response.out.write("Init matches Done.")


app = webapp2.WSGIApplication([('/', MainPage), ('/delete', DeletePage), ('/init', InitPage)], debug=True)



