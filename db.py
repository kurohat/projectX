"""
Description: read payloads or write result
"""
import pandas as pd
import numpy as np
import webbrowser

def readPayload(path):
    f = open(path)
    return f.read()

def writeResult(output):
    f = open(output,'w')
    #dummy text
    df_marks = pd.DataFrame({'name': ['Somu', 'Kiku', 'Amol', 'Lini'],
     'physics': ['pass', 'fail', 'pass', 'pass'],
     'chemistry': [84, 56, 73, 69],
     'algebra': [78, 88, 82, 87]})

    # add style to dataframe
    s = df_marks.style.applymap(color_fail_red, subset=['physics'])
    # render dataframe as html
    f.write(s.render())
    f.close()
    #open file
    webbrowser.open('file://'+str(output))  # open in new tab

def color_fail_red(row):
    """
    Takes a scalar and returns a string with
    the css property `'background-color: red'` for fail
    strings, green otherwise.
    """
    color = 'background-color: {}'.format('red' if row == 'fail' else 'green')
    return color