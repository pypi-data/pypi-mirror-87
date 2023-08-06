from RootInteractive.Tools.pandaTools import *
from RootInteractive.InteractiveDrawing.bokeh.bokehTools import *
import pandas as pd
import numpy as np
import ast

df = pd.DataFrame(np.random.random_sample(size=(500, 4)), columns=list('ABCD'))
initMetadata(df)

def parseString0(widgetString):
    toParse = "(" + widgetString + ")"
    #theContent = pyparsing.Word(pyparsing.alphanums + ".+-_[]{}") | '#' | pyparsing.Suppress(',') | pyparsing.Suppress(':')
    theContent =  pyparsing.Word(pyparsing.alphanums + ",.+-_[]{}:\ '")
    widgetParser = pyparsing.nestedExpr('(', ')', content=theContent)
    widgetList = widgetParser.parseString(toParse)[0]
    print(widgetList)
    return widgetList

def parseString(widgetString):
    r'''
    '''
    toParse = "(" + widgetString + ")"
    #theContent = pyparsing.Word(pyparsing.alphanums + ".+-_[]{}") | '#' | pyparsing.Suppress(',') | pyparsing.Suppress(':')
    theContent =  pyparsing.Word(pyparsing.alphanums + ",.+-_[]{}:\ '") | pyparsing.Suppress(',') | pyparsing.Suppress(' ')
    widgetParser = pyparsing.nestedExpr('(', ')', content=theContent)
    widgetList = widgetParser.parseString(toParse)[0]
    print(widgetList)
    for i, var in enumerate(widgetList):
        if isinstance(var, pyparsing.ParseResults):
            if var[0][0]=='{':
                options=""
                for var in widgetList[i]: options+=var+","
                options=ast.literal_eval(options[0:-1])
                print("option", options)
                widgetList[i]=options
            else:
                widgetList[i]=var[0].split(",")
                print("array", widgetList[i])
        else:
            widgetList[i]=var.replace(" ","").replace(",","")
    print(widgetList)
    return widgetList



widgetString="range.A({'type':'minmax','nBins':10}),  slider.C(0, 10, 100,0,1), slider.D({'type':'nsigma','nSigma':20}),range.A({'type':'minmax','nBins':10})"
widgetList=parseString(widgetString)



