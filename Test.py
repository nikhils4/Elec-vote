import datetime
from datetime import date

dbDate = dbDate.split("-")
dbDate = [int(x) for x in dbDate]
today = str(date.today()).split("-")
today = [int(x) for x in d1]
age =  date(today[0], today[1], today[2]) - date(dbDate[0], dbDate[1], dbDate[2])
age = age.days//365
return age