import pandas as pd
import os
import statistics
import numpy as np
from configparser import ConfigParser, NoSectionError
from datetime import datetime
import glob
from drop_bp_cords import *

configFile = r"Z:\DeepLabCut\DLC_extract\Troubleshooting\Open_field_4\project_folder\project_config.ini"

configFile = str(configFile)
config = ConfigParser()
config.read(configFile)
animalNo = config.getint('General settings', 'animal_no')
projectPath = config.get('General settings', 'project_path')
csv_dir_in = os.path.join(projectPath, 'csv', 'outlier_corrected_movement')
csv_dir_out = os.path.join(projectPath, 'csv', 'outlier_corrected_movement_location')

currentBodyPartFile = os.path.join(projectPath, 'logs', 'measures', 'pose_configs', 'bp_names', 'project_bp_names.csv')
dateTime = datetime.now().strftime('%Y%m%d%H%M%S')

try:
    animalIDlist = config.get('Multi animal IDs', 'id_list')
    animalIDlist = animalIDlist.split(",")
    if animalIDlist[0] != '':
        multiAnimalStatus = True
        print('Applying settings for multi-animal tracking...')
    else:
        multiAnimalStatus = False
        print('Applying settings for classical tracking...')

except NoSectionError:
    animalIDlist = ['']
    multiAnimalStatus = False
    print('Applying settings for classical tracking...')

bodyPartNameArrayForMeans = np.empty((animalNo, 5), dtype=object)
for animal in range(animalNo):
    bodyPart_1_Name, bodyPart_2_Name = 'location_bodypart1_mouse' + str(animal+1), 'location_bodypart2_mouse' + str(animal + 1)
    bodyPart1, bodyPart2 = config.get('Outlier settings', bodyPart_1_Name), config.get('Outlier settings', bodyPart_2_Name)
    bodyPart_1_X, bodyPart_1_Y, bodyPart_2_X, bodyPart_2_Y = bodyPart1 + '_x', bodyPart1 + '_y', bodyPart2 + '_x', bodyPart2 + '_y'
    animalName = 'Animal_' + str(animal+1)
    bodyPartNameArrayForMeans[animal] = [animalName, bodyPart_1_X, bodyPart_1_Y, bodyPart_2_X, bodyPart_2_Y]

bodyPartsFile = pd.read_csv(os.path.join(currentBodyPartFile, currentBodyPartFile), header=None)
bodyPartsList = list(bodyPartsFile[0])
bodyPartHeaders = []
xy_headers, p_cols, x_cols, y_cols, animal1_headers, animal2_headers, animalHeadersListofList = [], [], [], [], [], [], []
for i in bodyPartsList:
    col1, col2, col3 = (str(i) + '_x', str(i) + '_y', str(i) + '_p')
    p_cols.append(col3), x_cols.append(col1), y_cols.append(col2)
    bodyPartHeaders.extend((col1, col2, col3))
    xy_headers.extend((col1, col2))

if animalIDlist[0] != '':
    for animal in range(len(animalIDlist)):
        currentID = animalIDlist[animal] + '_'
        bodyPartNameArrayForMeans[animal][0] = animalIDlist[animal]
        bodyPartNameArrayForMeans[animal][1:7] = [currentID + x for x in bodyPartNameArrayForMeans[animal][1:5]]
else:
    animalIDlist = np.unique(bodyPartNameArrayForMeans[:,0])


animalBpDict = create_body_part_dictionary(multiAnimalStatus, animalIDlist, animalNo, x_cols, y_cols, p_cols, [])


vNm_list, fixedPositions_M1_list, frames_processed_list, counts_total_M1_list, loopy, loop = [], [], [], [], 0, 0
criterion = config.getfloat('Outlier settings', 'location_criterion')
filesFound = glob.glob(csv_dir_in + '/*.csv')
print('Processing ' + str(len(filesFound)) + ' files for location outliers...')

# ########### logfile path ###########
log_fn = os.path.join(projectPath, 'logs', 'Outliers_location_' + str(dateTime) + '.csv')
logDfColumns = ['Video', 'Frames_processed']
logDfColumns.extend(bodyPartsList)
logDfColumns.append(str('% corrected'))
log_df = pd.DataFrame(columns=logDfColumns)
#reliableCoordinates = np.zeros((7, 2))

