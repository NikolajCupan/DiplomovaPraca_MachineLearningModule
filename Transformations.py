import Constants
import Helper

import csv

import pandas as pd

def saveToFile(timeSeries):
    fileName = Helper.getRandomString(Constants.RANDOM_STRING_LENGTH)
    fullOutputPath = Helper.getFullOutputPath(fileName + ".csv")

    with open(fullOutputPath, mode = "w", newline = "") as file:
        writer = csv.writer(file)

        for date, data in timeSeries.items():
            writer.writerow([Helper.formatDate(date), data])

    return fullOutputPath

def difference(timeSeries, inputJson, outputJson):
    try:
        args = Helper.buildArguments(inputJson, ["difference_level", Constants.FREQUENCY_TYPE_KEY])

        elementsCount = timeSeries.count()
        differencesCount = args["difference_level"]

        if elementsCount - differencesCount < 10:
            outputJson[Constants.OUT_EXCEPTION_KEY] = {
                Constants.OUTPUT_ELEMENT_TITLE_KEY: Constants.OUT_EXCEPTION_TITLE_VALUE,
                Constants.OUTPUT_ELEMENT_RESULT_KEY: "Po vykonaní diferencie by dataset obsahoval menej ako 10 pozorovaní"
            }
            return False

        timeSeriesDifference = timeSeries
        for i in range(args["difference_level"]):
            timeSeriesDifference = timeSeriesDifference.diff()
            timeSeriesDifference.dropna(inplace = True)

        timeSeriesDifferenceStart = timeSeriesDifference.index.min()
        timeSeriesDifferenceEnd = timeSeriesDifference.index.max()
        timeSeriesDifferenceFrequency = args[Constants.FREQUENCY_TYPE_KEY]

        fullDatesRange = pd.date_range(start = timeSeriesDifferenceStart, end = timeSeriesDifferenceEnd, freq = timeSeriesDifferenceFrequency)
        timeSeriesDifference = timeSeriesDifference.reindex(fullDatesRange, fill_value = "-")

        fileName = saveToFile(timeSeriesDifference)

        outputJson[Constants.OUTPUT_TRANSFORMED_FILE_NAME_KEY] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: Constants.OUTPUT_TRANSFORMED_FILE_NAME_TITLE_VALUE,
            Constants.OUTPUT_ELEMENT_RESULT_KEY: fileName
        }
        outputJson[Constants.OUTPUT_START_DATE_TIME_KEY] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: Constants.OUTPUT_START_DATE_TIME_TITLE_VALUE,
            Constants.OUTPUT_ELEMENT_RESULT_KEY: Helper.formatDate(timeSeriesDifferenceStart)
        }
    except Exception as exception:
        outputJson[Constants.OUT_EXCEPTION_KEY] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: Constants.OUT_EXCEPTION_TITLE_VALUE,
            Constants.OUTPUT_ELEMENT_RESULT_KEY: str(exception)
        }
        return False

    return True

def logarithm(timeSeries, inputJson, outputJson):
    return

def normalization(timeSeries, inputJson, outputJson):
    return

def standardization(timeSeries, inputJson, outputJson):
    return
