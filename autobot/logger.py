import datetime
log = None
def setlog(f):
    global log
    log = f
    
def redirect(st):
    global log
    st = "[%s]"%(datetime.datetime.now().isoformat())+st
    print st
    try:
        log.write(st.rstrip()+'\n')
    except Exception as e:
        pass

def loge(st):
    redirect("[ERROR]\t" + st)
    
def logi(st):
    redirect("[INFO]\t" + st)

def logs(st):
    redirect("[SENSE]\t" + st)

import json
import requests
def slack(st):
    j = json.dumps({"text":st})
    print requests.post("https://hooks.slack.com/services/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", data = j)
