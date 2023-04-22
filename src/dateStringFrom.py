import datetime

def unix(time):
    return datetime.datetime.fromtimestamp(time).strftime("%Y-%m-%d %H:%M:%S")

def unixDelta(time):
    return str(datetime.timedelta(seconds=time))

def unixDay(time):
    return unix(time).split(" ")[0]