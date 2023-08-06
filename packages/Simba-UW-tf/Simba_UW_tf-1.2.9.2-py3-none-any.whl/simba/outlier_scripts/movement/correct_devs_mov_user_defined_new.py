import pandas as pd
import os
import numpy as np
import statistics
import math
from configparser import ConfigParser, NoSectionError
from datetime import datetime
from simba.drop_bp_cords import *
import glob


configFile = r"Z:\DeepLabCut\DLC_extract\Troubleshooting\SLEAP_9Test_2\project_folder\project_config.ini"

dateTime, loop = datetime.now().strftime('%Y%m%d%H%M%S'), 0
configFile = str(configFile)
config = ConfigParser()
config.read(configFile)
criterion = config.getfloat('Outlier settings', 'movement_criterion')
animal_no = config.getint('General settings', 'animal_no')
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

bodyPartNameArrayForMeans = np.empty((animal_no, 5), dtype=object)
for animal in range(animal_no):
    bodyPart_1_Name, bodyPart_2_Name = 'movement_bodypart1_mouse' + str(animal+1), 'movement_bodypart2_mouse' + str(animal + 1)
    bodyPart1, bodyPart2 = config.get('Outlier settings', bodyPart_1_Name), config.get('Outlier settings', bodyPart_2_Name)
    bodyPart_1_X, bodyPart_1_Y, bodyPart_2_X, bodyPart_2_Y = bodyPart1 + '_x', bodyPart1 + '_y', bodyPart2 + '_x', bodyPart2 + '_y'
    animalName = 'Animal_' + str(animal+1)
    bodyPartNameArrayForMeans[animal] = [animalName, bodyPart_1_X, bodyPart_1_Y, bodyPart_2_X, bodyPart_2_Y]

projectPath = config.get('General settings', 'project_path')
currentBodyPartFile = os.path.join(projectPath, 'logs', 'measures', 'pose_configs', 'bp_names', 'project_bp_names.csv')
bodyPartsFile = pd.read_csv(os.path.join(currentBodyPartFile), header=None)
bodyPartsList = list(bodyPartsFile[0])
bodyPartHeaders, columnHeadersShifted, xy_headers = [], [], []
p_cols, x_cols, y_cols = [], [], []
for i in bodyPartsList:
    col1, col2, col3 = (str(i) + '_x', str(i) + '_y', str(i) + '_p')
    col4, col5, col6 = (col1 + '_shifted', col2 + '_shifted', col3 + '_shifted')
    columnHeadersShifted.extend((col4, col5, col6))
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

#### CREATE DICT TO HOLD ANIMAL BPS AND NAMES
animalBpDict = create_body_part_dictionary(multiAnimalStatus, animalIDlist, animal_no, x_cols, y_cols, p_cols, [])
csv_dir_in, csv_dir_out, log_fn = os.path.join(projectPath, 'csv', 'input_csv'), os.path.join(projectPath, 'csv', 'outlier_corrected_movement'), os.path.join(projectPath, 'logs', 'Outliers_movement_' + str(dateTime) + '.csv')

def add_correction_prefix(col, bpcorrected_list):
    colc = 'Corrected_' + col
    bpcorrected_list.append(colc)
    return bpcorrected_list

def correct_value_position(df, colx, coly, col_corr_x, col_corr_y, dict_pos):
    dict_pos[colx] = dict_pos.get(colx, 0)
    dict_pos[coly] = dict_pos.get(coly, 0)
    currentCriterion = mean1size * criterion
    list_x = []
    list_y = []
    prev_x = df.iloc[0][colx]
    prev_y = df.iloc[0][coly]
    ntimes = 0
    live_prevx = df.iloc[0][colx]
    live_prevy = df.iloc[0][coly]
    NT = 12
    for index, row in df.iterrows():
        if index == 0:
            list_x.append(row[colx]), list_y.append(row[coly])
            continue
        if ((math.hypot(row[colx] - prev_x, row[coly] - prev_y) < currentCriterion) or (ntimes > NT and  math.hypot(row[colx] - live_prevx, row[coly] - live_prevy) < currentCriterion)):
            list_x.append(row[colx])
            list_y.append(row[coly])
            prev_x = row[colx]
            prev_y = row[coly]
            ntimes = 0
        else:
            list_x.append(prev_x)
            list_y.append(prev_y)
            dict_pos[colx] += 1
            dict_pos[coly] += 1
            ntimes += 1
        live_prevx = row[colx]
        live_prevy = row[coly]

    df[col_corr_x] = list_x
    df[col_corr_y] = list_y
    return df

