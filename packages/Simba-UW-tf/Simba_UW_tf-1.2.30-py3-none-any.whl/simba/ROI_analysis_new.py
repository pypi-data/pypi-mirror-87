import glob
import itertools
import os
from configparser import ConfigParser, MissingSectionHeaderError, NoSectionError
from datetime import datetime
import numpy as np
import pandas as pd
from shapely import geometry
from shapely.geometry import Point
from drop_bp_cords import getBpHeaders

inifile = r"Z:\DeepLabCut\DLC_extract\Troubleshooting\Open_field_2\project_folder\project_config.ini"
inputcsv = 'outlier_corrected_movement_location'

dateTime = datetime.now().strftime('%Y%m%d%H%M%S')
config = ConfigParser()
config.read(inifile)

## get dataframe column name
bplist = getBpHeaders(inifile)
noAnimals = config.getint('ROI settings', 'no_of_animals')
projectPath = config.get('General settings', 'project_path')

animalBodypartList = []
for bp in range(noAnimals):
    animalName = 'animal_' + str(bp + 1) + '_bp'
    animalBpName = config.get('ROI settings', animalName)
    animalBpNameX, animalBpNameY = animalBpName + '_x', animalBpName + '_y'
    animalBodypartList.append([animalBpNameX, animalBpNameY])
columns2grab = [item[0:2] for item in animalBodypartList]
columns2grab = [item for sublist in columns2grab for item in sublist]

try:
    multiAnimalIDList = config.get('Multi animal IDs', 'id_list')
    multiAnimalIDList = multiAnimalIDList.split(",")
    if multiAnimalIDList[0] != '':
        multiAnimalStatus = True
        print('Applying settings for multi-animal tracking...')
    else:
        multiAnimalStatus = False
        for animal in range(noAnimals):
            multiAnimalIDList.append('Animal_' + str(animal+1) + '_')
        print('Applying settings for classical tracking...')
except NoSectionError:
    multiAnimalIDList = []
    for animal in range(noAnimals):
        multiAnimalIDList.append('Animal_' + str(animal + 1) + '_')
    multiAnimalStatus = False
    print('Applying settings for classical tracking...')

logFolderPath = os.path.join(projectPath, 'logs')
vidInfPath = os.path.join(logFolderPath, 'video_info.csv')
vidinfDf = pd.read_csv(vidInfPath)
csv_dir_in = os.path.join(projectPath, 'csv', inputcsv)
ROIcoordinatesPath = os.path.join(logFolderPath, 'measures', 'ROI_definitions.h5')
rectanglesInfo = pd.read_hdf(ROIcoordinatesPath, key='rectangles')
circleInfo = pd.read_hdf(ROIcoordinatesPath, key='circleDf')
polygonInfo = pd.read_hdf(ROIcoordinatesPath, key='polygons')
outputDfTime = pd.DataFrame(columns=['Video'])
rectangleNames, circleNames, polygonNames = (list(rectanglesInfo['Name'].unique()), list(circleInfo['Name'].unique()), list(polygonInfo['Name'].unique()))
shapeList = list(itertools.chain(rectangleNames, circleNames, polygonNames))
for newcol in range(len(shapeList)):
    for bp in multiAnimalIDList:
        colName = str(bp) + shapeList[newcol]
        outputDfTime[colName] = 0
for newcol in range(len(shapeList)):
    for bp in multiAnimalIDList:
        colName = str(bp) + shapeList[newcol] + '_%_of_session'
        outputDfTime[colName] = 0
outputDfEntries = outputDfTime.copy()
filesFound = glob.glob(csv_dir_in + '/*.csv')

