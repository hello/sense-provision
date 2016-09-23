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
        print e
        pass

def loge(st):
    redirect("[ERROR]\t" + st)
    
def logi(st):
    redirect("[INFO]\t" + st)

def logs(st):
    redirect("[SENSE]\t" + st)
