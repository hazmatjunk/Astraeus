import pandas as pd
import numpy as np
from PIL import Image, ImageDraw

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

def nameSetup():
    listOfNames = df1['proper'].to_list()
    starName = []

    for x in listOfNames:
        y = str(x)
        y = y.replace('nan','NA')
        #print(y)
        starName.append(y)
    print("You have a Name and you have a name")
    #print(starName)
    return(starName)

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

def drawStarText (img,draw,data,black_areas,x1,y1,starMain,crossHairSizeH,starName,fontTitle):

    for i in range(len(x1)):
        #use a cross hair
        #replace black areas with star colour
        data[..., :-1][black_areas.T] = starMain[i]
        #apply colour to image
        crossHairColour = Image.fromarray(data)
        
        #add image with transparency
        img.paste(crossHairColour, (x1[i]-crossHairSizeH,y1[i]-crossHairSizeH), crossHairColour)


        #write text with name
        draw.text(((x1[i]+(crossHairSizeH)+(crossHairSizeH*0.5)), y1[i]-(crossHairSizeH)), starName[i],align="center", font=fontTitle, fill=(0,0,0))
    print("there are the stars... Hey they are labled")