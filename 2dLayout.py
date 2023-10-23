import layoutFunctions as ls
import pandas as pd
from PIL import ImageFont

#define canvas size
width = 5000
height = 5000
#distance as in dataclean
lyRad = 20
#canvas center
CenterCordWidth = width/2
CenterCordHeight = height/2
#canvas colour (RGB)
canvasColor = (8, 14, 92)
lineColor = (256, 0, 0)
lineColor2 = (256, 256, 256)
fontSizeTitle = 25
fontSize2 = 20
starColor = (0,0,0)
#star size (on canvas)
starSize = 100
starScale = 0.5
#scale factor of stars relitv to each other
scaleFactor = width/(lyRad*2)
stepCount = lyRad*2

lineWidth = int(width/(starSize*2))

print(lineWidth)

#import csv
df = pd.read_csv('starmaps/dataclean.csv')

#create lists for use
df1 = df[['Z']]

listOfZ = df1['Z'].to_list()

#setup star colour p is a testing colour
starMain = ls.spectraSetUp()
#to change later
starMult = ls.spectraSetUp()

#Loop through x and y coords and multiply be scale factor
x1 = ls.xSetup(scaleFactor= scaleFactor, CenterCordWidth= CenterCordWidth, starSize= starSize)[0]
x2 = ls.xSetup(scaleFactor= scaleFactor, CenterCordWidth= CenterCordWidth, starSize= starSize)[1]

y1 = ls.ySetup(scaleFactor= scaleFactor, CenterCordHeight= CenterCordHeight, starSize= starSize)[0]
y2 = ls.ySetup(scaleFactor= scaleFactor, CenterCordHeight= CenterCordHeight, starSize= starSize)[1]


starName = ls.textSetup()[0]
starSpect = ls.textSetup()[1]

starX = ls.textSetup()[2]
starY = ls.textSetup()[3]
starZ = ls.textSetup()[4]

#halve star size
starSize = starSize/2


#add every thing to a dictionary
dictionary = {'x1':x1,'x2':x2,'y1':y1,'y2':y2,"Colour":starMain,"Mult":starMult,"Name":starName}
print(len(dictionary))
dict2 = {'Spect':starSpect,'starX':starX,'starY':starY,'starZ':starZ}


#set up canvas
img = ls.canvasSetup(x= width, y= height,Color= canvasColor)
#setup draw
draw = ls.drawSetup(img= img)

#cross Hair setup
crossHairSizeH = ls.crosshairSetup(starScale= starScale)[0]
print("crossHair Hight config")
crossHairSizeW = ls.crosshairSetup(starScale= starScale)[1]
print("crossHair width config")
data = ls.crosshairSetup(starScale= starScale)[2]
print("crossHair data")
black_areas = ls.crosshairSetup(starScale= starScale)[3]
print("crossHair black")

#get fonts
font_path = "data/Roboto-Regular.ttf"
#set up font
fontTitle = ImageFont.truetype(font_path, fontSizeTitle)
fontW = ImageFont.truetype(font_path, fontSize2)

#create 2 diagonal lines to assit in finding center
#draw.line((0,0) + img.size, fill=lineColor, width=20)
#draw.line((0, img.size[1], img.size[0], 0), fill=lineColor, width=20)

ls.gridCreation(img=img, draw= draw, stepCount= stepCount, lineColor= lineColor)


#loop through lists drawing starbackgrounds
ls.drawStarBackground(draw= draw, x1=x1,y1=y1,x2=x2,y2=y2,crossHairSizeH=crossHairSizeH,starName=starName,canvasColor=canvasColor,fontTitle=fontTitle)

#draw lines joining every star
ls.findNeighbours(scaleFactor=scaleFactor,widthHalf=CenterCordWidth,heightHalf=CenterCordHeight,draw=draw,lineWidth=lineWidth)

#draw stars and add star name
ls.drawStarText(img=img, draw=draw,data=data,black_areas=black_areas,x1=x1,y1=y1,starMain=starMain,crossHairSizeH=crossHairSizeH,starName=starName,fontTitle=fontTitle,starSpect=starSpect,starX=starX,starY=starY,starZ=starZ)

#show canvas
img.show()
#save image
img.save('stellarMap.png')