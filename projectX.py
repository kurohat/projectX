from parse import parse
import db as dbHandler

args = parse()
mode, target, dbPath, output = args
print('scanning using mode %s' % mode)
if(mode == 'fuzz' or mode == 'payload'):
    print('the target website is %s' %target)
    print(dbHandler.readPayload(dbPath))
    # TO DO: send payload to web

    # TO DO: save result to the file
    print('the result is save in %s' % output)
    dbHandler.writeResult(output)
    print('DONE')
else: # run WAFWOOF
    print('woof woof woof')

