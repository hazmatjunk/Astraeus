from numpy.lib import emath
from numpy.lib.utils import source
import pandas as pd
import numpy as np
from scipy.spatial import distance
import os, glob
from PIL import Image, ImageDraw
import layoutFunctions as lf

df = pd.read_csv('starmaps/dataclean.csv')
print("found data frame")
#get x,y,z values
df1 = df[['X', 'Y', 'Z']]
df1.to_csv('yes.csv')
df1 = pd.read_csv('yes.csv')
#set up index
df1['Key1'] = df1.index
#df1.set_index('Unnamed: 0')
isPath = os.path.exists('test')
if not isPath:
    os.makedirs('test')

print(df1.index)
print(df1.columns)

df1 = df1.astype(np.float64)
df1.to_csv('yes.csv')
df1 = pd.read_csv('yes.csv')

df2 = pd.read_csv('yes.csv')

index = df['index'].tolist()
xyzArray = df2[['X', 'Y', 'Z']].to_numpy()
xyzdict = df2[['X', 'Y', 'Z']].to_dict()
xl = df['X']
yl = df['Y']
zl = df['Z']


#find length relitive to every other star

for i in index:
    x = df2.iloc[[i]]
    x = df2.iloc[:,1:]
    #print(x)
    #x = np.array(x)
    #x = np.array((x,y,z))
    c = distance.cdist(xyzArray,xyzArray, 'euclidean')
    #print(c)
    

dataFrame = pd.DataFrame(c)
dataFrame.to_csv('yea.csv')
df = pd.read_csv('yea.csv')

Start = []
dist = []
x = []
y = []
z = []

g = 0

#divide every table into every row and add xyz for coord
for i in index:
    filename = 'test/'+str(g)+'.csv'
    g = g+1

    #divide into rows
    x = df
    x = df.iloc[i:i+1,1:]
    
    #x = df.iloc[:,1:]
    
    #replace all 0's with large number
    #replace0 = x.replace(0,50)
    
    #get 4 min values and transpose table
    t = x.sort_values(by = [i],axis=1)
    t = t.iloc[:,:4]
    Tv = t.T
    Tv['dist'] = Tv
    Tv['Key1'] = Tv.index
    #Tv['key2'] = Tv.index

    #turn every thing to string
    Tv = Tv.astype(np.float64)

    #merge by index to give x y z values
    DataMerged = pd.merge(df1,Tv, on=['Key1'],how='inner')

    StartCol = DataMerged['Key1']
    distCol = DataMerged['dist']
    xCol = DataMerged['X']
    yCol = DataMerged['Y']
    zCol = DataMerged['Z']

    dataFinal = pd.concat([StartCol,distCol,xCol,yCol,zCol],axis=1)
    dataFinal = dataFinal.set_axis(['starKey','dist','X','Y','Z'],axis=1)

    #save as individual csv's
    dataFrame = pd.DataFrame(dataFinal)
    dataFrame.to_csv(filename)


#get x y z of origin star and draw line to next two
canvasColor = (8, 14, 92)
img = lf.canvasSetup(x= 3000, y= 4000,Color= canvasColor)
#setup draw
draw = lf.drawSetup(img= img)

Name = 0

for i in index:
    filename = 'test/'+str(Name)+'.csv'
    Name = Name+1
    df = pd.read_csv(filename)

    Xstar = df['X'].iloc[2]

    print(Xstar)



#show canvas
img.show()
#save image
img.save('stellarMapDistance.png')




#concat all csvfiles
os.chdir(r"C:\Users\Harry\Desktop\programming\Astraeus\test")

extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

#combine all files in the list
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
#export to csv
os.chdir(r"C:\Users\Harry\Desktop\programming\Astraeus")
combined_csv.to_csv( "combined_csv.csv", index=False, encoding='utf-8-sig')
