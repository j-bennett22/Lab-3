#first import is from AMIKEAL on GITHUB https://gist.github.com/amikeal/4e2847e3977a787e071e81014fe43390
# imported regex to make parsing a bit more straightforward instead of doing a mega if statement
from urllib.request import urlretrieve
import re

# just making some variables here to use later for counting
# count6mnths is going to become a list/array

countTotal = 0
count6mnths = 0

# this is a check for a local copy of the log file, if it's not there, it downloads it again

try:
    f = open("local_copy.log")
except FileNotFoundError:
    local_file, headers = urlretrieve('https://s3.amazonaws.com/tcmg476/http_access_log', 'local_copy.log')
    print()
else:
    print('File already exists')
    print()


# count the total amount of requests in the log

for line in open('local_copy.log'):
    countTotal += 1

# finding all of the instances where one of the lines of the log files is dated to one of the past 6 months
# putting that into a big list and then just creating a variable that holds the 'len' which represents the total number of requests within the past 6 months

with open('local_copy.log') as n:
    logFile = n.read()

    may = re.findall('May/1995', logFile)
    jun = re.findall('Jun/1995', logFile)
    jul = re.findall('Jul/1995', logFile)
    aug = re.findall('Aug/1995', logFile)
    sep = re.findall('Sep/1995', logFile)
    oct = re.findall('Oct/1995', logFile)
    count6mnths = may+jun+jul+aug+sep+oct
    mnth6total = len(count6mnths)


print('There were ', countTotal,' requests made within the time period of the log file (10/24/1994 - 10/11/1995)')
print()


print('Within the previous six months starting at 10/11/1955, there were ', mnth6total, 'requests from the log file')
print()