# projectX
WAF vulnerability scanning tool

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

# how to:
```console
# sqli
$ python3 projectX.py -sqli -u "http://169.254.179.84/vulnerabilities/sqli/?id=XXX&Submit=Submit#" -d text.html -o sqli.html -c PHPSESSID="mk5f489u62hilvgp9ml9peeccg",security="low"
# xss
$ python3 projectX.py -xss -u "http://169.254.179.84/vulnerabilities/xss_r/?name=XXX" -d text.html -o output2.html -c PHPSESSID="mk5f489u62hilvgp9ml9peeccg",security="low"
```