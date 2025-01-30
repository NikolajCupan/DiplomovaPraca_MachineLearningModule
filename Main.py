import sys
import json
import os

import Constants
import Tests

def getFullInputPath(pJsonFileName):
    return os.path.join(Constants.PYTHON_BASE_DIRECTORY, Constants.BACKEND_BASE_DIRECTORY_PATH, Constants.DATASET_INPUT_PATH, pJsonFileName)

def getFullOutputPath(pJsonFileName):
    return os.path.join(Constants.PYTHON_BASE_DIRECTORY, Constants.BACKEND_BASE_DIRECTORY_PATH, Constants.DATASET_OUTPUT_PATH, pJsonFileName)

def executeAction(jsonFileName):
    inputJsonFilePath = getFullInputPath(jsonFileName)
    outputJsonFilePath = getFullOutputPath(jsonFileName)

    outputJson = {}
    success = True

    with open(inputJsonFilePath) as inputFile:
        inputJson = json.load(inputFile)
        action = inputJson["action"]

        if action == Constants.ACTION_DICKEY_FULLER_TEST:
            Tests.dickeyFullerTest(outputJson)
        elif action == Constants.ACTION_DUMMY:
            Tests.dickeyFullerTest(outputJson)
        else:
            success = False

    outputJson["success"] = success
    outputJsonData = json.dumps(outputJson)

    with open(outputJsonFilePath, 'w') as outputFile:
        outputFile.write(outputJsonData)

if __name__ == "__main__":
    try:
        executeAction(sys.argv[1])
    except:
        sys.exit(1)

    sys.exit(0)
