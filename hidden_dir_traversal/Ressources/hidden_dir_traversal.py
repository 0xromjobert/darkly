import sys
import requests
from bs4 import BeautifulSoup

ip = 'http://10.11.249.211/'
url = ip + '.hidden/'
count = 0

def req_url(url):
    '''
    traverse an url and look for emmbedded link in the html tree
    '''
    res = requests.get(url)
    html_tree = BeautifulSoup(res.text, 'html.parser')
    dir_list = list()
    for link in html_tree.find_all('a'):
        addr = link.get('href')
        if addr and addr != "../" :
            dir_list.append(addr)
    return dir_list

def traverse_url(url, dir_list, result, flag):
    if dir_list is None or (len(dir_list) == 0 ):
        return
    if flag and len(flag) > 0:
        return
    for link in dir_list:
        new_url = url + link
        sub_dir = req_url(new_url)
        
        if (link.strip().upper() == 'README' or len(sub_dir) == 0):
            result.append(new_url)
            sys.stdout.write(f"\rfound endpoint - total is now:{len(result)} - link is: {new_url}")
            sys.stdout.flush()
            ret = is_flag(new_url)
            if ret:
                print("\n\n flag FOUND !!\n\n")
                flag.append(ret)
                return  # **Stop searching immediately!**

        if sub_dir:
            traverse_url(new_url, sub_dir, result, flag)
    
def is_flag(endurl):
    r = requests.get(endurl).text
    return r if "flag" in r else None
    
if __name__ == "__main__":
    
    print("Getting the hidden dir inital links ...")
    hidden_dir = req_url(url)
    #expect a result like ['amcbevgondgcrloowluziypjdh/', ... , 'zzfzjvjsupgzinctxeqtzzdzll/', 'README']
    
    
    print("\n\nTraversing the hidden directory and its subfile ... can be long as recursive ...\n\n")
    subdir_url = []
    flag = []
    traverse_url(url, hidden_dir, subdir_url, flag)
    dir_size = len(subdir_url)

    if flag is not None :
        print("\n\nflag is :", flag)
    
    print("\niterating over each link to seea few stat: ...")
    print("\n1. getting its content \n2. stopping if contains flag and return \n3.otherwise get result occurence ...")

    freq = {}
    for (i,x) in enumerate(subdir_url):
        r = requests.get(x).text
        freq[r] = freq.get(r, 0) + 1
        sys.stdout.write(f"\rGetting content from downloadbale linl- total is now : {i} / {dir_size}")
        sys.stdout.flush()
    print("\n\nwhat were in the links ? here it is: \n\n")
    print(freq)


