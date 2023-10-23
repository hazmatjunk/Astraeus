import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import os
import os.path
import urllib.request
import gzip
import shutil
from pandas._config.config import describe_option
from pandas.core.indexes.base import Index

#Collate data and Conversions

#max range from earth
distanceFromEarth = 20
#rotat data set by this value
raRot = 30
decRot = 0
#set up worksapce
if os.path.isfile('starmaps/hygdata_v3.csv') == True:
    print("We have Light")
else:
    print("We need light. Starting big bang")
    #check to see if starmaps exists and create if it dosent exist
    isPath = os.path.exists('starmaps')
    if not isPath:
        os.makedirs('starmaps')
    #download Hygdata
    urllib.request.urlretrieve("http://astronexus.com/downloads/catalogs/hygdata_v3.csv.gz", "starmaps/hygdata_v3.csv.gz")
    #extract hygdata
    with gzip.open('starmaps/hygdata_v3.csv.gz','rb') as f_in:
        with open('starmaps/hygdata_v3.csv', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    #clean up workspace
    os.remove('starmaps/hygdata_v3.csv.gz')
    print("Big Bang complete")


import dataFunctions as ds

if os.path.isfile('starmaps/dataclean1.csv') == True:
    print("file already here")
else:
    #import data
    HygData = pd.read_csv('starmaps/hygdata_v3.csv')
    #extract the columns
    df1 = HygData[['dec', 'ra', 'dist', 'absmag','proper','gl','spect','hd']]

    #Create lists for later use

    listOfAbsMag = df1['absmag'].to_list()
    listOfProper = df1['proper'].to_list()
    listOfGliese = df1['gl'].to_list()
    listOfSpectrum = df1['spect'].to_list()
    listOfHd = df1['hd'].to_list()


    #find closest stars in designated range


    #deciml to date time and add every thing to a dictinary

    ds.dictUpdate(raRotDec= raRot, decRotDec= decRot)
    ds.dictUpdate(raRotDec= raRot, decRotDec= decRot)

    #clean out distance greater than 20 ly
    #ds.distaneClean(x=distanceFromEarth)
    #Main calculations

    ds.RhoPhiTheta()

    #Cartisean calculations

    ds.RVECTXYZ()

    #remove temp files
    #os.remove("starmaps/finalangles.csv")

    #add extra miscllanious data that did not need to be edited
    df = pd.read_csv('starmaps/mapFinale.csv')
    dicMag = {'abs mag':listOfAbsMag, 'proper':listOfProper, 'gliese':listOfGliese,'hd':listOfHd, 'spect':listOfSpectrum}
    df1 = pd.DataFrame(dicMag)
    df = df.join(df1)
    df.to_csv('starmaps/mapFinale.csv')

    datafinal = pd.read_csv('starmaps/mapFinale.csv')
    ds.unusedClean(x=datafinal)

    print("file created")

#dataCleanup second
#data File to clean

#cleaned up everything and move final stuff to dataclean
ds.spectraClean()

ds.nameMerge()

ds.emptyFill()

ds.distanceCleaner2(x=distanceFromEarth)

os.remove("starmaps/mapFinale.csv")

ds.removeDuplicates()

df = pd.read_csv('starmaps/dataclean.csv')
df.insert(loc= 0, column='index', value=np.arange(len(df)))
df.to_csv('starmaps/dataclean.csv')

cleandata = pd.read_csv('starmaps/dataclean.csv')

cleandata = cleandata.drop(['gliese','hd'],axis=1)

ds.unusedClean(x=cleandata)

print("Data modified and cleaned!")

#preper 3d plot of all stars in range

print("Starting Univers Expansion")
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
print("Expansion complete")


#read in and assign varibles from the cleaned data
df = pd.read_csv('starmaps\dataclean.csv')

PropName = df['proper']
XList = df['X']
YList = df['Y']
ZList = df['Z']

listOfSpec = df['spect'].to_list()

starMain = []
starMult = []
print("COlouring Between the lines")
for x in listOfSpec:
    y = str(x)

    mC = y[:1]
    mM = y[1:]
        
    if mC == "O":
        starColor = (94/255, 128/255, 1)
    elif mC == "B":
        starColor = (130/255, 161/255, 1)
    elif mC == "A":
        starColor = (156/255, 180/255, 1)
    elif mC == "F":
        starColor = (233/255, 230/255, 1)
    elif mC == "G":
        starColor = (245/255, 197/255, 42/255)
    elif mC == "K":
        starColor = (1, 162/255, 48/255)
    elif mC == "M":
        starColor = (1, 72/255, 0)
    elif mC == "P":
        starColor = (0, 1, 0)

    starMain.append(starColor)
    starMult.append(mM)

print("Colouring complete")

ax.scatter(XList, YList, ZList, color = starMain)
print("The matter has condensed, FUSION!!")

ax.set_xlabel('X (Light Years)')
ax.set_ylabel('Y (Light Years)')
ax.set_zlabel('Z (Light Years)')
ax.text(0,0,0, s="Sol")
radText = "outer Radius (Ly): " + str(distanceFromEarth)
ax.text(distanceFromEarth,0,0, s=radText)
#ax.text(XList,YList,ZList,PropName)

plt.show()