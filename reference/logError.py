import traceback
import datetime

def whatever():
    print(1/0)

try:
    whatever()
except:
    f = open('error_{}.log'.format(str(datetime.datetime.now()).replace(' ','_').replace(':','-')), 'w')
    f.write(str(traceback.format_exc()))
    f.close()