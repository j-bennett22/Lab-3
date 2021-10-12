import requests
import urllib.request 
from os    import path
import re
from collections import Counter

## Logfile URL 
url = "https://s3.amazonaws.com/tcmg476/http_access_log"

print("Checking to see if log already exists:")

if  not path.exists('log'):
	print("Log did not exist, downloading from: ")
	print(url)
	urllib.request.urlretrieve(url, 'log')
	print("Done downloading")
else:
	print("Log existed, skipping download.\n")

r = requests.get(url, stream = True)

## Open and copy to new local file
with open("local_copy.txt","wb") as textfile:
   for chunk in r.iter_content(chunk_size=1024):

       if chunk:
           textfile.write(chunk)

# opening of the local file
file = open ("local_copy.txt")

# Creation of some variables in order to make the printing of these long queries a bit easier
result1 = {"Requests per each given day": {}}
result2 = {"Requests per each given week": {}}
result3 = {"Requests per each given month": {}}

date_day = None
days = 0
week = None
months_done = []

for line in file:
    
    if len(line) >= 56:
        data = line.split()
        date = data[3][1::].split(':')
        if not (date_day == date[0]):
            date_day = date[0]
            days += 1
            if days % 7 == 0:
                week = date_day
       
        ## Count file requests per day
        if date[0] in result1["Requests per each given day"]:
            result1["Requests per each given day"][date[0]] += 1
        else:
            result1["Requests per each given day"][date[0]] = 0
        
        ## Count file requests per week
        if week in result2["Requests per each given week"]:
            result2["Requests per each given week"][week] += 1
        else:
            result2["Requests per each given week"][week] = 0
        month = date[0][3::]
        
        ## Create a new file for the new month data
        if month not in months_done:
            file_name = month[:3:] + month[4::]
            if (len(file_name)) == 7:
                month_file = open(month[:3:] + month[4::] + ".txt", 'w')
                print(file_name)
            months_done.append(month)
        month_file.write(line)

      ## Count file requests per month
        if month in result3["Requests per each given month"]:
            result3["Requests per each given month"][month] += 1
        else:
            result3["Requests per each given month"][month] = 0

# adjusted regular expression to break the log file lines down into readable groups
regex = re.compile(r".*\[([^:]*):(.*) \-[0-9]{4}\] \"([A-Z]+) (.+?)( HTTP.*\"|\") ([2-5]0[0-9]) .*")


file = open('log', 'r')

logfile =[]

# Loop through the file, place each line into logfile array
for line in file:
    logfile.append(line)

code_4xx = 0
code_3xx = 0
file_requests = []

# Loop throough logfile array, break each line using regex
for element in logfile:
	pieces = re.split(regex, element)
	# counting the amount of 3xx and 4xx responses using the broken down lines
	try:
		file_requests.append(pieces[4])
		if pieces[6].startswith('3'):
			code_3xx+=1
		if pieces[6].startswith('4'):
			code_4xx+=1
	except IndexError:
		pass
	continue

total_count = 0
for item in logfile:
    total_count+=1

print('')
print(result1)
print('')
print(result2)
print('')
print(result3)
print('')

print("Total amount of 4xx responses within the log file: ", code_4xx)
percent_4xx = (code_4xx/total_count) * 100
print('Percentage of 4xx responses in relation to the total amount of log lines: ', round(percent_4xx,2))
print('')

print("Total amound of 3xx responses within the log file: ", code_3xx)
percent_3xx = (code_3xx / total_count) * 100
print('Percentage of 3xx responses in relation to the total amount of log lines: ', round(percent_3xx,2))
print('')

# Count most requested file 
Counter = Counter(file_requests)
most_freq = Counter.most_common(1)
print('The most requested file within the log file is: ')
print(most_freq)
print('')

# The count for the total amount of lines in the log file
total_count = 0
for item in logfile:
    total_count+=1

print("Total line count= ", total_count)
print('-------------------------')