for i in filesFound:
    CurrVidFn = os.path.basename(i)
    CurrentVideoName = CurrVidFn.replace('.csv', '')
    print('Analysing ' + str(CurrentVideoName) + '...')
    videoSettings = vidinfDf.loc[vidinfDf['Video'] == str(CurrentVideoName)]
    currFps = int(videoSettings['fps'])
    noRectangles = len(rectanglesInfo.loc[rectanglesInfo['Video'] == str(CurrentVideoName)])
    noCircles = len(circleInfo.loc[circleInfo['Video'] == str(CurrentVideoName)])
    noPolygons = len(polygonInfo.loc[polygonInfo['Video'] == str(CurrentVideoName)])
    rectangleTimes, rectangleEntries = ([[0] * len(multiAnimalIDList) for i in range(noRectangles)] , [[0] * len(multiAnimalIDList) for i in range(noRectangles)])
    circleTimes, circleEntries = ([[0] * len(multiAnimalIDList) for i in range(noCircles)], [[0] * len(multiAnimalIDList) for i in range(noCircles)])
    polygonTime, polyGonEntries = ([[0] * len(multiAnimalIDList) for i in range(noPolygons)], [[0] * len(multiAnimalIDList) for i in range(noPolygons)])
    Rectangles = (rectanglesInfo.loc[rectanglesInfo['Video'] == str(CurrentVideoName)])
    Circles = (circleInfo.loc[circleInfo['Video'] == str(CurrentVideoName)])
    Polygons = (polygonInfo.loc[polygonInfo['Video'] == str(CurrentVideoName)])
    rectangleEntryCheck = [[True] * len(multiAnimalIDList) for i in range(noRectangles)]
    circleEntryCheck = [[True] * len(multiAnimalIDList) for i in range(noCircles)]
    polygonEntryCheck = [[True] * len(multiAnimalIDList) for i in range(noPolygons)]
    currDfPath = os.path.join(csv_dir_in, CurrVidFn)
    currDf = pd.read_csv(currDfPath, usecols=columns2grab)
    totalSecInSession = currDf.shape[0] / currFps

    for index, row in currDf.iterrows():
        currentPoints = np.empty((noAnimals, 2), dtype=int)
        for animal in range(noAnimals):
            currentPoints[animal][0], currentPoints[animal][1] = int(row[animalBodypartList[animal][0]]), int(row[animalBodypartList[animal][1]])
        for rectangle in range(noRectangles):
            topLeftX, topLeftY = (Rectangles['topLeftX'].iloc[rectangle], Rectangles['topLeftY'].iloc[rectangle])
            bottomRightX, bottomRightY = (topLeftX + Rectangles['width'].iloc[rectangle], topLeftY + Rectangles['height'].iloc[rectangle])
            for bodyparts in range(len(currentPoints)):
                if (((topLeftX-10) <= currentPoints[bodyparts][0] <= (bottomRightX+10)) and ((topLeftY-10) <= currentPoints[bodyparts][1] <= (bottomRightY+10))):
                    rectangleTimes[rectangle][bodyparts] = round((rectangleTimes[rectangle][bodyparts] + (1 / currFps)), 2)
                    if rectangleEntryCheck[rectangle][bodyparts] == True:
                        rectangleEntries[rectangle][bodyparts] += 1
                        rectangleEntryCheck[rectangle][bodyparts] = False
                else:
                    rectangleEntryCheck[rectangle][bodyparts] = True
        for circle in range(noCircles):
            circleName, centerX, centerY, radius = (Circles['Name'].iloc[circle], Circles['centerX'].iloc[circle], Circles['centerY'].iloc[circle], Circles['radius'].iloc[circle])
            for bodyparts in range(len(currentPoints)):
                euclidPxDistance = int(np.sqrt((currentPoints[bodyparts][0] - centerX) ** 2 + (currentPoints[bodyparts][1] - centerY) ** 2))
                if euclidPxDistance <= radius:
                    circleTimes[circle][bodyparts] = round((circleTimes[circle][bodyparts] + (1 / currFps)),2)
                    if circleEntryCheck[circle][bodyparts] == True:
                        circleEntries[circle][bodyparts] += 1
                        circleEntryCheck[circle][bodyparts] = False
                else:
                    circleEntryCheck[circle][bodyparts] = True
        for polygon in range(noPolygons):
            PolygonName, vertices = (Polygons['Name'].iloc[polygon], Polygons['vertices'].iloc[polygon])
            vertices = np.array(vertices, np.int32)
            for bodyparts in range(len(currentPoints)):
                pointList = []
                for i in vertices:
                    point = geometry.Point(i)
                    pointList.append(point)
                polyGon = geometry.Polygon([[p.x, p.y] for p in pointList])
                CurrPoint = Point(int(currentPoints[bodyparts][0]), int(currentPoints[bodyparts][1]))
                polyGonStatus = (polyGon.contains(CurrPoint))
                if polyGonStatus == True:
                    polygonTime[polygon][bodyparts] = round((polygonTime[polygon][bodyparts] + (1 / currFps)), 2)
                    if polygonEntryCheck[polygon][bodyparts] == True:
                        polyGonEntries[polygon][bodyparts] += 1
                        polygonEntryCheck[polygon][bodyparts] = False
                else:
                    polygonEntryCheck[polygon][bodyparts] = True

    rectangleTimes, circleTimes, polygonTime = (list(itertools.chain(*rectangleTimes)), list(itertools.chain(*circleTimes)), list(itertools.chain(*polygonTime)))
    rectangleEntries, circleEntries, polyGonEntries = (list(itertools.chain(*rectangleEntries)), list(itertools.chain(*circleEntries)), list(itertools.chain(*polyGonEntries)))
    collapsedListTime = [CurrentVideoName, rectangleTimes, circleTimes, polygonTime]
    collapsedListTime = list(itertools.chain.from_iterable(itertools.repeat(x, 1) if isinstance(x, str) else x for x in collapsedListTime))
    timesInCollTime = collapsedListTime[1:]
    timesInCollTime = [x / totalSecInSession for x in timesInCollTime]
    timesInCollTime = ['%.3f' % elem for elem in timesInCollTime]
    collapsedListTime.extend(timesInCollTime)
    collapsedListEntry = [CurrentVideoName, rectangleEntries, circleEntries, polyGonEntries]
    collapsedListEntry = list(itertools.chain.from_iterable(itertools.repeat(x, 1) if isinstance(x, str) else x for x in collapsedListEntry))
    EntrieInEntryList = collapsedListEntry[1:]
    sumEntries = sum(EntrieInEntryList)
    EntrieInEntryList = [x / sumEntries for x in EntrieInEntryList]
    EntrieInEntryList = ['%.3f' % elem for elem in EntrieInEntryList]
    collapsedListEntry.extend(EntrieInEntryList)
    outputDfTime = outputDfTime.append(pd.Series(dict(zip(outputDfTime.columns, collapsedListTime))),ignore_index=True)
    outputDfEntries = outputDfEntries.append(pd.Series(dict(zip(outputDfEntries.columns, collapsedListEntry))),ignore_index=True)

if len(filesFound) < 1:
    print('No files found. Have you corrected outliers?')
else:
    outputDfTimeFilePath , outputDfEntryFilePath = (os.path.join(logFolderPath, 'ROI_time_data_' + dateTime + '.csv'), os.path.join(logFolderPath, 'ROI_entry_data_' + dateTime + '.csv'))
    outputDfTime.to_csv(outputDfTimeFilePath, index=False)
    outputDfEntries.to_csv(outputDfEntryFilePath, index=False)
    print('ROI data saved in ' + 'project_folder\logs.')


