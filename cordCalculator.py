import pandas as pd
import numpy as np
from pandas._config.config import describe_option

#import data
HygData = pd.read_csv('starmaps/hygdata_v3.csv')
#extract the columns
df1 = HygData[['dec', 'ra', 'dist', 'absmag','proper','gl','spect']]

listOfAbsMag = df1['absmag'].to_list()
listOfProper = df1['proper'].to_list()
listOfGliese = df1['gl'].to_list()
listOfSpectrum = df1['spect'].to_list()

#write data to new csv file
df1.to_csv('starmaps/angles.csv')

#region     Collate data and Conversions

interData = pd.read_csv('starmaps/angles.csv')

dist2 = interData['dist'].to_list()

#convert from decimil time to HH:MM:SS

#region     Create empty lists for later use
declist = []
Hdeclist = []
Mdeclist = []
Sdeclist = []
declist2 = []

ralist = []
Hralist = []
Mralist = []
Sralist = []
ralist2 = []

distList = []

PhiList = []
ThetaList = []
RhoList = []

XList = []
YList = []
ZList = []
RVectList = []

#convert dec and ra to a list
listOfDec = interData['dec'].to_list()
listOfRa = interData['ra'].to_list()

#endregion

#deciml to date time

for x in listOfDec:
    p = x
    if x < 0 :
        time = x * -1

        h = int(time)
        m = (time*60) %  60
        s = (time*3600) % 60

        Tdec = ("-%d:%02d:%02d" % (h, m, s))
        Hdec = -h
        Mdec = m
        Sdec = s
    
    else:
        time = x
        h = int(time)
        m = (time*60) %  60
        s = (time*3600) % 60

        Tdec = ("%d:%02d:%02d" % (h, m, s))
        Hdec = h
        Mdec = m
        Sdec = s

    #print(Tdec)
    declist.append(Tdec)
    Hdeclist.append(Hdec)
    Mdeclist.append(Mdec)
    Sdeclist.append(Sdec)
    declist2.append(p)

for x in listOfRa:
    p = x
    time = x
    h = int(time)
    m = (time*60) %  60
    s = (time*3600) % 60

    Tra = ("%d:%02d:%02d" % (h, m, s))
    Hra = h
    Hra = int(Hra)
    Mra = m
    Mra = int(Mra)
    Sra = s
    Sra = int(Sra)

    #print(Tra)
    ralist.append(Tra)
    Hralist.append(Hra)
    Mralist.append(Mra)
    Sralist.append(Sra)
    ralist2.append(p)

for x in dist2:
    dist = x
    distList.append(dist)

#add every thing to a dictinary
dictionary = {'decdec':declist2,'dec':declist,'Hdec':Hdeclist,'Mdec':Mdeclist,'Sdec':Sdeclist,'radec':ralist2, 'ra': ralist,'Hra':Hralist,'Mra':Mralist,'Sra':Sralist, 'dist':distList}


dataFrame = pd.DataFrame(dictionary)
dataFrame.to_csv('starmaps/finalAngles.csv')

#endregion


#region     Main calculations

#get all the correct data from last step
df = pd.read_csv('starmaps/finalAngles.csv')

#create 3 empty Dataframes for Use
df1 = pd.DataFrame()
df2 = pd.DataFrame()
df3 = pd.DataFrame()

#Find Rho, Phi and Theta
df1['Rho'] = df.apply(lambda row: (row.dist * 3.262), axis = 1)

#df2['Phi'] = df.apply(lambda row: ((row.Hra*15) + (row.Mra*0.25) + (row.Sra*0.0041666))*(np.pi/180), axis = 1)
df2['Phi'] = ralist2 * 15
#df3['Theta'] = df.apply(lambda row: ((abs(row.Hdec) + (row.Mdec/60) + (row.Sdec/3600)*(np.sign(row.Hdec)))*(np.pi/180)), axis = 1)
df3['Theta'] = declist2 

#get all the data into the same dataframe and add it to a new csv file
df1 = df1.join(df2)
df1 = df1.join(df3)
df1.to_csv('starmaps/mapFinale.csv')

#region     Cartisean calculations

#open final csv file calculate RVECT and add it THIS SHOULD BE POSITIVE
df = pd.read_csv('starmaps/mapFinale.csv')
df1['RVECT'] = df.apply(lambda row: (row.Rho * (np.cos((row.Theta)))), axis = 1)
df1.to_csv('starmaps/mapFinale.csv')

#open final csv file calculate X and add it
df = pd.read_csv('starmaps/mapFinale.csv')
df1['X'] = df.apply(lambda row: ((row.RVECT) * (np.cos((row.Phi)))), axis = 1)
df1.to_csv('starmaps/mapFinale.csv')

#open final csv file calculate Y and add it
df = pd.read_csv('starmaps/mapFinale.csv')
df1['Y'] = df.apply(lambda row: ((row.RVECT) * (np.sin((row.Phi)))), axis = 1)
df1.to_csv('starmaps/mapFinale.csv')

#open final csv file calculate Z and add it
df = pd.read_csv('starmaps/mapFinale.csv')
df1['Z'] = df.apply(lambda row: ((row.Rho) * (np.sin((row.Theta)))), axis = 1)
df1.to_csv('starmaps/mapFinale.csv')
#endregion

#endregion

#add extra miscllanious data that did not need to be edited
df = pd.read_csv('starmaps/mapFinale.csv')
dicMag = {'abs mag':listOfAbsMag, 'proper':listOfProper, 'gliese':listOfGliese, 'spect':listOfSpectrum}
df1 = pd.DataFrame(dicMag)
df = df.join(df1)
df.to_csv('starmaps/mapFinale.csv')