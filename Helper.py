import Constants

import os
import random
import string

import json
import numpy as np

def getFullInputPath(pFileName):
    return os.path.join(Constants.PYTHON_BACKEND_BASE_DIRECTORY_PATH, Constants.JAVA_BACKEND_BASE_DIRECTORY_NAME, Constants.DATASET_INPUT_PATH, pFileName)

def getFullOutputPath(pFileName):
    return os.path.join(Constants.PYTHON_BACKEND_BASE_DIRECTORY_PATH, Constants.JAVA_BACKEND_BASE_DIRECTORY_NAME, Constants.DATASET_OUTPUT_PATH, pFileName)

def getFullTimeSeriesPath(pDatasetFileName):
    return os.path.join(Constants.PYTHON_BACKEND_BASE_DIRECTORY_PATH, Constants.JAVA_BACKEND_BASE_DIRECTORY_NAME, Constants.DATASET_TIME_SERIES_PATH, pDatasetFileName)

def getRandomString(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k = length))

def formatDate(date):
    return date.strftime(Constants.DATE_TIME_FORMAT)

def convertToJsonArray(array):
    listArray = array.tolist()
    return [None if np.isnan(x) else x for x in listArray]

def convertToJsonDatesArray(array):
    listArray = array.tolist()
    return [date.strftime(Constants.DATE_TIME_FORMAT) for date in listArray]

def buildArguments(inputJson, keys):
    args = {}

    for key in keys:
        if key in inputJson:
            if inputJson[key] == "None":
                args[key] = None
            else:
                args[key] = inputJson[key]

    print("\n=============================================================== ARGS ===============================================================")
    print(json.dumps(args, ensure_ascii = False, indent = 4))
    print("============================================================= ARGS END =============================================================")

    return args
