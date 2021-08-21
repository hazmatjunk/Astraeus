import pandas as pd
import numpy as np
from scipy.spatial import distance
from PIL import Image, ImageDraw
import os
from random import randrange

#layout functions below
#import data

df = pd.read_csv('starmaps/dataclean.csv')

#create list
df1 = df[['X','Y','Z','spect','proper']]

def spectraSetUp():

    listOfSpec = df1['spect'].to_list()

    starMain = []
    starMult = []

    for x in listOfSpec:
        y = str(x)

        mC = y[:1]
        mM = y[1:]
            
        if mC == "O":
            starColor = (94, 128, 255)
        elif mC == "B":
            starColor = (130, 161, 255)
        elif mC == "A":
            starColor = (156, 180, 255)
        elif mC == "F":
            starColor = (233, 230, 255)
        elif mC == "G":
            starColor = (245, 197, 42)
        elif mC == "K":
            starColor = (255, 162, 48)
        elif mC == "M":
            starColor = (255, 72, 0)
        elif mC == "P":
            starColor = (0, 255, 0)

        starMain.append(starColor)
        starMult.append(mM)
    print("We have colour")
    return(starMain)

def xSetup(scaleFactor, CenterCordWidth, starSize):
    listOfX = df1['X'].to_list()
    listOfX1 = []

    x1 = []
    x2 = []

    for x in listOfX:
        xScale = x * scaleFactor
        listOfX1.append(xScale)

    for x in listOfX1:
        absCordXT = CenterCordWidth + x - starSize
        absCordXB = CenterCordWidth + x + starSize

        absCordXT = CenterCordWidth + x
        absCordXB = CenterCordWidth + x

        X1 = absCordXT
        X2 = absCordXB

        X1 = int(X1)
        X2 = int(X2)

        x1.append(X1)
        x2.append(X2)
    print("Thats X")
    return(x1,x2)

def ySetup(scaleFactor, CenterCordHeight, starSize):
    listOfY = df1['Y'].to_list()
    listOfY1 = []

    y1 = []
    y2 = []

    for x in listOfY:
        yScale = x * scaleFactor
        listOfY1.append(yScale)

    for x in listOfY1:
        absCordYT = CenterCordHeight + x - starSize
        absCordYB = CenterCordHeight + x + starSize

        absCordYT = CenterCordHeight + x
        absCordYB = CenterCordHeight + x

        Y1 = absCordYT
        Y2 = absCordYB

        Y1 = int(Y1)
        Y2 = int(Y2)

        y1.append(Y1)
        y2.append(Y2)
    print("and thats Y")
    return(y1, y2)

def textSetup():
    listOfNames = df1['proper'].to_list()
    starName = []
    listOfSpectra = df1['spect'].to_list()
    starSpect = []
    listOfCoordX = df1['X'].to_list()
    starX = []
    listOfCoordY = df1['Y'].to_list()
    starY = []
    listOfCoordZ = df1['Z'].to_list()
    starZ = []

    for x in listOfNames:
        y = str(x)
        y = y.replace('nan','NA')
        #print(y)
        starName.append(y)
    
    for x in listOfSpectra:
        y = str(x)
        #print(y)
        starSpect.append(y)

    for x in listOfCoordX:
        y = float(x)
        y = round(y,2)
        y = str(y)
        #print(y)
        starX.append(y)

    for x in listOfCoordY:
        y = float(x)
        y = round(y,2)
        y = str(y)
        #print(y)
        starY.append(y)

    for x in listOfCoordZ:
        y = float(x)
        y = round(y,2)
        y = str(y)
        #print(y)
        starZ.append(y)
    
    print("You have a Name and you have a name")
    return(starName,starSpect,starX,starY,starZ)

def canvasSetup(x, y,Color):

    #create canvas
    img = Image.new(mode="RGBA", size= (x, y), color= Color)
    #setup drawing
    draw = ImageDraw.Draw(img)
    print("oh look a block of colour")
    return(img)

def drawSetup(img):
    #setup drawing
    draw = ImageDraw.Draw(img)
    print("draw tools enabled")
    return(draw)

