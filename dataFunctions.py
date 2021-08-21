import pandas as pd
import numpy as np

#import data
HygData = pd.read_csv('starmaps/hygdata_v3.csv')
#extract the columns
df1 = HygData[['dec', 'ra', 'dist', 'absmag','proper','gl','spect']]


def decimilDateTimeDEC(decRotDec):

    listOfDec = HygData['dec'].to_list()

    declist = []
    Hdeclist = []
    Mdeclist = []
    Sdeclist = []
    declist2 = []

    for x in listOfDec:
        x = x + decRotDec
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
        declist2.append(x)
    
    decDict = {'decdec':declist2,'dec':declist,'Hdec':Hdeclist,'Mdec':Mdeclist,'Sdec':Sdeclist,}
    print("Decimal date time found for declination")
    return(decDict)

def decimilDateTimeRA(raRotDec):

    listOfRa = HygData['ra'].to_list()

    ralist = []
    Hralist = []
    Mralist = []
    Sralist = []
    ralist2 = []

    for x in listOfRa:
        p = x
        p = p + raRotDec
        time = p
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

    raDict = {'radec':ralist2, 'ra': ralist,'Hra':Hralist,'Mra':Mralist,'Sra':Sralist}

    print("Decimal date time found for right acension")

    return(raDict)

def distConverter():

    dist = HygData['dist'].to_list()

    distList = []

    for x in dist:
        dist = x
        distList.append(dist)

    distDict = {'dist':distList}

    print("Distance converted")

    return(distDict)

def dictUpdate(raRotDec,decRotDec):
    dictionary = {}
    dictionary.update(decimilDateTimeDEC(decRotDec))
    dictionary.update(decimilDateTimeRA(raRotDec))
    dictionary.update(distConverter())

    dataFrame = pd.DataFrame(dictionary)
    dataFrame.to_csv('starmaps/finalAngles.csv')

    print("Dictionarys updated")

    df1 = pd.read_csv('starmaps/finalAngles.csv')
    print("This is the data size ", df1.shape)
    df2 = df1.loc[df1["dist"] <= (20 * 3.262) ]
    print("This is the new data size ", df2.shape)
    print("Distance cleaned 1")
    
    #modify all ra by global roation

    df2.to_csv('starmaps/finalAngles.csv')

    return(dictionary)

def RhoPhiTheta():

    df = pd.read_csv('starmaps/finalAngles.csv')

    Rho = pd.DataFrame()
    Phi = pd.DataFrame()
    Theta = pd.DataFrame()

    Rho['Rho'] = df.apply(lambda row: (row.dist * 3.262), axis = 1)

    print("Rho found")

    ra1 = df['radec'].to_list()
    dec1 = df['decdec'].to_list()

    Phi['Phi'] = ra1 * 15
    print("Phi found")

    Theta['Theta'] = dec1
    print("Theta found")

    #get all the data into the same dataframe and add it to a new csv file
    #print(Rho)
    df["Rho"]=Rho
    df.to_csv('starmaps/mapFinale.csv')
    df["Phi"]=Phi
    df.to_csv('starmaps/mapFinale.csv')
    df["Theta"]=Theta
    df.to_csv('starmaps/mapFinale.csv')
    print("Rho, Phi and Theta added to csv found")

def RVECTXYZ():
    #open final csv file calculate RVECT and add it THIS SHOULD BE POSITIVE
    df = pd.read_csv('starmaps/mapFinale.csv')
    df['RVECT'] = df.apply(lambda row: (row.Rho * (np.cos((row.Theta)))), axis = 1)
    df.to_csv('starmaps/mapFinale.csv')
    print("RVECT found")

    #open final csv file calculate X and add it
    df = pd.read_csv('starmaps/mapFinale.csv')
    df['X'] = df.apply(lambda row: ((row.RVECT) * (np.cos((row.Phi)))), axis = 1)
    df.to_csv('starmaps/mapFinale.csv')
    print("X found")

    #open final csv file calculate Y and add it
    df = pd.read_csv('starmaps/mapFinale.csv')
    df['Y'] = df.apply(lambda row: ((row.RVECT) * (np.sin((row.Phi)))), axis = 1)
    df.to_csv('starmaps/mapFinale.csv')
    print("Y found")

    #open final csv file calculate Z and add it
    df = pd.read_csv('starmaps/mapFinale.csv')
    df['Z'] = df.apply(lambda row: ((row.Rho) * (np.sin((row.Theta)))), axis = 1)
    df.to_csv('starmaps/mapFinale.csv')
    print("Z found")

