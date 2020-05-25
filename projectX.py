from parse import parse
# from bs4 import BeautifulSoup
from progress.bar import Bar
# import db as dbHandler
import urllib.parse
import subprocess
import requests
import pandas as pd
# import numpy as np
import webbrowser
from itertools import cycle
import json


def write_results(output, results):
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

        Fetching proxy from "http://proxylist.fatezero.org/proxy.list" 
        then test realiability for each ip buy sending to httpbin.org
        if the website return the sent ip then we add it in proxies list
        The proxies list is resturn when it reach the length of 15

    Arg:
        none

    Returns:
        proxies (list): list of proxy ip adresses x.x.x.x:xxxx
    """
    proxies = []
    r = requests.get("http://proxylist.fatezero.org/proxy.list")
    print("[+] Getting proxie list, this will take a fews sec")
    for line in r.iter_lines():
        if len(proxies) == 10:
            break
        line = json.loads(line.decode("utf-8"))
        if line["type"] == "https":
            ip = line["host"] +":"+ str(line["port"])
            try:
                response = requests.get('https://httpbin.org/ip',proxies={"http": ip, "https": ip})
                proxies.append(ip)
                print("[+] Got %s proxies" %len(proxies))
            except:
                print("[!] BAD proxy. skip to next one")  
                #Most free proxies will often get connection errors. You will have retry the entire request using another proxy to work. 
                #We will just skip retries as its beyond the scope of this tutorial and we are only downloading a single url
    print('[+] Got ALL 10 proxies')
    return proxies

def fire(mode, target, payload, header, count, proxy):
    """Firing payload to target website
    
        send payload to send it to target website.
        Check the respone and return the result. 
    
    Args:
        mode (str): tool mode = fuzzing / xss / sqli
        target (str): target website
        payload (str): payload that needed to be send to website
        header (json): html header
        count (int): count how many payload is sent
        proxy (str): ip address of the proxy site

    Returns:
        result (list): result of executed payload which include infomation such as
        payload, type, and status
    """
    payload = urllib.parse.quote(payload.replace('\n', ''))

    if proxy == None: # not using proxy
        r = requests.get(target.replace('projectX', payload), headers=header)
    else: # using proxy
        r = requests.get(target.replace('projectX', payload), headers=header, proxies={"http": proxy, "https": proxy})
        # print(r.json())
    # f = open('test.html', 'w')
    # f.write(r.text)
    # f.close()

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

def create_header(cookies):
    """create html header
    
        ask user if they want to use a bypass waf headers which are 
        X-Originating-IP:, X-Forwarded-For:, X-Remote-IP and X-Remote-Addr.
        Mentioned header can be use to bypass some waf products
    
    Args:
        cookies (str): website cookies for bypassing auth

    Returns:
        header (json): html header
    """

    usr_input = input("[?] Do you want to add a extension header ?\nThe headers inlude X-Originating-IP:, X-Forwarded-For:, X-Remote-IP, X-Remote-Addr: \nThe mentioned header can be use for bypassing some WAF products. [y/n]")
    if usr_input.lower() == 'y':
        header = {'content-type': 'application/json',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:72.0) Gecko/20100101 Firefox/72.0',
               'Accept-Encoding': 'gzip,deflate,sdch',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'Connection': 'keep-alive',
               'X-Originating-IP': '127.0.0.1',
               'X-Forwarded-For': '127.0.0.1',
               'X-Remote-IP': '127.0.0.1', 
               'X-Remote-Addr': '127.0.0.1',
               'Cookie': cookies}
    else:
        header = {'content-type': 'application/json',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:72.0) Gecko/20100101 Firefox/72.0',
               'Accept-Encoding': 'gzip,deflate,sdch',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'Connection': 'keep-alive',
               'Cookie': cookies}
    return header


def read_payload(mode, target, dbPath, header):
    """Read payloads from database and firing it to target website
    
        Read payload from the given path then firing the payloads to target website
        the process bar is shows when tool start sending payloads.
    
    Args:
        mode (str): tool mode = fuzzing / xss / sqli
        target (str): target website
        dbPath (str): path to database needed to be read
        header (json): html header

    Returns:
        results (list): results of executed payloads
    """
    count = 0
    results = []
    # using proxy?
    usr_input = input('[?] Do you want to use web proxy to advoid IP ban? \n[!] WARNING the tool performance will decrease if proxy is used [y/n]: ')
    # proxy pool in Round Robin queue
    proxy_pool = cycle(get_proxies()) if usr_input == 'y' else None

    # read payloads
    with open(dbPath, 'r') as payloads:
        payloads = payloads.readlines()
        bar = Bar('Processing', max=len(payloads))        
        for payload in payloads:
            count = count + 1
            if proxy_pool == None: # no proxy pool
                result = fire(mode, target, payload, header, count, None)
            else:
                proxy = next(proxy_pool) # pop IP from RR queue
                result = fire(mode, target, payload, header, count, proxy)
            if result != None:
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

if args[0] == 'wafw00f': # footprinting
    target = args[1]
    print('[+] The target website is %s' % target)
    print('[+] Executing wafw00f')
    output = subprocess.getoutput('python3 wafw00f-master/wafw00f/main.py {}'.format(target))
    print(output)
else:
    mode, target, dbPath, output, cookies = args # fixthis
    # fix cookies's format
    if cookies is not None:
        cookies = cookies.replace(',', '; ').replace(':', '=') + ";"
    # prepare html header
    header = create_header(cookies)
    print('[+] The target website is %s' % target)
    if dbPath == 'db/fuzz/': # defualt fuzzing
        results = read_payload('fuzz xss', target, dbPath+'xss.txt', header) # read fuzz/xss.txt
        result2 = read_payload('fuzz sqli', target, dbPath+'sqli.txt', header) # read fuzz/sqli.txt then append to the previous results
        results = results + result2
    else:  # xss or sqli
        results = read_payload(mode, target, dbPath, header)
    print('[+] The result is save in %s' % output)
    #writing output as .html
    write_results(output, results)
