import pandas as pd
import os
import os.path
import urllib.request
import gzip
import shutil
from pandas._config.config import describe_option

#Collate data and Conversions

#max range from earth
distanceFromEarth = 20

#get hygdata
if os.path.isfile('starmaps/hygdata_v3.csv') == True:
    print("We have Light")
else:
    print("We need light. Starting big bang")
    urllib.request.urlretrieve("http://astronexus.com/downloads/catalogs/hygdata_v3.csv.gz", "starmaps/hygdata_v3.csv.gz")
    with gzip.open('starmaps/hygdata_v3.csv.gz','rb') as f_in:
        with open('starmaps/hygdata_v3.csv', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    os.remove('starmaps/hygdata_v3.csv.gz')
    print("Big Bang complete")

import functionsStellar as fs

if os.path.isfile('starmaps/mapFinale.csv') == True:
    print("file already here")
else:
    #import data
    HygData = pd.read_csv('starmaps/hygdata_v3.csv')
    #extract the columns
    df1 = HygData[['dec', 'ra', 'dist', 'absmag','proper','gl','spect']]

    #Create lists for later use

    listOfAbsMag = df1['absmag'].to_list()
    listOfProper = df1['proper'].to_list()
    listOfGliese = df1['gl'].to_list()
    listOfSpectrum = df1['spect'].to_list()

    #deciml to date time and add every thing to a dictinary

    fs.dictUpdate()

    #Main calculations

    fs.RhoPhiTheta()

    #Cartisean calculations

    fs.RVECTXYZ()

    #remove temp files
    os.remove("starmaps/finalangles.csv")

    #add extra miscllanious data that did not need to be edited
    df = pd.read_csv('starmaps/mapFinale.csv')
    dicMag = {'abs mag':listOfAbsMag, 'proper':listOfProper, 'gliese':listOfGliese, 'spect':listOfSpectrum}
    df1 = pd.DataFrame(dicMag)
    df = df.join(df1)
    df.to_csv('starmaps/mapFinale.csv')

    datafinal = pd.read_csv('starmaps/mapFinale.csv')
    fs.unusedClean(x=datafinal)

    print("file created")

#dataCleanup second
#data File to clean

fs.distaneClean(x=distanceFromEarth)

fs.spectraClean()

fs.nameMerge()

fs.emptyFill()

cleandata = pd.read_csv('starmaps/dataclean.csv')
fs.unusedClean(x=cleandata)