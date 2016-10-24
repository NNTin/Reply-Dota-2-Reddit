import time

def unixTimeConverter(timeVar):
    timeVarStr = str(timeVar)
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(timeVarStr)))

def durationTimeConverter(timeVar):
    m, s = divmod(int(timeVar), 60)
    return "%d:%02d" % (m, s)