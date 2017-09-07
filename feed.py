from FeedlyClient import *

FEEDLY_REDIRECT_URI = "http://fabreadly.com/auth_callback"
FEEDLY_CLIENT_ID="client_id"
FEEDLY_CLIENT_SECRET="client_secret"


userId = "4a4c8ba5-f80e-4d43-b998-6cc07e8a8362"
token = "AyyijrCwAt6iYxnTHgATYF9deZk3gNQ2DLlw3iDd3JebBfZMRKPw9BqQoXdulPwYT1x3HaiUmh2IWUi8g4biNVzWvmiqdwL19PSTsxMx2ucDaDzXQ_0xDP7ZaHBOEwAqvuOtwIWCSBT4UwYOilA8bzPemGTr9mCbS_DI2a14cic74JO5U6LO9yBPeqbyJBWxcbpGKXeR4Q8NqysMhgDUTRLUW6ey:feedlydev"


headers = {'Authorization': 'OAuth '+ token}

def get_feedly_client(token=None):
        if token:
                return FeedlyClient(token=token, sandbox=True)
        else:
                return FeedlyClient(
                                                        client_id=FEEDLY_CLIENT_ID,
                                                        client_secret=FEEDLY_CLIENT_SECRET,
                                                        sandbox=True
                )
def auth(request):
        feedly = get_feedly_client()
        # Redirect the user to the feedly authorization URL to get user code
        code_url = feedly.get_code_url(FEEDLY_REDIRECT_URI)
        return redirect(code_url)





f = FeedlyClient(userId, token )
#print f

def getEndPoint(path):
        url = "https://cloud.feedly.com" 
        if path is not None:
            url += "/%s" % path
        return url
        

def getUserSubscriptions():
        quest_url=getEndPoint('v3/subscriptions')
        res = requests.get(url=quest_url, headers=headers)
        return res.json()


def getStreams(id , saved = False):
        if (saved):
                quest_url=getEndPoint("v3/streams/ids")
        else :
                quest_url=getEndPoint("v3/streams/ids")
        unreadOnly = True
        params = dict(
                      streamId=id,
                      #streamId="/tag/global.saved",
                      unreadOnly=unreadOnly
                      )
        #res = requests.get(url=quest_url, headers=headers)
        #print "id => " + id
        res = requests.get(url=quest_url, params=params,headers=headers)
        return res.json()


def saveItems():
        print "== Save Items with user"
        quest_url=getEndPoint("v3/streams/ids?streamId=user/" + userId + "/tag/global.saved&count=8000")
        
        print quest_url
        #http://cloud.feedly.com/v3/streams/contents?streamId=user/240f594d-ee80-4f07-8437-XXXXXXXX/tag/global.saved&count=10
        #/ids?streamId=user/<my user id>/tag/global.saved
        params = dict()
        res = requests.get(url=quest_url, params=params,headers=headers)
        return res.json()


def saveItems0(feedId):
        print "== Stream Only"
        quest_url=getEndPoint("v3/streams/ids?streamId=" + feedId )
        
        print quest_url
        #http://cloud.feedly.com/v3/streams/contents?streamId=user/240f594d-ee80-4f07-8437-XXXXXXXX/tag/global.saved&count=10
        #/ids?streamId=user/<my user id>/tag/global.saved
        params = dict()
        res = requests.get(url=quest_url, params=params,headers=headers)
        return res.json()

def saveItems(feedId):
        print "== Save Items with user"
        quest_url=getEndPoint("v3/streams/ids?streamId=" + feedId + "/tag/global.saved&count=8000")
        print quest_url
        #http://cloud.feedly.com/v3/streams/contents?streamId=user/240f594d-ee80-4f07-8437-XXXXXXXX/tag/global.saved&count=10
        #/ids?streamId=user/<my user id>/tag/global.saved
        params = dict()
        res = requests.get(url=quest_url, params=params,headers=headers)
        return res.json()


def unreadList(subs):
        total = 0
        for feed in subs:
                total += unreadListPartial(feed)
        print " Total : %s" %total
                

def KOunreadListPartial(feed):
        
        id = feed["id"]
        entries = getStreams(id)
        ids = entries['ids']
        if len(ids) > 0:
#                print " %s => %s " %(id, len(ids))
                return len(ids)
        return 0



def unreadListPartial(feed, saved = False):
        
        id = feed["id"]
        entries = getStreams(id , saved )
        print entries
        ids = entries['ids']
        if len(ids) > 0:
#                print " %s => %s " %(id, len(ids))
                return len(ids)
        return 0
        

#subs =  f.get_user_subscriptions(token)
subs = getUserSubscriptions()
print subs[0]
print "Nb of subscription " + str(len(subs))

#print subs[0]['website']
"""
for a in subs[0].keys():
        print a + "=> " + str(subs[0][a])
"""        

unreadList(subs)

##unreadListPartial(subs[0])
##unreadListPartial(subs[0], True)
#itemsSave = saveItems()["ids"]
itemsSave = saveItems0(subs[0]["id"])["ids"]
"""
print " Length of save items (saveItems0)  => %s " %( len(itemsSave))


itemsSave = saveItems(subs[0]["id"])["ids"]
print " Length of save items  => %s " %( len(itemsSave))


#print getStreams(subs[0]["id"])

#for a in subs :
#        print a

#print f.get_article_unread(token)
"""

print "Test Feedly"
