from parse import parse

args = parse()
mode, target, db = args
print('scanning using mode %s' % mode)
if(mode == 'fuzz' or mode == 'payload'):
    print(target)
    print(db)
else: # run WAFWOOF
    print('woof woof woof')