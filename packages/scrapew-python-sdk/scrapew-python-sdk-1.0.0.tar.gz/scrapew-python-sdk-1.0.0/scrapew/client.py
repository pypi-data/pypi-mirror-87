import requests
import furl

class ScrapewAPIClient(object):

    def __init__(self, apikey):
        self.apikey = apikey
        self.api = 'https://api.scrapew.com/request'

    def get(self, url, render, template_id):
        
        f =  furl.furl(self.api)  
        f.args = {"url": url, "render":render, "apikey":self.apikey, "template_id": template_id}
        print(f.url)
        return requests.get(f.url, headers={"accept": "application/json"})


    