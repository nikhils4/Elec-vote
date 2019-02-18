import datetime as dt


dateNow = str(dt.datetime.date(dt.datetime.now())).split("-")
timeNow = str(dt.datetime.time(dt.datetime.now())).split(":")

dateNow = [int(x) for x in dateNow]
timeNow = [int(float(x)) for x in timeNow]

print(dateNow)
print(timeNow)

a = dt.datetime(dateNow[0],dateNow[1],dateNow[2],timeNow[0],timeNow[1],timeNow[2])
b = dt.datetime(2013,12,31,23,59,59)

(b-a).total_seconds()
print((b-a).total_seconds()
)