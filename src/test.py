print "This is a test with gitHub."
import sys, os
sys.path.append('/usr/local/share/google/google-cloud-sdk/platform/google_appengine/lib/yaml/lib')
sys.path.append('/usr/local/share/google/google-cloud-sdk/platform/google_appengine/')
import spcoc
os.environ['APPLICATION_ID'] = 'myapp'


datastore_file = 'mydatestore'
from google.appengine.api import apiproxy_stub_map,datastore_file_stub
apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap() 
stub = datastore_file_stub.DatastoreFileStub('myapp', datastore_file, '/')
apiproxy_stub_map.apiproxy.RegisterStub('datastore_v3', stub)
'''

apiproxy_stub_map.apiproxy.RegisterStub('memcache', stubMemCache)
'''

#journees = spcoc.cleanDB()        
#journees = spcoc.addAllMatchInDB()

#journees = spcoc.matchDeLaSemaine()

print spcoc.LastResult()