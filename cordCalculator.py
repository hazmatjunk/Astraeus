import pandas as pd
import numpy as np
import os
import os.path
import urllib.request
import gzip
import shutil
import zipfile
from pandas._config.config import describe_option
from pandas.core.indexes.base import Index

#Collate data and Conversions

#max range from earth
distanceFromEarth = 20

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

if os.path.isfile('Helvetica.ttf') == True:
        print("We have Ink")
else:
    print("We need ink. Starting squids")
    urllib.request.urlretrieve("https://dl.freefontsfamily.com/download/Helvetica-Font", "HelveticaFont.zip")
    with zipfile.ZipFile('HelveticaFont.zip', 'r') as zip_ref:
        zip_ref.extractall('')
    os.remove('Helvetica-Bold.ttf')
    os.remove('Helvetica-BoldOblique.ttf')
    os.remove('helvetica-compressed-5871d14b6903a.otf')
    os.remove('helvetica-light-587ebe5a59211.ttf')
    os.remove('Helvetica-Oblique.ttf')
    os.remove('helvetica-rounded-bold-5871d05ead8de.otf')
    os.remove('HelveticaFont.zip')

#https://dl.freefontsfamily.com/download/Helvetica-Font

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

    ds.dictUpdate()

    #clean out distance greater than 20 ly
    #ds.distaneClean(x=distanceFromEarth)
    #Main calculations

    ds.RhoPhiTheta()

    #Cartisean calculations

    ds.RVECTXYZ()

    #remove temp files
    os.remove("starmaps/finalangles.csv")

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

df = pd.read_csv('starmaps/dataclean.csv')
df.insert(loc= 0, column='index', value=np.arange(len(df)))
df.to_csv('starmaps/dataclean.csv')

ds.distanceCleaner2(x=distanceFromEarth)

cleandata = pd.read_csv('starmaps/dataclean.csv')

ds.unusedClean(x=cleandata)

print(cleandata.shape)

os.remove("starmaps/mapFinale.csv")

ds.removeDuplicates()

print("Data modified and cleaned!")