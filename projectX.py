from parse import parse
import db as dbHandler
import requests
import json

def fire(t,db,cookie):
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
    "Connection": "keep-alive" ,
    "Cookie": cookie}
    body = {'<x onclick=alert(1)>click this!'}
    # r = r.prepare()
    r = requests.get(t, headers=headers)
    # r = requests.post(t, data=json.dumps(body), headers=headers)
    f = open('test.html','w')
    f.write(r.text)
    f.close()

args = parse()
mode, target, dbPath, output, cookies = args
# fix cookies's format
cookies = .replace(',', '; ').replace(':', '=') + ";"
print('scanning using mode %s' % mode)
if(mode == 'fuzz' or mode == 'payload'):
    print('the target website is %s' %target)
    print(dbHandler.readPayload(dbPath))
    # TO DO: send payload to web
    fire(target, dbPath, cookies)
    # TO DO: save result to the file
    print('the result is save in %s' % output)
    # dbHandler.writeResult(output)
    print('DONE')
else: # run WAFWOOF
    print('woof woof woof')