def distanceCleaner2(x):
    df = pd.read_csv('starmaps/dataclean.csv')
    print(df.shape)
    df2 = df.loc[df["Rho"] <= x]
    print(df2.shape)
    df2.to_csv('starmaps/dataclean.csv')

def unusedClean(x):
    df = x
    df = df[df.columns.drop(list(df.filter(regex='Unnamed:')))]
    #df = df.drop(columns=["Unnamed: 0"])
    #df = df.iloc[:,1:]
    df.to_csv('starmaps/dataclean.csv')
    print("datacleaned")

def emptyFill():
    #fill emptyies with null
    df = pd.read_csv('starmaps/dataclean.csv')
    df.spect = df.spect.fillna('NULL')
    df.to_csv('starmaps/dataclean.csv')
    print("NULL voided")

def spectraClean():
    #get spectra in easy to use

    df = pd.read_csv('starmaps/dataclean.csv')

    pecu = [":","...","!","comp","e","[e]","er","eq","f","f*","f+","(f)","(f+)","((f))","((f*))","h","ha","He wk","k","m",'n',"nn","neb","p","pq","q","s","ss","sh","var","wl","J","S","b","Sd","d","D"]
    lumClass = ["0","Ia+","Ia","Iab","Ib","II","III","IV","VI","VII","I","V"]
    subSpec = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 4.0, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 5.0, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8, 5.9, 6.0, 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8, 6.9, 7.0, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9, 8.0, 8.1, 8.2, 8.3, 8.4, 8.5, 8.6, 8.7, 8.8, 8.9, 9.0, 9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 9.7, 9.8, 9.9]
    mainClass = ['O','B','A','F','G','K','M']


    listOfSpec = df['spect'].to_list()

    cleanedSpec = []

    for x in listOfSpec:
        y = str(x)
        pecu = str(pecu)
        lumClass = str(lumClass)

        y = y.strip(pecu)

        d = y[:2]

        #print(list(d))
        cleanedSpec.append(d)

    dict = {'spect':cleanedSpec}

    df = df.drop(columns=["spect"])

    df1 = pd.DataFrame(dict)
    df = df.join(df1)
    df.to_csv('starmaps/dataclean.csv')
    print("Spectra cleaned")

def nameMerge():
    df = pd.read_csv('starmaps/dataclean.csv')
    df.proper = np.where(df.proper.isnull(),df.gliese, df.proper)
    df.proper = np.where(df.proper.isnull(),df.hd, df.proper)
    df.to_csv('starmaps/dataclean.csv')
    print("Names Merged")

def removeDuplicates():
    df = pd.read_csv('starmaps/dataclean.csv')
    print(df.shape)
    df.sort_values('Rho', ascending=True,inplace=True)
    df = df.drop_duplicates('Rho',keep= 'first')
    df = df.dropna(subset=['proper'],axis=0)
    print(df.shape)

    #for i in range(len(df)):
        #df = pd.read_csv('starmaps/dataclean.csv')

        #tNum = [(df['X'].iloc[i])]
        #print(tNum)
        #tNum = str(tNum)
        #tNum = tNum.strip("[]")
        #tNum = float(tNum)

        #bNum = [(df['X'].iloc[i])]
        #print(bNum)
        #bNum = str(bNum)
        #bNum = bNum.strip("[]")
        #bNum = float(bNum)

        #df = df[~df.iloc[:, 16].between(bNum,tNum,inclusive=False)]
        #df.to_csv('starmaps/dataclean.csv')

    df.to_csv('starmaps/dataclean.csv')
    print("Duplicates Dropped")