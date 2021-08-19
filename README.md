# Astraeus
Stellar Cartography Tools

This is Beta lots of problems and bits of code doing nothing

Must Have hygdata_v3
This was tested and made using python 3.9
three modules are required:
    numpy
    pandas
    Pillow

To create the final map follow these steps:
1) ensure hygdata is in a sub folder in the same folder as the 3 python programs
2) run cordCalculator and await results. May take up to 5 minutes
3) run dataCleanup if need be change maximun range
4) run layout may need to change scale factor
5) final map should be stellarMap.png in Astraeus folder

Knowen Bugs
-Currently you need Helvetica.ttf in the main folder
-All the Data is to the left
-Sometimes stops working requiring restart
-need to not create nearly so many files
