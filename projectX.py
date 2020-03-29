from parse import parse
# from bs4 import BeautifulSoup
from progress.bar import Bar
# import db as dbHandler
import urllib.parse
import subprocess
import requests
import pandas as pd
import numpy as np
import webbrowser

def writeResult(output, results):
    """Writing result as a html file
    
        Using pandas to create a html table and save it as a html file
    
    Args:
        output (str): path to the output file
        results (list): a list contains results
    """

    f = open(output, 'w')
    name = []
    status = []
    info = []
    for result in results:
        name.append(result[0].replace('>', '&gt;').replace('<', '&lt;'))
        status.append(result[1])
        info.append(result[2])

    df_marks = pd.DataFrame({'Payload': name,
                             'Status': status,
                             'Type': info})

    # add style to dataframe
    s = df_marks.style.applymap(color_fail_red, subset=['Status'])
    # render dataframe as html
    f.write('')
    f.write(s.render())
    f.close()
    # open file
    webbrowser.open('file://'+str(output))


def color_fail_red(row):
    """Takes a scalar and returns a string with
    the css property `'background-color: red'` for fail
    strings, pass = green
    """
    color = 'background-color: {}'.format('red' if row == 'fail' else 'green')
    return color


def get_proxies():
    """Fetching proxy

        Fetching proxy from "http://proxylist.fatezero.org/proxy.list" and put frist 20 ips
        in a list

    Arg:
        none

    Returns:
        proxies (list): list of proxy ip adresses x.x.x.x:xxxx
    """
    proxies = []
    r = requests.get("http://proxylist.fatezero.org/proxy.list", stream=True)
    while len(proxies) < 21:
        for line in r.iter_lines():
            line = json.loads(line.decode("utf-8"))
            if line["type"] == "https":
                ip = line["host"] +":"+ str(line["port"])
                proxies.append(ip)
    return proxies

def fire(mode, target, payload, cookie, count):
    """Firing payload to target website
    
        Create a http header using rquests module then send it to target website.
        Check the respone and return the result. 
    
    Args:
        mode (str): tool mode = fuzzing / xss / sqli
        target (str): target website
        payload (str): payload that needed to be send to website
        cookies (str): website cookies for bypassing auth
        count (int): count how many payload is sent

    Returns:
        result (list): result of executed payload which include infomation such as
        payload, type, and status
    """

    """
    GET http://169.254.179.84/ HTTP/1.1
    User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:72.0) Gecko/20100101 Firefox/72.0
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
    Accept-Language: sv-SE,sv;q=0.8,en-US;q=0.5,en;q=0.3
    Connection: keep-alive
    Cookie: PHPSESSID=mk5f489u62hilvgp9ml9peeccg; security=low
    Upgrade-Insecure-Requests: 1
    Host: 169.254.179.84
    """
    headers = {'content-type': 'application/json',
               "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:72.0) Gecko/20100101 Firefox/72.0",
               "Accept-Encoding": "gzip,deflate,sdch",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
               "Connection": "keep-alive",
               "Cookie": cookie}

    payload = urllib.parse.quote(payload.replace('\n', ''))
    r = requests.get(target.replace('XXX', payload), headers=headers)
    
    # f = open('test.html', 'w')
    # f.write(r.text)
    # f.close()

    # check for status
    # if mode == 'xss':
    #     status = 'fail' if r.text.find('=alert') == -1 else 'pass'
    # elif mode == 'sqli':
    #     # URL encode
    #     status = 'fail' if r.text.find('First name: Hack') == -1 else 'pass'
    # else:
    #     status = 'fail' if r.text.find(payload) == -1 else 'pass'
    status = 'pass' if r.status_code == 200 else 'fail'

    #Fuzzing mode then keep pass and fail, payload execution keep only pass
    if mode == 'xss' or mode == 'sqli':
        if status == 'pass':
            result = (urllib.parse.unquote(payload), status, mode)
        else:
            return None
    else:
        result = (urllib.parse.unquote(payload), status, mode)
    return result

def read_payload(mode, target, dbPath, cookies):
    """Read payloads from database and firing it to target website
    
        Read payload from the given path then firing the payloads to target website
        the process bar is shows when tool start sending payloads.
    
    Args:
        mode (str): tool mode = fuzzing / xss / sqli
        target (str): target website
        dbPath (str): path to database needed to be read
        cookies (str): website cookies for bypassing auth

    Returns:
        results (list): results of executed payloads
    """
    count = 0
    results = []
    # read payloads
    with open(dbPath, 'r') as payloads:
        payloads = payloads.readlines()
        bar = Bar('Processing', max=len(payloads))        
        for payload in payloads:
            count = count + 1
            result = fire(mode, target, payload, cookies, count)
            if result != None:
                results.append(result)
            bar.next()
    bar.finish()  
    return results

def callWafw00f(target): # todo: create method for wafw00f
    print('bla')

logo = """
                        t#,                   ,;      .,                        
 t         j.          ;##W. itttttttt      f#i      ,Wt                        
 ED.       EW,        :#L:WE fDDK##DDi    .E#t      i#D. GEEEEEEEL              
 E#K:      E##j      .KG  ,#D   t#E      i#W,      f#f   ,;;L#K;;.   :KW,      L
 E##W;     E###D.    EE    ;#f  t#E     L#D.     .D#i       t#E       ,#W:   ,KG
 E#E##t    E#jG#W;  f#.     t#i t#E   :K#Wfff;  :KW,        t#E        ;#W. jWi 
 E#ti##f   E#t t##f :#G     GK  t#E   i##WLLLLt t#f         t#E         i#KED.  
 E#t ;##D. E#t  :K#E:;#L   LW.  t#E    .E#L      ;#G        t#E          L#W.   
 E#ELLE##K:E#KDDDD###it#f f#: jfL#E      f#E:     :KE.      t#E        .GKj#K.  
 E#L;;;;;;,E#f,t#Wi,,, f#D#;  :K##E       ,WW;     .DW:     t#E       iWf  i#K. 
 E#t       E#t  ;#W:    G#t     G#E        .D#;      L#,    t#E      LK:    t#E 
 E#t       DWi   ,KK:    t       tE          tt       jt     fE      i       tDj
                                  .                           :                 
Develop by Amata A. Github: gu2rks
"""
print(logo)
# parse the given input
args = parse()

# mode, target, dbPath, output, cookies = args # fixthis
# fire(mode, target, 'onabort', cookies, 1)

if args[0] == 'wafw00f': # footprinting
    target = args[1]
    print('the target website is %s' % target)
    print('executing wafw00f')
    output = subprocess.getoutput('python3 wafw00f-master/wafw00f/main.py {}'.format(target))
    print(output)
else:
    mode, target, dbPath, output, cookies = args # fixthis
    # fix cookies's format
    cookies = cookies.replace(',', '; ').replace(':', '=') + ";"
    print('the target website is %s' % target)
    if dbPath == 'db/fuzz/': # defualt fuzzing
        results = read_payload('fuzz xss', target, dbPath+'xss.txt', cookies) # read fuzz/xss.txt
        result2 = read_payload('fuzz sqli', target, dbPath+'sqli.txt', cookies) # read fuzz/sqli.txt then append to the previous results
        results = results + result2
    else:  # xss or sqli
        results = read_payload(mode, target, dbPath, cookies)
    print('the result is save in %s' % output)
    #writing output as .html
    writeResult(output, results)
    print('DONE')
