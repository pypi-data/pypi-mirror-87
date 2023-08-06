import numpy as np
import cv2
import os
import pandas as pd
from scipy import ndimage
from configparser import ConfigParser, MissingSectionHeaderError, NoSectionError
import glob
from simba.drop_bp_cords import create_bp_dict
from pylab import *

def plotsklearnresult(iniFile,videoSetting, frameSetting):

    config = ConfigParser()
    configFile = str(iniFile)
    try:
        config.read(configFile)
    except MissingSectionHeaderError:
        print('ERROR:  Not a valid project_config file. Please check the project_config.ini path.')
    projectPath = config.get('General settings', 'project_path')
    csv_dir_in = os.path.join(projectPath, 'csv', "machine_results")
    animalsNo = config.getint('General settings', 'animal_no')
    frames_dir_out = os.path.join(projectPath, 'frames', 'output', 'sklearn_results')
    if not os.path.exists(frames_dir_out):
        os.makedirs(frames_dir_out)
    counters_no, vidInfPath = config.getint('SML settings', 'No_targets'), os.path.join(projectPath, 'logs', 'video_info.csv')
    try:
        multiAnimalIDList = config.get('Multi animal IDs', 'id_list')
        multiAnimalIDList = multiAnimalIDList.split(",")
        if multiAnimalIDList[0] != '':
            multiAnimalStatus = True
            print('Applying settings for multi-animal tracking...')
        else:
            multiAnimalStatus = False
            print('Applying settings for classical tracking...')

    except NoSectionError:
        multiAnimalIDList = ['']
        multiAnimalStatus = False
        print('Applying settings for classical tracking...')
    print(multiAnimalStatus)

    vidinfDf = pd.read_csv(vidInfPath)
    target_names, loopy = [], 0
    cmaps = ['hot', 'winter', 'spring', 'summer', 'autumn', 'cool', 'bone', 'pink']
    Xcols, Ycols, Pcols = getBpNames(iniFile)
    cMapSize = int(len(Xcols)/animalsNo) + 1
    colorListofList = []
    for colormap in range(animalsNo):
        currColorMap = cm.get_cmap(cmaps[colormap], cMapSize)
        currColorList = []
        for i in range(currColorMap.N):
            rgb = list((currColorMap(i)[:3]))
            rgb = [i * 255 for i in rgb]
            rgb.reverse()
            currColorList.append(rgb)
        colorListofList.append(currColorList)

    filesFound = glob.glob(csv_dir_in + '/*.csv')
    print('Processing ' + str(len(filesFound)) + ' videos ...')
    ########### GET MODEL NAMES ###########
    for i in range(counters_no):
        currentModelNames = 'target_name_' + str(i + 1)
        currentModelNames = config.get('SML settings', currentModelNames)
        target_names.append(currentModelNames)
    cmap = cm.get_cmap('Set1', counters_no + 3)
    colors = []
    for i in range(cmap.N):
        rgb = list((cmap(i)[:3]))
        rgb = [i * 255 for i in rgb]
        rgb.reverse()
        colors.append(rgb)

    #### CREATE DICT TO HOLD ANIMAL BPS AND NAMES
    animalBpDict = create_bp_dict(multiAnimalStatus, multiAnimalIDList, animalsNo, Xcols, Ycols, [], colorListofList)
    print(animalBpDict)

    ########### FIND PREDICTION COLUMNS ###########
    for currentVideo in filesFound:
        target_counters, target_timers = ([0] * counters_no, [0] * counters_no)
        loopy += 1
        CurrentVideoName = os.path.basename(currentVideo)
        if frameSetting == 1:
            videoFrameDir = os.path.join(frames_dir_out, CurrentVideoName.replace('.csv', ''))
            if not os.path.exists(videoFrameDir):
                os.makedirs(videoFrameDir)
        CurrentVideoRow = vidinfDf.loc[vidinfDf['Video'] == str(CurrentVideoName.replace('.csv', ''))]
        try:
            fps = int(CurrentVideoRow['fps'])
        except TypeError:
            print('Error: make sure all the videos that are going to be analyzed are represented in the project_folder/logs/video_info.csv file')
        currentDf = pd.read_csv(currentVideo, index_col=0)
        currentDf = currentDf.fillna(0)
        currentDf = currentDf.astype(int)
        currentDf = currentDf.loc[:, ~currentDf.columns.str.contains('^Unnamed')]
        currentDf = currentDf.reset_index()
        if os.path.exists(os.path.join(projectPath,'videos', CurrentVideoName.replace('.csv', '.mp4'))):
            videoPathName = os.path.join(projectPath,'videos', CurrentVideoName.replace('.csv', '.mp4'))
        elif os.path.exists(os.path.join(projectPath,'videos', CurrentVideoName.replace('.csv', '.avi'))):
            videoPathName = os.path.join(projectPath,'videos', CurrentVideoName.replace('.csv', '.avi'))
        else:
            print('Cannot locate video ' + str(CurrentVideoName.replace('.csv', '')) + ' in mp4 or avi format')
            break
        cap = cv2.VideoCapture(videoPathName)
        width, height, frames = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        outputFileName = os.path.join(frames_dir_out, CurrentVideoName)
        if height < width:
            videoHeight, videoWidth = width, height
        if height >= width:
            videoHeight, videoWidth = height, width
        writer = cv2.VideoWriter(outputFileName.replace('.csv', '.mp4'), fourcc, fps, (videoWidth, videoHeight))
        mySpaceScale, myRadius, myResolution, myFontScale = 60, 12, 1500, 1.5
        maxResDimension = max(width, height)
        circleScale, fontScale, spacingScale = int(myRadius / (myResolution / maxResDimension)), float(myFontScale / (myResolution / maxResDimension)), int(mySpaceScale / (myResolution / maxResDimension))
        currRow = 0
        a = np.deg2rad(90)
        while (cap.isOpened()):
            ret, frame = cap.read()
            rotationFlag = False
            IDlabelLoc = []
            if ret == True:
                for currAnimal in range(animalsNo):
                    currentDictID = list(animalBpDict.keys())[currAnimal]
                    currentDict = animalBpDict[currentDictID]
                    currNoBps = len(currentDict['X_bps'])
                    IDappendFlag = False
                    animalArray = np.empty((currNoBps, 2), dtype=int)
                    for bp in range(currNoBps):
                        hullColor = currentDict['colors'][bp]
                        currXheader, currYheader, currColor = currentDict['X_bps'][bp], currentDict['Y_bps'][bp], currentDict['colors'][bp]
                        currAnimal = currentDf.loc[currentDf.index[currRow], [currXheader, currYheader]]
                        cv2.circle(frame, (currAnimal[0], currAnimal[1]), 0, hullColor, circleScale)
                        animalArray[bp] = [currAnimal[0], currAnimal[1]]
                        if (multiAnimalStatus == True):
                            if ('Centroid' in currXheader) or ('Center' in currXheader) or ('centroid' in currXheader) or ('center' in currXheader):
                                IDlabelLoc.append([currAnimal[0], currAnimal[1]])
                                IDappendFlag = True
                    if (multiAnimalStatus == False):
                        animalArray = np.reshape(animalArray, (-1, 2))
                        polyglon_array_hull = cv2.convexHull((animalArray.astype(int)))
                        cv2.drawContours(frame, [polyglon_array_hull.astype(int)], 0, (255, 255, 255), 2)
                    if IDappendFlag == False and (multiAnimalStatus == True):
                        IDlabelLoc.append([currAnimal[0], currAnimal[1]])
                if height < width:
                    frame = ndimage.rotate(frame, 90)
                    rotationFlag = True
                if (multiAnimalStatus == True):
                    if rotationFlag == False:
                        for currAnimal in range(animalsNo):
                            currentDictID = list(animalBpDict.keys())[currAnimal]
                            cv2.putText(frame, str(multiAnimalIDList[currAnimal]), (IDlabelLoc[currAnimal][0], IDlabelLoc[currAnimal][1]), cv2.FONT_HERSHEY_COMPLEX, fontScale, animalBpDict[currentDictID]['colors'][0], 4)
                    if rotationFlag == True:
                        for currAnimal in range(animalsNo):
                            currentDictID = list(animalBpDict.keys())[currAnimal]
                            newX1, newY1 = abs(int(IDlabelLoc[currAnimal][0] * cos(a) + IDlabelLoc[currAnimal][1] * sin(a))), int(frame.shape[0] - int(((-IDlabelLoc[currAnimal][1]) * cos(a) + IDlabelLoc[currAnimal][0] * sin(a))))
                            cv2.putText(frame, str(multiAnimalIDList[currAnimal]), (newX1, newY1), cv2.FONT_HERSHEY_COMPLEX, fontScale, animalBpDict[currentDictID]['colors'][0], 4)

                # draw event timers
                for b in range(counters_no):
                    target_timers[b] = (1 / fps) * target_counters[b]
                    target_timers[b] = round(target_timers[b], 2)
                cv2.putText(frame, str('Timers'), (10, ((height - height) + spacingScale)), cv2.FONT_HERSHEY_COMPLEX, fontScale, (0, 255, 0), 4)
                addSpacer = 2
                for k in range(counters_no):
                    cv2.putText(frame, (str(target_names[k]) + ' ' + str(target_timers[k]) + str('s')), (10, (height - height) + spacingScale * addSpacer), cv2.FONT_HERSHEY_SIMPLEX, fontScale, (255, 0, 0), 4)
                    addSpacer += 1
                cv2.putText(frame, str('ensemble prediction'), (10, (height - height) + spacingScale * addSpacer), cv2.FONT_HERSHEY_SIMPLEX, fontScale, (0, 255, 0), 4)
                addSpacer += 1
                for p in range(counters_no):
                    TargetVal = int(currentDf.loc[currRow, [target_names[p]]])
                    if TargetVal == 1:
                        cv2.putText(frame, str(target_names[p]), (10, (height - height) + spacingScale * addSpacer), cv2.FONT_HERSHEY_TRIPLEX, int(fontScale*1.8), colors[p], 4)
                        target_counters[p] += 1
                        addSpacer += 1
                if videoSetting == 1:
                    writer.write(frame)
                if frameSetting == 1:
                    frameName = os.path.join(videoFrameDir, str(currRow) + '.png')
                    cv2.imwrite(frameName, frame)
                if (videoSetting == 0) and (frameSetting == 0):
                    print('Error: Please choose video and/or frames.')
                    break
                print('Frame ' + str(currRow) + '/' + str(frames) + '. Video ' + str(loopy) + '/' + str(len(filesFound)))
                currRow += 1

            if frame is None:
                print('Video ' + str(os.path.basename(CurrentVideoName.replace('.csv', '.mp4'))) + ' saved.')
                cap.release()
                break