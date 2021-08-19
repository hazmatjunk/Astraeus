import sys
import PIL
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont, ImageFilter

#define canvas size
width = 3000
height = 4000
#distance as in dataclean
lyRad = 20
#canvas center
CenterCordWidth = width/2
CenterCordHeight = height/2
#canvas colour (RGB)
canvasColor = (8, 14, 92)
lineColor = (256, 0, 0)
fontSizeTitle = 25
fontSize2 = 20
starColor = (0,0,0)
#star size (on canvas)
starSize = 100
starScale = 0.25
#scale factor of stars relitv to each other
scaleFactor = width/(lyRad*2)
stepCount = lyRad*2

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

#setup star colour p is a testing colour

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

#Loop through x and y coords and multiply be scale factor
for x in listOfX:
    xScale = x * scaleFactor
    listOfX1.append(xScale)

for x in listOfY:
    yScale = x * scaleFactor
    listOfY1.append(yScale)

for x in listOfNames:
    y = str(x)
    y = y.replace('nan','NA')
    #print(y)
    starName.append(y)

#halve star size
starSize = starSize/2

#loop through x and y coords to move the orign to center page and offset by the star size

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

#add every thing to a dictionary
dictionary = {'x1':x1,'x2':x2,'y1':y1,'y2':y2,"Colour":starMain,"Mult":starMult,"Name":starName}

#create canvas
img = Image.new(mode="RGBA", size= (width, height), color= canvasColor)

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



#setup drawing
draw = ImageDraw.Draw(img)
#get fonts
font_path = "Helvetica.ttf"
#set up font
fontTitle = ImageFont.truetype(font_path, fontSizeTitle)
fontW = ImageFont.truetype(font_path, fontSize2)

#create 2 diagonal lines to assit in finding center
#draw.line((0,0) + img.size, fill=lineColor, width=20)
#draw.line((0, img.size[1], img.size[0], 0), fill=lineColor, width=20)

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


#loop through lists drawing each star
for i in range(len(x1)):
    #draw a circle for the star
    draw.ellipse((x1[i]-(crossHairSizeH*4),y1[i]-(crossHairSizeH*4),x2[i]+(crossHairSizeH*4),y2[i]+(crossHairSizeH*4)),fill=canvasColor)


for i in range(len(x1)):
    #use a cross hair
    #replace black areas with star colour
    data[..., :-1][black_areas.T] = starMain[i]
    #apply colour to image
    crossHairColour = Image.fromarray(data)
    
    #add image with transparency
    img.paste(crossHairColour, (x1[i]-crossHairSizeH,y1[i]-crossHairSizeH), crossHairColour)
    

    #find text center
    textoffset = draw.textsize(starName[i], font=fontTitle)
    textoffset = str(textoffset)
    textoffset = textoffset[1:]
    textoffset = textoffset[:3]
    textoffset = textoffset.rstrip(',')
    textoffset = int(textoffset)*0.5

    draw.text(((x1[i]+(crossHairSizeH)+(crossHairSizeH*0.5)), y1[i]-(crossHairSizeH)), starName[i],align="center", font=fontTitle, fill=(0,0,0))

    #print(x1[i],y1[i],x2[i],y2[i])
    #im.show()

#show canvas
img.show()
#save image
img.save('stellarMap.png')