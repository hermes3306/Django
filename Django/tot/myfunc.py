import datetime

def today():
    d = datetime.date.today()
    t = d.strftime("%y%m%d")
    return t


