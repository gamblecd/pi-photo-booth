import facebook
import urllib
import subprocess
import urlparse

FACEBOOK_PROFILE_ID = ""
FACEBOOK_ACCESS_TOKEN = ""
class FacebookUploader:

    def login(self):
        print("Connecting to Facebook")
        oauth_args = dict(client_id     = FACEBOOK_APP_ID,
                        client_secret = FACEBOOK_APP_SECRET,
                        grant_type    = 'client_credentials')
        oauth_curl_cmd = ['curl',
                        'https://graph.facebook.com/oauth/access_token?' + urllib.urlencode(oauth_args)]

        oauth_response = subprocess.Popen(oauth_curl_cmd,
                                        stdout = subprocess.PIPE,
                                        stderr = subprocess.PIPE).communicate()[0]
        try:
            print("Logging in")

            oauth_access_token = urlparse.parse_qs(str(oauth_response))['access_token'][0]
        except KeyError:
            print('Unable to grab an access token!')
            exit()
        print ("Successfully Logged in")
        return oauth_access_token

    def __init__(self):
        print("Initializing Uploader")
        self.events = None
       #self.token = self.login()
        self.graph = facebook.GraphAPI(FACEBOOK_ACCESS_TOKEN)
        print("Connected to Facebook")


    def getEvents(self):
        if self.events is None:
            self.events = self.graph.get_object("me/events", fields="name")
        return self.events

    def findEvent(self, eventName):
        events = self.getEvents();
        for x in events.get("data"):
            if eventName in x.get("name"):
                print("{} : {}".format(eventName, x.get("id")))
                return x.get("id")
        return None;
    
    def uploadToEvent(self, imageName, id):
        ret = self.graph.put_photo(image=open(imageName, 'rb'), album_path=id + "/photos")
        return ret
    