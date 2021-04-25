import os
import json

def InitData():
    if not os.path.isfile('CheckerData.ini'):
        f = open('CheckerData.ini','w')
        f.write(str("{}"))
        f.close()

def ReplaceData(tag, value):
    f = open('CheckerData.ini', 'r')
    a = json.loads(f.read())
    a[tag] = value
    f.close()

    f = open('CheckerData.ini', 'w')
    f.write(json.dumps(a))
    f.close()

def ReadData():
    f = open('CheckerData.ini', 'r')
    a = json.loads(f.read())
    f.close()
    return a