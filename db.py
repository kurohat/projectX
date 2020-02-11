"""
Description: read payloads or write result
"""
def readPayload(path):
    f = open(path)
    return f.read()

def writeResult(path):
    f = open(path,'w')
    message = """<html>
    <head></head>
    <body><p>Hello World!</p></body>
    </html>"""
    f.write(str(message))
    f.close()