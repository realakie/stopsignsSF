# This is the first stopsign project.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
# Avoidance/Block street list to be added

import pandas as pd
import re



def cleanup(filename):
    df = pd.read_csv(filename,header = 1) # Filter the top row
    df = df[['STREET','X_STREET','ST_FACING','Neighborhoods']] #filtering by the column names
    df['Neighborhoods']=df['Neighborhoods'].fillna(0).astype(int) #filtering by the neighborhood
    sunsetneighborhood = [39,40,46,109]
    filter = df.Neighborhoods.isin(sunsetneighborhood)
    df = df[filter]
    df = df.reset_index(drop = True)
    #print(df)

    #Clear the names of the street to numbers and x_street to ABCs
    for x in df.index: #for each row
        streetFirst = df.iat[x,0]
        streetSecond = df.iat[x,1]
        numStreet = streetFirst
        abcStreet = streetSecond

        if streetFirst[0].isdigit():
            numStreet = int(re.findall('\d+',streetFirst)[0])
            abcStreet = streetSecond[0] #Get the first letter of the Aphabet
        elif streetSecond[0].isdigit():
            #Flip the two column values
            numStreet = int(re.findall('\d+',streetSecond)[0])
            abcStreet = streetFirst[0]
        else:
            #neigher street has numbers remove the row
            numStreet = 'Remove'
            abcStreet = 'Remove'

        df.loc[x,'STREET'] = numStreet
        df.loc[x,'X_STREET'] = abcStreet
    df.drop_duplicates(inplace = True) #clean up duplicates
    df = df[df['STREET'] !='Remove']
    df = df.reset_index(drop = True)
    #print(df)

    #Combine All the stopsign directions into one row by grouping
    df.ST_FACING = df.ST_FACING.map(lambda x: x.rstrip('B'))
    df.ST_FACING = df.groupby(['STREET','X_STREET'])['ST_FACING'].transform(lambda x: ''.join(x))
    df.drop_duplicates(inplace = True)
    df = df.reset_index(drop = True)

    return df
    #print(df)


#Calculate minimum stops required from pointA to pointB

def minstops(df, start, end, i, j ,direction):
    disH = end[0] - start [0]
    disV = ord(end[1])-ord(start[1])

    if abs(i) > abs(disH) or abs(j) > abs(disV): #out of range
        #print("Out of Range: ",i," ",j)
        return 1000, [100,100]

    #set the general Move direction based on the start and end points
    going = ''
    move = []
    if disH < 0 and disV > 0:
        going = 'ES'
        move = [-1,1]
    elif disH < 0 and disV < 0:
        going = 'EN'
        move = [-1,-1]
    elif disH > 0 and disV > 0:
        going = 'WS'
        move = [1,1]
    elif disH > 0 and disV < 0:
        going = 'WN'
        move = [1,-1]

    #Current Location
    location = start[0] + move[0]*i, chr(ord(start[1]) + move[1]*j)
    #print("Current Location: ",location)

    #Is there a stop sign at this location?
    try:
        stopCorner = df.loc[(df.STREET == location[0]) & (df.X_STREET == location[1]),'ST_FACING'].values[0]
    except IndexError:
        stopCorner = 'none'

    numStop = 0
    #Is there a stopsign at the direction it is coming from?
    if ((direction == 'H') & (going[0] in stopCorner)) | ((direction == 'V') & (going[1] in stopCorner)):
        numStop = 1

    #reached the destination
    if abs(i) == abs(disH) and abs(j) == abs(disV):
        #print("at the end: ",end)
        return numStop, end
    #This corner is nott all way stop - avoid this intersection
    elif numStop == 1 and len(stopCorner) < 4:
        #print("avoid this intersection: ",location)
        return 1000, location

    #Keep going down the recursion
    else:
        #which direction returns less number of stops?
        horizontal = minstops(df, start, end, i+1, j, 'H')
        vertical = minstops(df, start, end, i, j+1, 'V')
        #Passing the pathway in the second parameter

        if horizontal[0] < vertical[0]:
            return numStop + horizontal[0], [location,horizontal[1]]
        else:
            return numStop + vertical[0], [location,vertical[1]]


