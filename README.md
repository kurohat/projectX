# projectX
WAF vulnerability scanning tool
Special thank to all contributors @Awesome-WAF(https://github.com/0xInfection/Awesome-WAF/graphs/contributors) repo

table 
- https://pandas.pydata.org/pandas-docs/stable/user_guide/style.html
- https://pythonexamples.org/pandas-render-dataframe-as-html-table/

# requriment
- jinja2
- pandas
- argparse
- pathlib
- requests
- progress: https://pypi.org/project/progress/


# useful
- https://github.com/s0md3v/XSStrike/blob/4032e40c671ad5ad0919a9e9f2ecbd2e9edabe50/core/config.py
- https://github.com/fate0/proxylist

# header
```python
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

    # check for status 
    for testing without waf
    if mode == 'xss':
        status = 'fail' if r.text.find('=alert') == -1 else 'pass'
    elif mode == 'sqli':
        # URL encode
        status = 'fail' if r.text.find('First name: Hack') == -1 else 'pass'
    else:
        status = 'fail' if r.text.find(payload) == -1 else 'pass'
```
# setup dvwa
- https://kifarunix.com/how-to-setup-damn-vulnerable-web-app-lab-on-ubuntu-18-04-server/

# setup nginx
- https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-naxsi-on-ubuntu-16-04
- https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-ubuntu-16-04

# how to:
```console
# sqli
$ python3 projectX.py -sqli -t "http://169.254.179.84/vulnerabilities/sqli/?id=XXX&Submit=Submit#" -o sqli.html -c PHPSESSID="mk5f489u62hilvgp9ml9peeccg",security="low"
# xss
$ python3 projectX.py -xss -t "http://169.254.179.84/vulnerabilities/xss_r/?name=XXX" -o output2.html -c PHPSESSID="mk5f489u62hilvgp9ml9peeccg",security="low"
# fuzz
$ python3 projectX.py -F -t "http://169.254.179.84/vulnerabilities/xss_r/?name=XXX" -o fuzz.html -c PHPSESSID="mk5f489u62hilvgp9ml9peeccg",security="low"

```