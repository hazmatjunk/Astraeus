from numpy.lib.function_base import append
import pandas as pd
import numpy as np

#clean out distance greater than 20 ly
df = pd.read_csv('starmaps/mapFinale.csv')

print(df.shape)

df2 = df.loc[df["Rho"] <= 20]

print(df2.shape)

df2.to_csv('starmaps/dataclean.csv')

#clean out abs mag greater than 5

#delet unanmed misc columns

df = pd.read_csv('starmaps/dataclean.csv')
print(df.shape)
df2 = df.drop(columns=["Unnamed: 0","Unnamed: 0.1","Unnamed: 0.1.1"])
print(df2.shape)
df2.to_csv('starmaps/dataclean.csv')

df = pd.read_csv('starmaps/dataclean.csv')
df2.spect = df.spect.fillna('NULL')
df2.to_csv('starmaps/dataclean.csv')

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

    print(list(d))
    cleanedSpec.append(d)

dict = {'spect':cleanedSpec}

df = df.drop(columns=["spect"])

df1 = pd.DataFrame(dict)
df = df.join(df1)
df.to_csv('starmaps/dataclean.csv')


#merger gliese and proper names
df = pd.read_csv('starmaps/dataclean.csv')

df.proper = np.where(df.proper.isnull(),df.gliese, df.proper)

df.to_csv('starmaps/dataclean.csv')