import Constants
import Debug
import Helper

import Models
import Tests
import Transformations

import sys
import json

import pandas as pd

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
    timeSeriesPath = Helper.getFullTimeSeriesPath(datasetFileName + ".csv")
    dataset = pd.read_csv(str(timeSeriesPath), header = None, names = [Constants.DATE_COLUMN_NAME, Constants.DATA_COLUMN_NAME])
    dataset[Constants.DATE_COLUMN_NAME] = pd.to_datetime(dataset[Constants.DATE_COLUMN_NAME], format = Constants.DATE_TIME_FORMAT, errors = "coerce")

    timeSeries = pd.Series(dataset[Constants.DATA_COLUMN_NAME].values, index=dataset[Constants.DATE_COLUMN_NAME])
    timeSeries = timeSeries.dropna()
    timeSeries = timeSeries[timeSeries != "-"]
    timeSeries = pd.to_numeric(timeSeries, errors = "coerce").dropna()

    return timeSeries

def executeAction(jsonFileName):
    inputJsonFilePath = Helper.getFullInputPath(jsonFileName)
    outputJsonFilePath = Helper.getFullOutputPath(jsonFileName)

    outputJson = {}

    with open(inputJsonFilePath) as inputFile:
        inputJson = json.load(inputFile)
        action = inputJson[Constants.INPUT_ACTION_KEY]
        timeSeries = getTimeSeries(inputJson[Constants.INPUT_FILE_NAME_KEY])

        #
        # Tests
        if action == Constants.ACTION_DICKEY_FULLER_TEST:
            success = Tests.dickeyFullerTest(timeSeries, inputJson, outputJson)
        elif action == Constants.ACTION_KPSS_TEST:
            success = Tests.kpssTest(timeSeries, inputJson, outputJson)
        elif action == Constants.ACTION_SEASONAL_DECOMPOSE:
            success = Tests.seasonalDecompose(timeSeries, inputJson, outputJson)
        elif action == Constants.ACTION_PERIODOGRAM:
            success = Tests.periodogram(timeSeries, inputJson, outputJson)
        elif action == Constants.ACTION_CORRELOGRAM_ACF:
            success = Tests.correlogramAcf(timeSeries, inputJson, outputJson)
        elif action == Constants.ACTION_CORRELOGRAM_PACF:
            success = Tests.correlogramPacf(timeSeries, inputJson, outputJson)
        elif action == Constants.ACTION_ARCH_TEST:
            success = Tests.archTest(timeSeries, inputJson, outputJson)
        elif action == Constants.ACTION_LJUNG_BOX_TEST:
            success = Tests.ljungBoxTest(timeSeries, inputJson, outputJson)
        # Tests end
        #
        #
        # Transformations
        elif action == Constants.ACTION_DIFFERENCE:
            success = Transformations.difference(timeSeries, inputJson, outputJson)
        elif action == Constants.ACTION_LOGARITHM:
            success = Transformations.logarithm(timeSeries, inputJson, outputJson)
        elif action == Constants.ACTION_NORMALIZATION:
            success = Transformations.normalization(timeSeries, inputJson, outputJson)
        elif action == Constants.ACTION_STANDARDIZATION:
            success = Transformations.standardization(timeSeries, inputJson, outputJson)
        # Transformations end
        #
        #
        # Models
        elif action == Constants.ACTION_ARIMA:
            success = Models.arima(timeSeries, inputJson, outputJson)
        elif action == Constants.ACTION_SIMPLE_EXP_SMOOTHING:
            success = Models.simpleExpSmoothing(timeSeries, inputJson, outputJson)
        elif action == Constants.ACTION_HOLT_WINTER:
            success = Models.holtWinter(timeSeries, inputJson, outputJson)
        # Models End
        #
        #
        # Other
        else:
            success = False
        # Other end
        #

    outputJson[Constants.OUTPUT_SUCCESS_KEY] = success
    if success:
        Tests.evaluatePValue(inputJson, outputJson)

    outputJsonData = json.dumps(outputJson)

    with open(outputJsonFilePath, 'w') as outputFile:
        outputFile.write(outputJsonData)

    print("\n============================================================ INPUT JSON ============================================================")
    print(formatJson(inputJson))
    print("========================================================== INPUT JSON END ==========================================================")

    print("\n=========================================================== OUTPUT JSON ============================================================")
    print(formatJson(outputJson))
    print("========================================================== OUTPUT JSON END ==========================================================")

if __name__ == "__main__":
    if Constants.DEBUG:
        Debug.debug()
        sys.exit(0)

    sys.stdout.reconfigure(encoding = 'utf-8')

    try:
        fileName = ""
        if len(sys.argv) > 1:
            fileName = sys.argv[1]
        else:
            fileName = "debug.json"

        executeAction(fileName)
    except Exception as exception:
        print(exception)
        sys.exit(1)

    sys.exit(0)
