"""
Description: read payloads or write result
"""
import pandas as pd
import numpy as np
import webbrowser

def writeResult(output, results):
    f = open(output,'w')
    name = []
    status = []
    info = []
    for result in results:
        name.append(result[0].replace('>', '&gt;').replace('<', '&lt;'))
        status.append(result[1])
        info.append(result[2])
    
    df_marks = pd.DataFrame({'XSS': name,
     'Status': status,
     'Type': info})

    # add style to dataframe
    s = df_marks.style.applymap(color_fail_red, subset=['Status'])
    # render dataframe as html
    f.write('')
    f.write(s.render())
    f.close()
    #open file
    webbrowser.open('file://'+str(output))

def color_fail_red(row):
    """
    Takes a scalar and returns a string with
    the css property `'background-color: red'` for fail
    strings, green otherwise.
    """
    color = 'background-color: {}'.format('red' if row == 'fail' else 'green')
    return color