def crosshairSetup(starScale):
    #import crosshair
    crossHair = Image.open('data/starCrosshair.gif')
    crossHairMask = Image.open('data/starCrosshairMask.gif')
    crossHair = crossHair.convert("RGBA")

    #image scale
    crossHair = crossHair.resize((round(crossHair.size[0]*starScale),round(crossHair.size[0]*starScale)))
    crossHairSizeH,crossHairSizeW = crossHair.size
    crossHairSizeH = int(crossHairSizeH/2)
    crossHairSizeW = int(crossHairSizeW/2)
    #print(crossHairSizeH,crossHairSizeW)

    #set up colour manipulation of the crosshair
    data = np.array(crossHair)
    red, green, blue, alpha = data.T
    black_areas = (red == 0) & (blue == 0) & (green == 0)

    print("lined up in my crosshairs")
    return(crossHairSizeH,crossHairSizeW,data,black_areas)

def gridCreation(img,draw,stepCount,lineColor):
    #create grid
    #draw lines
    yStart = 0
    yEnd = img.height
    stepSize = int(img.width/stepCount)

    for x in range(0, img.width, stepSize):
        line = ((x, yStart), (x, yEnd))
        draw.line(line, fill=128)

    xStart = 0
    xEnd = img.width

    for y in range(0, img.height, stepSize):
        line = ((xStart, y + img.height/2), (xEnd, y + img.height/2))
        draw.line(line, fill= 128)

    for y in range(0, img.height, stepSize):
        line = ((xStart, img.height/2 - y), (xEnd, img.height/2 - y))
        draw.line(line, fill= 128)

    #draw line on up down going through 0,0
    draw.line((img.width/2,0,img.width/2,img.height), fill= lineColor, width= 10)
    #draw line going left right 0,0
    draw.line((0,img.height/2,img.width,img.height/2), fill= lineColor, width= 10)    
    print("Grid Loaded")

def textOffSetX(draw, starName, fontTitle , i):
    textoffset = draw.textsize(starName[i], font=fontTitle)
    textoffset = str(textoffset)
    textoffset = textoffset[1:]
    textoffset = textoffset[:3]
    textoffset = textoffset.rstrip(',')
    textoffset = int(textoffset)
    return(textoffset)

def textOffSetY(draw, starName, fontTitle , i):
    textoffset = draw.textsize(starName[i], font=fontTitle)
    textoffset = str(textoffset)
    textoffsety = textoffset
    textoffsety = textoffsety.rstrip(')')
    textoffsety = textoffsety[4:]
    textoffsety = textoffsety.lstrip(',')
    textoffsety = int(textoffsety)
    return(textoffsety)

def drawStarBackground(draw, x1, y1,x2 ,y2, crossHairSizeH,starName, canvasColor, fontTitle):
    #loop through lists drawing each star
    for i in range(len(x1)):
        #draw a circle for the star background
        draw.ellipse((x1[i]-(crossHairSizeH*4),y1[i]-(crossHairSizeH*4),x2[i]+(crossHairSizeH*4),y2[i]+(crossHairSizeH*4)),fill=canvasColor)

        textoffset = textOffSetX(draw= draw, starName= starName, fontTitle= fontTitle, i= i)
        textoffsety = textOffSetY(draw= draw, starName= starName, fontTitle= fontTitle, i= i)
        #draw a rectangle behind the text
        draw.rectangle((x1[i]+(crossHairSizeH)+(crossHairSizeH*0.5), y1[i]-(crossHairSizeH),x2[i]+(crossHairSizeH)+(crossHairSizeH*0.5)+textoffset,y2[i]+textoffsety), fill=canvasColor)
    print("so little stars")

