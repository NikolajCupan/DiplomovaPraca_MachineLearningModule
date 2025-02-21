import Constants

import json
import os
import random
import string

import numpy as np
import pandas as pd

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

def formatJson(pJson):
    jsonData = json.dumps(pJson, ensure_ascii = False, indent = 4)
    formattedJsonData = ""

    inString = False
    inArray = False
    escape = False

    for i in range(len(jsonData)):
        char = jsonData[i]
        appendedChar = char

        if inString:
            if escape:
                escape = False
            elif char == '\\':
                escape = True
            elif char == '\"':
                inString = False
        else:
            if char == '\"':
                inString = True
            elif char == '[':
                inArray = True
            elif char == ']':
                inArray = False
            elif char == '\n' and inArray:
                appendedChar = ''
            elif char == ' ' and inArray:
                appendedChar = ''
            elif char == ',' and inArray:
                appendedChar = ", "

        formattedJsonData += appendedChar

    return formattedJsonData

def getTimeSeries(datasetFileName):
    timeSeriesPath = getFullTimeSeriesPath(datasetFileName + ".csv")
    dataset = pd.read_csv(str(timeSeriesPath), header = None, names = [Constants.DATE_COLUMN_NAME, Constants.DATA_COLUMN_NAME])
    dataset[Constants.DATE_COLUMN_NAME] = pd.to_datetime(dataset[Constants.DATE_COLUMN_NAME], format = Constants.DATE_TIME_FORMAT, errors = "coerce")

    timeSeries = pd.Series(dataset[Constants.DATA_COLUMN_NAME].values, index=dataset[Constants.DATE_COLUMN_NAME])
    timeSeries = timeSeries.dropna()
    timeSeries = timeSeries[timeSeries != "-"]
    timeSeries = pd.to_numeric(timeSeries, errors = "coerce").dropna()

    return timeSeries

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
