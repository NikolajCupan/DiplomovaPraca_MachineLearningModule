import Constants
import Debug
import Helper

import Models
import Tests
import Transformations

import sys
import json

def executeAction(jsonFileName):
    inputJsonFilePath = Helper.getFullInputPath(jsonFileName)
    outputJsonFilePath = Helper.getFullOutputPath(jsonFileName)

    outputJson = {}

    with open(inputJsonFilePath) as inputFile:
        inputJson = json.load(inputFile)
        action = inputJson[Constants.INPUT_ACTION_KEY]
        timeSeries = Helper.getTimeSeries(inputJson[Constants.INPUT_FILE_NAME_KEY])

        #
        # Debug
        if action == Constants.ACTION_DEBUG:
            Debug.debug(timeSeries, inputJson, outputJson)
        # Debug end
        #
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
        elif action == Constants.ACTION_DOUBLE_EXP_SMOOTHING:
            success = Models.doubleExpSmoothing(timeSeries, inputJson, outputJson)
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
    print(Helper.formatJson(inputJson))
    print("========================================================== INPUT JSON END ==========================================================")

    print("\n=========================================================== OUTPUT JSON ============================================================")
    print(Helper.formatJson(outputJson))
    print("========================================================== OUTPUT JSON END ==========================================================")

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding = 'utf-8')

    try:
        fileName = ""
        if len(sys.argv) > 1:
            fileName = sys.argv[1]
        else:
            fileName = Constants.DEBUG_FILE_NAME

        executeAction(fileName)
    except Exception as exception:
        print(exception)
        sys.exit(1)

    sys.exit(0)
