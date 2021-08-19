import sys
import PIL
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

#define canvas size
width = 3000
height = 4000
#canvas center
CenterCordWidth = width/2
CenterCordHeight = height/2
#canvas colour (RGB)
canvasColor = (8, 14, 92)
lineColor = (256, 0, 0)
fontSize = 25
starColor = (0,0,0)
#star size (on canvas)
starSize = 100
#scale factor of stars relitv to each other
scaleFactor = 75

#import csv
df = pd.read_csv('starmaps/dataclean.csv')

#create lists for use
df1 = df[['X','Y','Z','spect','proper']]

listOfX = df1['X'].to_list()
listOfY = df1['Y'].to_list()

listOfZ = df1['Z'].to_list()

listOfSpec = df1['spect'].to_list()

listOfNames = df1['proper'].to_list()

listOfX1 = []
listOfY1 = []
xyTop =[]
xyBot = []
x1 = []
x2 = []
y1 = []
y2 = []

starMain = []
starMult = []

starName = []

#setup star colour

for x in listOfSpec:
    y = str(x)

    mC = y[:1]
    mM = y[1:]
        
    if mC == "O":
        starColor = (3, 215, 252)
    elif mC == "B":
        starColor = (56, 226, 232)
    elif mC == "A":
        starColor = (145, 251, 255)
    elif mC == "F":
        starColor = (251, 255, 133)
    elif mC == "G":
        starColor = (248, 255, 31)
    elif mC == "K":
        starColor = (255, 166, 0)
    elif mC == "M":
        starColor = (255, 94, 0)

    starMain.append(starColor)
    starMult.append(mM)

#Loop through x and y coords and multiply be scale factor
for x in listOfX:
    xScale = x * scaleFactor
    listOfX1.append(xScale)

for x in listOfY:
    yScale = x * scaleFactor
    listOfY1.append(yScale)

for x in listOfNames:
    y = str(x)
    starName.append(y)

#halve star size
starSize = starSize/2
#loop through x and y coords to move the orign to center page and offset by the star size
for x in listOfX1:
    absCordXT = CenterCordWidth + x - starSize
    absCordXB = CenterCordWidth + x + starSize

    X1 = absCordXT
    X2 = absCordXB

    x1.append(X1)
    x2.append(X2)

for x in listOfY1:
    absCordYT = CenterCordHeight + x - starSize
    absCordYB = CenterCordHeight + x + starSize

    Y1 = absCordYT
    Y2 = absCordYB

    y1.append(Y1)
    y2.append(Y2)

#add every thing to a dictionary
dictionary = {'x1':x1,'x2':x2,'y1':y1,'y2':y2,"Colour":starMain,"Mult":starMult,"Name":starName}

#create canvas
img = Image.new(mode="RGB", size= (width, height), color= canvasColor)


#setup drawing
with img as im:
    draw = ImageDraw.Draw(im)
    #get fonts
    font_path = "Helvetica.ttf"
    #set up font
    font = ImageFont.truetype(font_path, fontSize)
    #create 2 diagonal lines to assit in finding center
    draw.line((0,0) + im.size, fill=lineColor, width=20)
    draw.line((0, im.size[1], im.size[0], 0), fill=lineColor, width=20)


    #loop through lists drawing each star
    for i in range(len(x1)):
        
        draw.ellipse((x1[i],y1[i],x2[i],y2[i]),fill=starMain[i])
        textoffset = draw.textsize(starName[i], font=font)

        textoffset = str(textoffset)
        textoffset = textoffset[1:]
        textoffset = textoffset[:2]
        textoffset = int(textoffset)
        #print(textoffset)

        draw.text(((x1[i]+starSize-(textoffset-textoffset*0.5) ),y1[i]+(starSize*2)+(0.5*starSize)),starName[i],align="center", font=font, fill=starMain[i])

        #print(x1[i],y1[i],x2[i],y2[i])
        #im.show()

#show canvas
im.show()
#save image
im.save('stellarMap.png')