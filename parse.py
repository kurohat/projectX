"""
Description: parse argument and return to the main class
"""
import argparse


def parse():
    parser = argparse.ArgumentParser(description="ProjectX WAF vulnerability scanning tool")
    parser.add_argument('-F', '--fuzz', action="store_true", help="scanning WAF using fuzzing")
    parser.add_argument('-P', '--payload', action="store_true", help="scanning WAF using payload execution")
    parser.add_argument('-f', '--footprinting', action="store_true", help="footprinting WAF using WAFWOOF")
    parser.add_argument('-u', '--url', type=str, required=True, help="Target's WAF using WAFWOOF")
    parser.add_argument('-d', '--database', type=str, help="Absolute path to file contain payloads. the tool will use the default database if -d is not given")
    args = parser.parse_args()
    
    target = args.url
    if args.footprinting:
        return ['WAFWOOF', target]
    else:
        db = validateDatabase(args)
        if args.fuzz: #fuzzing
            return ['fuzz', target, db]
        elif args.payload:
            return ['payload', target, db]

def validateDatabase(args):
    if args.database is not None: # TO DO: check if file is exist
        return args.database
    else:
        return 'default' # TO DO: add defualt path point to db directory
   