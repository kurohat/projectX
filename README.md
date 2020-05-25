# projectX
WAF testing tool offer 4 testing methods:
1. Footprinting
2. Fuzzing (XSS, SQL)
3. Payload execution (XSS, SQL)
4. Bypassing


Special thank to all contributors [Awesome-WAF](https://github.com/0xInfection/Awesome-WAF/graphs/contributors) repo. Moreover, this research could not be done without [WAFNinja](https://github.com/khalilbijjou/WAFNinja), since it was the tool that inspired me to work on this project and give me the idea of creating ProjectX. Lastly, ProjectX would not be able to offer "all-in-one" feature without [Wafw00f](https://github.com/EnableSecurity/wafw00f), since it is used in ProjectX when performing footprinting testing methods.

# Installation
```console
$ pip3 install -r requirements.txt # setup ProjectX
$ python wafw00f-master/setup.py install # setup Wafw00f
```

# Usage

## Man page
```console
$ python3 projectX.py -h

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

usage: projectX.py [-h] [-F] [-xss] [-sqli] [-f] -t TARGET [-d DATABASE]
                   [-o OUTPUT] [-c COOKIES]

ProjectX WAF testing tool

optional arguments:
  -h, --help            show this help message and exit
  -F, --fuzz            testing WAF using fuzzing
  -xss, --xss           testing WAF by executing XSS payloads
  -sqli, --sqli         testin WAF by executing SQL payloads
  -f, --footprinting    footprinting WAF using WAFWOOF
  -t TARGET, --target TARGET
                        target's url and "projectX" where the payloads will be
                        replace. For instance: -t
                        "http://<YOUR_HOST>/?param=projectX"
  -d DATABASE, --database DATABASE
                        Absolute path to file contain payloads. the tool will
                        use the default database if -d is not given
  -o OUTPUT, --output OUTPUT
                        Name of the output file ex -o output.html
  -c COOKIES, --cookies COOKIES
                        cookies for the secssion. Use "," (comma) to separeate
                        cookies For instance: -c
                        cookie1="something",cookie2="something"
```
## Fuzzing mode
```console
$ python3 projectX.py -F -t "<target IP>/?q=projectX" -o fuzz.html -c cookie="something"
```
the payloads will be replace with ```projectX``` in ``-t`` so dont for get to include it
## XSS Payload execution mode
```console
$ python3 projectX.py -xss -t "<target IP>/?name=projectX" -o xss.html -c cookie1="something",cookie2="something"
```
the payloads will be replace with ```projectX``` in ``-t`` so dont for get to include it

## SQL Payload execution mode
```console
$ python3 projectX.py -sqli -t "<target IP>/?name=projectX" -o sql.html -c cookie1="something",cookie2="something"
```
the payloads will be replace with ```projectX``` in ``-t`` so dont for get to include it

## Footprinting
ProjectX is use [Wafw00f](https://github.com/EnableSecurity/wafw00f) to prefrom footprintin
```console
$ python3 projectX.py -f -t "<target IP>"
```

# Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. need a Idea?


As a future work continuation on improving the tools would be interesting.  The code injection has been the most common vulnerability in the past ten years based on the OWASP top ten list. It would be interesting to add more fuzzing mode and payload execution to ProjectX. For instance, XML External Entity (XXE) Injection and Command Injection. When ProjectX is performing fuzzing mode, it fuzzes both XSS and SQL at the same time. Another thing that would be interesting is to split fuzzing mode so the tester specifically fuzzes what they want, not both XSS and SQLI at the same time. Furthermore, testing the tool on different WAF products/vendors could also be possible and beneficial. Lastly, both default payload executions and fuzzing databases should be updated to make to ProjectX more powerful
