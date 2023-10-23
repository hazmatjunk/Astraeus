# Astraeus
Stellar Cartography Tools

This is Beta and thus contains several problems and lots bits of code doing nothing

Must Have hygdata_v3
(this is auto downloaded usally but just confirm that this turns up)

This was tested and made using python 3.9
five modules are required:
    -numpy
    -pandas
    -Pillow
    -matplotlib
    -scipy

To create the final map follow these steps:
1) ensure hygdata is in a sub folder in the same folder as the 3 python programs
2) run cordCalculator and await results. May take up to 5 minutes
3) run 2dlayout or 3dlayout. You may need to change scale factor and rotation for 2dlayout
5) final map should be stellarMap.png in Astraeus folder for 2d. The 3d should open it's own window

Knowen Bugs
-Currently you need Helvetica.ttf in the main folder
    -ignore this currently using google fonts robotico as the helvetica link has decayed need to fix this when I have time
-All the Data is to the left
-Sometimes stops working requiring restart
-need to not create nearly so many files
