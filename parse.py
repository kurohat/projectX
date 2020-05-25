"""
Description: parse arguments and return to the main class
"""
import argparse
# import sys
from pathlib import Path
from datetime import datetime


def parse():
    """Parse user given arguments

    Returns:
        parsed args (list): list of parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="ProjectX WAF testing tool")
    parser.add_argument('-F', '--fuzz', action="store_true",
                        help="testing WAF using fuzzing")
    parser.add_argument('-xss', '--xss', action="store_true",
                        help="testing WAF by executing XSS payloads")
    parser.add_argument('-sqli', '--sqli', action="store_true",
                        help="testin WAF by executing SQL payloads")
    parser.add_argument('-f', '--footprinting', action="store_true",
                        help="footprinting WAF using WAFWOOF")
    parser.add_argument('-t', '--target', type=str, required=True,
                        help='target\'s url and "projectX" where the payloads will be replace.\nFor instance: -t "http://<YOUR_HOST>/?param=projectX"')
    parser.add_argument('-d', '--database', type=str,
                        help="Absolute path to file contain payloads. the tool will use the default database if -d is not given")
    parser.add_argument('-o', '--output', type=str,
                        help="Name of the output file ex -o output.html")
    parser.add_argument('-c', '--cookies', type=str,
                        help='cookies for the secssion. Use "," (comma) to separeate cookies\nFor instance: -c cookie1="something",cookie2="something"')
    args = parser.parse_args()


    print(type(args))
    target = args.target
    # check mode
    if args.footprinting: 
        return ['wafw00f', target]
    else:
        out = validate_output(args)
        cookies = args.cookies
        path = validate_database(args)
        if args.fuzz:  # fuzzing
            return ['fuzz', target, path, out, cookies]
        elif args.xss:
            return ['xss', target, path, out, cookies]
        elif args.sqli:
            return ['sqli', target, path, out, cookies]


def validate_database(args):
    """validating given database
    
        check if the given database is exists, if not exists then the default database will be use
        if the given path to database if exits the the given path will be use.

    Args:
        args (list): arguments given by user

    Returns:
        database path (str): path to payload database
    """
    if args.database is not None:  # TO DO: check if file is exist
        file = Path(args.database)
        if file.is_file():
            return args.database
        else:
            print('[!!] file not found: Using default payloads')
            return get_defaultpath(args)
    else:
        return get_defaultpath(args)


def validate_output(args): #to do: come upwith better defualt name
    """validating output file name
    
        check if the output file exists, if not exists then it will use the given name
        if the file already exists then defualt file name (executed timestam) will be use.
    
    Args:
        args (list): arguments given by user

    Returns:
        file name (str): output file name .html
    """
    if args.output is not None:
        file = Path(args.output)
        if file.exists():
            print('[!!] file already exists: Using default file name')
            return Path(removeWhiteSpace(datetime.now())).resolve()
        else:
            return Path(args.output).resolve()
    else:
        return Path(removeWhiteSpace(datetime.now())).resolve()


def get_defaultpath(args):
    """get defualt path to the database
    
        check tool mode then return the defualt path to database base on tool mode
    
    Args:
        args (list): arguments given by user

    Returns:
        defualt path (str): path to dabase base on tool mode
    """
    if args.fuzz:
        return 'db/fuzz/' # fix this
    elif args.xss:
        return 'db/xss.txt'
    else:
        return 'db/sqli.txt'


def removeWhiteSpace(f):
    fName = str(f)+'.html'.replace(" ", "")
    return fName
