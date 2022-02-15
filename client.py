import requests
from timeit import default_timer as timer
from datetime import timedelta


class Spider:
    """
    requests the server for the site map and revert a valid response. 
    """
    def __init__(self, base_url):
        self.base_url =  base_url
    
    def crawlIt(self):
        url = "http://127.0.0.1:8080/crawler/"
        my_json = {"base_url": self.base_url, "depth": 2}
        response = requests.post(url=url, data=my_json, verify=False)
        return response

if __name__ == '__main__':
    """
    short script to query server
    """
    start = timer()
    print("This should not take more than 120 seconds or 2 minutes to get the site map")
    print("fetching links....")
    # querying server
    inst = Spider("https://yahoo.com")
    text = inst.crawlIt()
    if text.status_code != 200 or text.status_code != 201:
        print("Could not fetch the site map, got some errors :( \n")
        print("RESPONSE CODE: ", text.status_code)
    print(text.text.replace('\\n', '\n'))
    end = timer()
    # prints performance...
    print("\n###Time taken: {0} seconds to scrape {1} valid links: ".format(timedelta(seconds=end-start).total_seconds(), text.text.count("http")))
