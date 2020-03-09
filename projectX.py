from parse import parse
# from bs4 import BeautifulSoup
from progress.bar import Bar
import db as dbHandler
import urllib.parse
import requests
import json


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
    # r = requests.post(t, data=json.dumps(body), headers=headers)
    # savefile
    # f = open('test'+str(count)+'.html','w')
    # f.write(r.text)
    # f.close()
    payload = urllib.parse.quote(payload.replace('\n', ''))
    r = requests.get(target.replace('XXX', payload), headers=headers)
    
    # check for status
    if mode == 'xss':
        status = 'fail' if r.text.find('=alert') == -1 else 'pass'
    elif mode == 'sqli':
        # URL encode
        status = 'fail' if r.text.find('First name: Hack') == -1 else 'pass'
    else:
        status = 'fail' if r.text.find(payload) == -1 else 'pass'

    result = (urllib.parse.unquote(payload), status, mode)
    return result

def readPayload(mode, target, dbPath, cookies):
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
            results.append(result)
            bar.next()
    bar.finish()  
    return results

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
mode, target, dbPath, output, cookies = args 
# fix cookies's format
cookies = cookies.replace(',', '; ').replace(':', '=') + ";"
print('scanning using mode %s' % mode)
if(mode == 'WAFWOOF'): # footprinting
    print('woof woof woof')
else:
    print('the target website is %s' % target)
    if dbPath == 'db/fuzz/': # defualt fuzzing
        results = readPayload('fuzz xss', target, dbPath+'xss.txt', cookies) # read fuzz/xss.txt
        result2 = readPayload('fuzz sqli', target, dbPath+'sqli.txt', cookies) # read fuzz/sqli.txt then append to the previous results
        results = results + result2
    else:  # xss or sqli
        results = readPayload(mode, target, dbPath, cookies)
    print('the result is save in %s' % output)
    #writing output as .html
    dbHandler.writeResult(output, results)
    print('DONE')
