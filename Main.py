import Constants
import Tests

import sys
import json
import os
import pandas as pd

def getFullInputPath(pJsonFileName):
    return os.path.join(Constants.PYTHON_BASE_DIRECTORY, Constants.BACKEND_BASE_DIRECTORY_PATH, Constants.DATASET_INPUT_PATH, pJsonFileName)

def getFullOutputPath(pJsonFileName):
    return os.path.join(Constants.PYTHON_BASE_DIRECTORY, Constants.BACKEND_BASE_DIRECTORY_PATH, Constants.DATASET_OUTPUT_PATH, pJsonFileName)

def getFullTimeSeriesPath(pDatasetFileName):
    return os.path.join(Constants.PYTHON_BASE_DIRECTORY, Constants.BACKEND_BASE_DIRECTORY_PATH, Constants.DATASET_TIME_SERIES_PATH, pDatasetFileName)

def getTimeSeries(datasetFileName):
    timeSeriesPath = getFullTimeSeriesPath(datasetFileName + ".csv")
    dataset = pd.read_csv(str(timeSeriesPath), header = None, names = [Constants.DATE_COLUMN_NAME, Constants.DATA_COLUMN_NAME])
    dataset[Constants.DATE_COLUMN_NAME] = pd.to_datetime(dataset[Constants.DATE_COLUMN_NAME], format = Constants.DATE_TIME_FORMAT)

    return pd.Series(dataset[Constants.DATA_COLUMN_NAME].values, index = dataset[Constants.DATE_COLUMN_NAME])

def evaluatePValue(inputJson, outputJson):
    inputPValue = -1
    resultPValue = -1

    if Constants.OUTPUT_P_VALUE_KEY in outputJson:
        resultPValue = float(outputJson[Constants.OUTPUT_P_VALUE_KEY][Constants.OUTPUT_ELEMENT_RESULT_KEY])

    if Constants.INPUT_P_VALUE_KEY in inputJson:
        inputPValue = float(inputJson[Constants.INPUT_P_VALUE_KEY])

    outputJson[Constants.OUTPUT_USED_P_VALUE_KEY] = {
        Constants.OUTPUT_ELEMENT_TITLE_KEY: Constants.OUTPUT_USED_P_VALUE_TITLE_VALUE,
        Constants.OUTPUT_ELEMENT_RESULT_KEY: inputPValue
    }

    outputJson[Constants.OUTPUT_EVALUATION_KEY] = {
        Constants.OUTPUT_ELEMENT_TITLE_KEY: Constants.OUTPUT_EVALUATION_TITLE_VALUE,
        Constants.OUTPUT_ELEMENT_RESULT_KEY: ""
    }

    if inputPValue == -1 or resultPValue == -1:
        outputJson[Constants.OUTPUT_EVALUATION_KEY][Constants.OUTPUT_ELEMENT_RESULT_KEY] = "p-hodnoty nebolo možné vyhodnotiť"
        return

    if resultPValue < inputPValue:
        outputJson[Constants.OUTPUT_EVALUATION_KEY][Constants.OUTPUT_ELEMENT_RESULT_KEY] = "p-hodnota je nižšia ako zvolená hladina významnosti, zamietame nulovú hypotézu v prospech alternatívnej hypotézy"
    else:
        outputJson[Constants.OUTPUT_EVALUATION_KEY][Constants.OUTPUT_ELEMENT_RESULT_KEY] = "p-hodnota je rovná ale vyššia ako hladina významnosti, nezamietame nulovú hypotézu"

def executeAction(jsonFileName):
    inputJsonFilePath = getFullInputPath(jsonFileName)
    outputJsonFilePath = getFullOutputPath(jsonFileName)

    outputJson = {}

    with open(inputJsonFilePath) as inputFile:
        inputJson = json.load(inputFile)
        action = inputJson[Constants.INPUT_ACTION_KEY]
        timeSeries = getTimeSeries(inputJson[Constants.INPUT_FILE_NAME_KEY])

        if action == Constants.ACTION_DICKEY_FULLER_TEST:
            success = Tests.dickeyFullerTest(timeSeries, inputJson, outputJson)
        else:
            success = False

    outputJson[Constants.OUTPUT_SUCCESS_KEY] = success
    if success:
        evaluatePValue(inputJson, outputJson)

    outputJsonData = json.dumps(outputJson)

    with open(outputJsonFilePath, 'w') as outputFile:
        outputFile.write(outputJsonData)

    print("============================================================ INPUT JSON ============================================================")
    print(json.dumps(inputJson, ensure_ascii = False, indent = 4))
    print("========================================================== INPUT JSON END ==========================================================")

    print("\n=========================================================== OUTPUT JSON ============================================================")
    print(json.dumps(outputJson, ensure_ascii = False, indent = 4))
    print("========================================================== OUTPUT JSON END ==========================================================")

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding = 'utf-8')

    try:
        fileName = ""
        if len(sys.argv) > 1:
            fileName = sys.argv[1]
        else:
            fileName = "debug.json"
            print("\n\n===== DEBUG =====")

        executeAction(fileName)
    except Exception as exception:
        print(exception)
        sys.exit(1)

    sys.exit(0)
