from dateutil.parser import parse
import datetime

def handle(inat, duration):
    today = datetime.date.today()
    tt = parse(duration)
    if inat == "in":
        return (tt - datetime.datetime(today.year, today.month, today.day)).total_seconds()
    elif inat == "at":
        return (tt - datetime.datetime(datetime.time.now())).total_seconds()
    else:
        raise ValueError("Invalid")