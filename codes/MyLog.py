from datetime import datetime

logpath = "log.txt"
def mylog(content):
    with open(logpath, "a",encoding='utf-8') as fp:
        now = datetime.now()
        fp.write(str(now)+"\n"+content+"\n")


# mylog("hello world")


