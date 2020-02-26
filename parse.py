"""
Description: parse argument and return to the main class
"""
import argparse
import sys
from pathlib import Path
from datetime import datetime


def parse():
    parser = argparse.ArgumentParser(
        description="ProjectX WAF vulnerability scanning tool")
    parser.add_argument('-F', '--fuzz', action="store_true",
                        help="scanning WAF using fuzzing")
    parser.add_argument('-xss', '--xss', action="store_true",
                        help="scanning WAF by executing xss payloads")
    parser.add_argument('-sqli', '--sqli', action="store_true",
                        help="scanning WAF by executing xss payloads")
    parser.add_argument('-f', '--footprinting', action="store_true",
                        help="footprinting WAF using WAFWOOF")
    parser.add_argument('-u', '--url', type=str, required=True,
                        help="Target's WAF using WAFWOOF")
    parser.add_argument('-d', '--database', type=str,
                        help="Absolute path to file contain payloads. the tool will use the default database if -d is not given")
    parser.add_argument('-o', '--output', type=str,
                        help="Name of the output file ex -o output.html")
    parser.add_argument('-c', '--cookies', type=str,
                        help="cookies for the secssion. use, to separeate cookies")
    args = parser.parse_args()

    target = args.url
    if args.footprinting:
        return ['WAFWOOF', target]
    else:
        out = validateOutput(args)
        cookies = args.cookies
        path = validateDatabase(args)
        if args.fuzz:  # fuzzing
            return ['fuzz', target, path, out, cookies]
        elif args.xss:
            return ['xss', target, path, out, cookies]
        elif args.sqli:
            return ['sqli', target, path, out, cookies]


def validateDatabase(args):
    if args.database is not None:  # TO DO: check if file is exist
        file = Path(args.database)
        if file.is_file():
            return args.database
        else:
            print('[!!] file not found \nusing default payloads')
            return getDefaultData(args)
    else:
        return getDefaultData(args)


def validateOutput(args):
    if args.output is not None:
        file = Path(args.output)
        if file.exists():
            print('[!!] file already exists \nusing default file name')
            return Path(removeWhiteSpace(datetime.now())).resolve()
        else:
            return Path(args.output).resolve()
    else:
        return Path(removeWhiteSpace(datetime.now())).resolve()


def getDefaultData(args):
    if args.fuzz:
        return 'db/fuzz.txt'
    elif args.xss:
        return 'db/xss.txt'
    else:
        return 'db/sqli.txt'


def removeWhiteSpace(f):
    fName = str(f)+'.html'.replace(" ", "")
    return fName
