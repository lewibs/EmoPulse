import datetime as dt
import dateStringFrom

def datetime(date):
    # Convert the datetime object to UTC
    utc_date = date.astimezone(dt.timezone.utc)
    # Convert the UTC datetime object to a Unix timestamp 
    return int(utc_date.timestamp())

def timedelta(date):
    return date.total_seconds()

def roundToDay(unix):
    return unix - (unix % 86400)

def stampInDay(unix):
    time_str = dateStringFrom.unix(unix).split(" ")[1]
    times = [int(time) for time in time_str.split(":")]
    
    return times[0] * 3600 + times[1] * 60 + times[2]