########### CREATE PD FOR RAW DATA AND PD FOR MOVEMENT BETWEEN FRAMES ###########
for currentFile in filesFound:
    loopy += 1
    videoFileBaseName = os.path.basename(currentFile).replace('.csv', '')
    csv_df = pd.read_csv(currentFile, names=bodyPartHeaders, low_memory=False)
    csv_df = csv_df.drop(csv_df.index[[0]])
    csv_df = csv_df.apply(pd.to_numeric)
    vNm_list.append(videoFileBaseName)
    df_p_cols = pd.DataFrame([csv_df.pop(x) for x in p_cols]).T
    df_p_cols.fillna(0)
    df_p_cols.reset_index()
    totalFixList = []
    csv_out = pd.DataFrame()

    for animal in range(len(bodyPartNameArrayForMeans)):
        organizedDf_combined = pd.DataFrame()
        print('Processing animal ' + str(animal + 1) + '...')
        mean1size = statistics.mean(np.sqrt((csv_df[bodyPartNameArrayForMeans[animal][1]] - csv_df[bodyPartNameArrayForMeans[animal][3]]) ** 2 + (csv_df[bodyPartNameArrayForMeans[animal][2]] - csv_df[bodyPartNameArrayForMeans[animal][4]]) ** 2))
        currentCriterion = mean1size * criterion
        currXcols, currYcols, currPcols = animalBpDict[animalIDlist[animal]]['X_bps'], animalBpDict[animalIDlist[animal]]['Y_bps'], animalBpDict[animalIDlist[animal]]['P_bps']
        allColumns = currXcols + currYcols
        outputArray = np.array([0] * (len(currXcols * 2)))
        currentFixedList, fixedPositions_M1 = [], 0
        counts_total_M1 = [0] * len(currXcols)
        currDf = csv_df[allColumns]
        for index, row in currDf.iterrows():
            currentArray = row.to_numpy()
            currentArray = [[i, i + 1] for i in currentArray[0:-1:2]]
            nbody_parts = int(len(currentArray))
            counts = [0] * nbody_parts
            for i in range(0, (nbody_parts )-1):
                for j in range((i + 1), (nbody_parts)):
                    dist_ij = np.sqrt((currentArray[i][0] - currentArray[j][0]) ** 2 + (currentArray[i][1] - currentArray[j][1]) ** 2)
                    print(dist_ij)
                    if dist_ij > currentCriterion:
                        counts[i] += 1
                        counts[j] += 1
            positions = [i for i in range(len(counts)) if counts[i] > 1]
            for pos in positions:
                counts_total_M1[pos] += 1
            fixedPositions_M1 = fixedPositions_M1 + len(positions)
            if not positions:
                reliableCoordinates = currentArray
            else:
                for currentPosition in positions:
                    currentArray[currentPosition][0] = reliableCoordinates[currentPosition][0]
                    currentArray[currentPosition][1] = reliableCoordinates[currentPosition][1]
                reliableCoordinates = currentArray
            currentArray = np.array(currentArray)
            currentArray = currentArray.flatten()
            outputArray = np.vstack((outputArray, currentArray))
        totalFixList.append(counts_total_M1)
        outputArray = np.delete(outputArray, 0, 0)
        csvDf = pd.DataFrame(outputArray, columns=allColumns)
        csvDf.reset_index()
        for cols in range(int(len(csvDf.columns)/2)):
            colX, colY, colP = list(csvDf[currXcols[cols]]), list(csvDf[currYcols[cols]]), list(df_p_cols[currPcols[cols]])
            organizedDf = pd.DataFrame(list(zip(colX, colY, colP)))
            organizedDf_combined = pd.concat([organizedDf_combined, organizedDf], axis=1)
        csv_out = pd.concat([csv_out, organizedDf_combined], axis=1)
    csv_out.columns = bodyPartHeaders
    csvOutPath = os.path.join(csv_dir_out, videoFileBaseName + str('.csv'))
    csv_out.to_csv(csvOutPath)
    totalFixList = [item for sublist in totalFixList for item in sublist]
    currentFixedList.append(videoFileBaseName)
    currentFixedList.append(len(csv_df))
    currentFixedList.extend(totalFixList)
    percentBDcorrected = round(sum(totalFixList) / (len(csv_df) * len(df_p_cols.columns)), 6)
    currentFixedList.append(percentBDcorrected)
    print(str(videoFileBaseName) + '. Tot frames: ' + str(len(csv_df)) + '. Outliers: ' + str(sum(totalFixList)) + '. % outliers: ' + str(round(percentBDcorrected, 3)))
    log_df.loc[loop] = currentFixedList
    loop = loop + 1
log_df.to_csv(log_fn, index=False)
print('Log for corrected "location outliers" saved in project_folder/logs')