def drawStarText (img,draw,data,black_areas,x1,y1,starMain,crossHairSizeH,starName,fontTitle,starSpect,starX,starY,starZ):

    g = 0

    for i in range(len(x1)):
        #use a cross hair
        #replace black areas with star colour
        data[..., :-1][black_areas.T] = starMain[i]
        #apply colour to image
        crossHairColour = Image.fromarray(data)
        
        #add image with transparency
        img.paste(crossHairColour, (x1[i]-crossHairSizeH,y1[i]-crossHairSizeH), crossHairColour)

        text = starName[g] + '\n' + 'Spect: ' + starSpect[g] + '\n' + 'X: ' + starX[g] + 'Y: ' + starY[g] + 'Z: ' + starZ[g]
        #write text with name  + starX[i] + starY[i] + starY[i] + starZ[i]
        draw.multiline_text(((x1[i]+(crossHairSizeH)+(crossHairSizeH*0.5)), y1[i]-(crossHairSizeH)), text ,align="center", font=fontTitle, fill=(0,0,0))

        g = g + 1

    print("there are the stars... Hey they are labled")

def findNeighbours(scaleFactor,widthHalf,heightHalf,draw,lineWidth):

    df = pd.read_csv('starmaps/dataclean.csv')
    print("found data frame")

    #get x,y,z values
    df1 = df[['X', 'Y', 'Z']]

    #add x y z to new file
    df1.to_csv('yes.csv')
    df1 = pd.read_csv('yes.csv')
    #set up index
    df1['Key1'] = df1.index
    #df1.set_index('Unnamed: 0')

    #create test folder
    isPath = os.path.exists('test')
    if not isPath:
        os.makedirs('test')

    print("test directory created")


    df1 = df1.astype(np.float64)
    df1.to_csv('yes.csv')
    df1 = pd.read_csv('yes.csv')

    df2 = pd.read_csv('yes.csv')

    index = df['index'].tolist()
    xyzArray = df2[['X', 'Y', 'Z']].to_numpy()

    #find length relitive to every other star

    for i in index:
        #print(df2)
        x = df2.iloc[[i]]
        x = df2.iloc[:,1:]
        c = distance.cdist(xyzArray,xyzArray, 'euclidean')

    dataFrame = pd.DataFrame(c)
    dataFrame.to_csv('yea.csv')
    df = pd.read_csv('yea.csv')

    x = []

    g = 0

    for i in index:
        filename = 'test/'+str(g)+'.csv'
        g = g+1

        #divide into rows
        x = df
        x = df.iloc[i:i+1,1:]
        
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

    Name = 0

    for i in index:
        filename = 'test/'+str(Name)+'.csv'
        df = pd.read_csv(filename)

        XstarOrigin = df['X'].iat[0]
        XstarOrigin = (XstarOrigin * scaleFactor) + widthHalf
        YstarOrigin = df['Y'].iat[0]
        YstarOrigin = (YstarOrigin * scaleFactor) + heightHalf
        #ZstarOrigin = df['Z'].iat[0]

        Xstar1 = df['X'].iat[1]
        Xstar1 = (Xstar1 * scaleFactor) + widthHalf
        Ystar1 = df['Y'].iat[1]
        Ystar1 = (Ystar1 * scaleFactor) + heightHalf

        Xstar2 = df['X'].iat[2]
        Xstar2 = (Xstar2 * scaleFactor) + widthHalf
        Ystar2 = df['Y'].iat[2]
        Ystar2 = (Ystar2 * scaleFactor) + heightHalf

        Xstar3 = df['X'].iat[3]
        Xstar3 = (Xstar3 * scaleFactor) + widthHalf
        Ystar3 = df['Y'].iat[3]
        Ystar3 = (Ystar3 * scaleFactor) + heightHalf

        #print(XstarOrigin,Xstar1,Xstar2,Xstar3)
        #print(YstarOrigin,Ystar1,Ystar2,Ystar3)

        #draw.line([(XstarOrigin,YstarOrigin),(Xstar1,Ystar1)],fill= lineColor,width=20)
        draw.line([(XstarOrigin,YstarOrigin),(Xstar2,Ystar2)],fill= (randrange(100,256),randrange(100,256),randrange(100,256)),width=(int(lineWidth/2)))
        draw.line([(XstarOrigin,YstarOrigin),(Xstar3,Ystar3)],fill= (randrange(100,256),randrange(100,256),randrange(100,256)),width=(int(lineWidth/2)))

        os.remove('test/'+str(Name)+'.csv')
        Name = Name+1
    os.removedirs('test')
    os.remove("yea.csv")
    os.remove("yes.csv")
