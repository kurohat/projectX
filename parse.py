"""
Description: parse argument and return to the main class
"""
import argparse
import sys
from pathlib import Path
from datetime import datetime

FUZZ = 'fuzz'
PAYLOAD = 'payload'

def parse():
    parser = argparse.ArgumentParser(description="ProjectX WAF vulnerability scanning tool")
    parser.add_argument('-F', '--fuzz', action="store_true", help="scanning WAF using fuzzing")
    parser.add_argument('-P', '--payload', action="store_true", help="scanning WAF using payload execution")
    parser.add_argument('-f', '--footprinting', action="store_true", help="footprinting WAF using WAFWOOF")
    parser.add_argument('-u', '--url', type=str, required=True, help="Target's WAF using WAFWOOF")
    parser.add_argument('-d', '--database', type=str, help="Absolute path to file contain payloads. the tool will use the default database if -d is not given")
    parser.add_argument('-o', '--output', type=str, help="Name of the output file")
    args = parser.parse_args()
    
    target = args.url
    if args.footprinting:
        return ['WAFWOOF', target]
    else:
        out = validateOutput(args)
        if args.fuzz: #fuzzing
            db = validateDatabase(args, FUZZ)
            return ['fuzz', target, db, out]
        elif args.payload:
            db = validateDatabase(args, PAYLOAD)
            return ['payload', target, db, out]

def validateDatabase(args, mode):
    if args.database is not None: # TO DO: check if file is exist
        file = Path(args.database)
        if file.is_file():
            return args.database
        else:
            print('[!!] file not found \nusing default payloads')
            return getDefaultData(mode)
    else:
        return getDefaultData(mode)

def validateOutput(args):
    if args.output is not None:
        file = Path(args.output)
        if file.exists():
            print('[!!] file already exists \nusing default file name')
            return str(datetime.now()) + '.html'
    else:
        return str(datetime.now()) + '.html'

def getDefaultData(mode):
    if mode == FUZZ:
        return 'db/fuzz.txt' # TO DO: add defualt path point to db directory
    else:
        return 'db/payload.txt'