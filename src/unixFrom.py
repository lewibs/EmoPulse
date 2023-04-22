import datetime as dt

def datetime(date):
    # Convert the datetime object to UTC
    utc_date = date.astimezone(dt.timezone.utc)
    # Convert the UTC datetime object to a Unix timestamp 
    return int(utc_date.timestamp())

def timedelta(date):
    return date.total_seconds()

def roundToDay(unix):
    return unix - (unix % 86400)