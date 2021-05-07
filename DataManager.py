import os
import json

def InitData():
    if not os.path.isfile('CheckerData.ini'):
        f = open('CheckerData.ini','w')
        f.write(str("{}"))
        f.close()

    # print('[DataManager] Inited')

def ReplaceData(tag, value):
    f = open('CheckerData.ini', 'r')
    a = json.loads(f.read())
    a[tag] = value
    f.close()

    f = open('CheckerData.ini', 'w')
    f.write(json.dumps(a))
    f.close()

    # print('[DataManager] Replaced {} : {}'.format(tag, value))

def ReadData():
    f = open('CheckerData.ini', 'r')
    a = json.loads(f.read())
    f.close()

    # print('[DataManager] Read {}'.format(a))
    return a