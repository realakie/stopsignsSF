import main
from main import *

#data from https://data.sfgov.org/Transportation/Stop-Signs/4542-gpa3
dataStopSign = main.cleanup('Stopsigns.csv') #API didn't include Neighborhoods column
start = [35,'Q']
end = [40,'I']
if (end[0] - start[0]) == 0 or (ord(end[1]) - ord(start[1])) == 0:
    print("Go Straight")
result = main.minstops(dataStopSign, start, end, 0, 0, 'Start')
print("Minimum Number of Stop signs encountered: ", result[0])
print(result[1])

#thisloc = [[35, 'Q']]
#thisloc.append([34,'R'])
#print(thisloc)