filesFound = glob.glob(csv_dir_in + '/*.csv')
print('Processing ' + str(len(filesFound)) + ' files for movement outliers...')

########### CREATE PD FOR RAW DATA AND PD FOR MOVEMENT BETWEEN FRAMES ###########
logDfColumns = ['Video', 'Frames processed']
logDfColumns.extend(bodyPartsList)
logDfColumns.append(str('% corrected'))
log_df = pd.DataFrame(columns=logDfColumns)
list_dict_count_corrections = {}
for currentFile in filesFound:
    list_dict_count_corrections[currentFile] = {}
    baseNameFile = os.path.basename(currentFile).replace('.csv', '')
    csv_df = pd.read_csv(currentFile, names=bodyPartHeaders, index_col=None)
    csv_df = csv_df.drop(csv_df.index[[0, 1, 2]])
    csv_df = csv_df.apply(pd.to_numeric)

########### CREATE SHIFTED DATAFRAME FOR DISTANCE CALCULATIONS ###########################################
    csv_df_shifted = csv_df.shift(periods=1)
    csv_df_shifted.columns = columnHeadersShifted
    csv_df_combined = pd.concat([csv_df, csv_df_shifted], axis=1, join='inner')
    csv_df_combined = csv_df_combined.fillna(0)
    df_p_cols = pd.DataFrame([csv_df.pop(x) for x in p_cols]).T
    df_p_cols.reset_index()
    csv_out = pd.DataFrame()

    ########### MEAN MOUSE SIZES ###########################################
    dict_pos = {}
    for animal in range(len(bodyPartNameArrayForMeans)):
        print('Processing animal ' + str(animal + 1) + '...')
        mean1size = statistics.mean(np.sqrt((csv_df[bodyPartNameArrayForMeans[animal][1]] - csv_df[bodyPartNameArrayForMeans[animal][3]]) ** 2 + (csv_df[bodyPartNameArrayForMeans[animal][2]] - csv_df[bodyPartNameArrayForMeans[animal][4]]) ** 2))
        bplist1x, bplist1y, bpcorrected_list1x, bpcorrected_list1y = [], [], [], []
        currXcols, currYcols, currPcols = animalBpDict[animalIDlist[animal]]['X_bps'], animalBpDict[animalIDlist[animal]]['Y_bps'], animalBpDict[animalIDlist[animal]]['P_bps']

        for bp in currXcols:
            bplist1x.append(bp)
            bpcorrected_list1x = add_correction_prefix(bp, bpcorrected_list1x)
        for bp in currYcols:
            bplist1y.append(bp)
            bpcorrected_list1y = add_correction_prefix(bp, bpcorrected_list1y)
        
        for idx, col1x in enumerate(bplist1x):
            col1y = bplist1y[idx]
            col_corr_1x = bpcorrected_list1x[idx]
            col_corr_1y = bpcorrected_list1y[idx]
            csv_df_combined = correct_value_position(csv_df_combined, col1x, col1y, col_corr_1x, col_corr_1y, dict_pos)
        csv_df_combined.reset_index()

        for cols in range(len(currXcols)):
            csv_out = pd.concat([csv_out, csv_df_combined[bpcorrected_list1x[cols]], csv_df_combined[bpcorrected_list1y[cols]], df_p_cols[currPcols[cols]]], sort=False, axis=1)

    csv_out = csv_out.rename_axis('scorer')
    csv_out.columns = csv_out.columns.str.replace('Corrected_', '')

    fileOut = str(baseNameFile) + str('.csv')
    pathOut = os.path.join(csv_dir_out, fileOut)
    csv_out.to_csv(pathOut)
    fixed_M1_pos, currentFixedList = [], []
    currentFixedList.append(baseNameFile)
    currentFixedList.append(len(csv_out))
    for k in list(dict_pos):
        if k.endswith('_x'):
            del dict_pos[k]
    for y in list(dict_pos):
        fixed_M1_pos.append(dict_pos[y])
    currentFixedList.extend(fixed_M1_pos)
    percentCorrected = round(sum(fixed_M1_pos) / (len(csv_out) * len(bodyPartsList)) * 100, 3)
    currentFixedList.append(percentCorrected)
    log_df.loc[loop] = currentFixedList
    loop = loop + 1
    print(str(baseNameFile) + ' complete. Tot frames: '+ str(len(csv_out)) + '. Outliers: ' + str(sum(fixed_M1_pos)) + '. % corrected: ' + str(percentCorrected))
log_df.to_csv(log_fn, index=False)
print('Log for corrected "movement outliers" saved in project_folder/logs')