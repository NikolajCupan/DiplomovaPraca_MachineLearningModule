import Constants
import Helper

import csv

import numpy as np
import pandas as pd

def saveToFile(timeSeries):
    fileName = Helper.getRandomString(Constants.RANDOM_STRING_LENGTH)
    fullOutputPath = Helper.getFullOutputPath(fileName + ".csv")

    with open(fullOutputPath, mode = "w", newline = "") as file:
        writer = csv.writer(file)

        for date, data in timeSeries.items():
            writer.writerow([Helper.formatDate(date), data])

    return fullOutputPath

def processResult(timeSeries, args):
    timeSeriesStart = timeSeries.index.min()
    timeSeriesEnd = timeSeries.index.max()
    timeSeriesFrequency = args[Constants.PYTHON_FREQUENCY_TYPE_KEY]

    fullDatesRange = pd.date_range(start = timeSeriesStart, end = timeSeriesEnd, freq = timeSeriesFrequency)
    timeSeries = timeSeries.reindex(fullDatesRange, fill_value = "-")

    fileName = saveToFile(timeSeries)
    return fileName, timeSeriesStart

def difference(timeSeries, inputJson, outputJson):
    try:
        args = Helper.buildArguments(inputJson, ["difference_level", Constants.PYTHON_FREQUENCY_TYPE_KEY])

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

        fileName, timeSeriesDifferenceStart = processResult(timeSeriesDifference, args)
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
    try:
        args = Helper.buildArguments(inputJson, ["use_natural_log", "base", Constants.PYTHON_FREQUENCY_TYPE_KEY])

        if (timeSeries <= 0).any():
            outputJson[Constants.OUT_EXCEPTION_KEY] = {
                Constants.OUTPUT_ELEMENT_TITLE_KEY: Constants.OUT_EXCEPTION_TITLE_VALUE,
                Constants.OUTPUT_ELEMENT_RESULT_KEY: "Dataset obsahuje záporné hodnoty"
            }
            return False

        if "base" in args:
            baseValue = args["base"]
            timeSeries = np.log(timeSeries) / np.log(baseValue)
        else:
            timeSeries = np.log(timeSeries)

        fileName, timeSeriesStart = processResult(timeSeries, args)
        outputJson[Constants.OUTPUT_TRANSFORMED_FILE_NAME_KEY] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: Constants.OUTPUT_TRANSFORMED_FILE_NAME_TITLE_VALUE,
            Constants.OUTPUT_ELEMENT_RESULT_KEY: fileName
        }
        outputJson[Constants.OUTPUT_START_DATE_TIME_KEY] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: Constants.OUTPUT_START_DATE_TIME_TITLE_VALUE,
            Constants.OUTPUT_ELEMENT_RESULT_KEY: Helper.formatDate(timeSeriesStart)
        }
    except Exception as exception:
        outputJson[Constants.OUT_EXCEPTION_KEY] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: Constants.OUT_EXCEPTION_TITLE_VALUE,
            Constants.OUTPUT_ELEMENT_RESULT_KEY: str(exception)
        }
        return False

    return True

def normalization(timeSeries, inputJson, outputJson):
    def normalize(value, pTimeSeriesMin, pTimeSeriesMax, pMin, pMax):
        return (value - pTimeSeriesMin) / (pTimeSeriesMax - pTimeSeriesMin) * (pMax - pMin) + pMin

    try:
        args = Helper.buildArguments(inputJson, ["min", "max", Constants.PYTHON_FREQUENCY_TYPE_KEY])

        timeSeriesMin = min(timeSeries.values)
        timeSeriesMax = max(timeSeries.values)

        timeSeriesNormalized = [
            normalize(element, timeSeriesMin, timeSeriesMax, args["min"], args["max"])
            for element in timeSeries
        ]
        timeSeriesNormalized = pd.Series(timeSeriesNormalized, index = timeSeries.index)

        fileName, timeSeriesStart = processResult(timeSeriesNormalized, args)
        outputJson[Constants.OUTPUT_TRANSFORMED_FILE_NAME_KEY] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: Constants.OUTPUT_TRANSFORMED_FILE_NAME_TITLE_VALUE,
            Constants.OUTPUT_ELEMENT_RESULT_KEY: fileName
        }
        outputJson[Constants.OUTPUT_START_DATE_TIME_KEY] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: Constants.OUTPUT_START_DATE_TIME_TITLE_VALUE,
            Constants.OUTPUT_ELEMENT_RESULT_KEY: Helper.formatDate(timeSeriesStart)
        }
    except Exception as exception:
        outputJson[Constants.OUT_EXCEPTION_KEY] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: Constants.OUT_EXCEPTION_TITLE_VALUE,
            Constants.OUTPUT_ELEMENT_RESULT_KEY: str(exception)
        }
        return False

    return True

def standardization(timeSeries, inputJson, outputJson):
    def standardize(value, pTimeSeriesMean, pTimeSeriesStandardDeviation, pMean, pStandardDeviation):
        return (value - pTimeSeriesMean) / pTimeSeriesStandardDeviation * pStandardDeviation + pMean

    try:
        args = Helper.buildArguments(inputJson, ["mean", "standard_deviation", Constants.PYTHON_FREQUENCY_TYPE_KEY])

        timeSeriesMean = np.mean(timeSeries)
        timeSeriesStandardDeviation = np.std(timeSeries)

        timeSeriesStandardized = [
            standardize(element, timeSeriesMean, timeSeriesStandardDeviation, args["mean"], args["standard_deviation"])
            for element in timeSeries
        ]
        timeSeriesStandardized = pd.Series(timeSeriesStandardized, index = timeSeries.index)

        fileName, timeSeriesStart = processResult(timeSeriesStandardized, args)
        outputJson[Constants.OUTPUT_TRANSFORMED_FILE_NAME_KEY] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: Constants.OUTPUT_TRANSFORMED_FILE_NAME_TITLE_VALUE,
            Constants.OUTPUT_ELEMENT_RESULT_KEY: fileName
        }
        outputJson[Constants.OUTPUT_START_DATE_TIME_KEY] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: Constants.OUTPUT_START_DATE_TIME_TITLE_VALUE,
            Constants.OUTPUT_ELEMENT_RESULT_KEY: Helper.formatDate(timeSeriesStart)
        }
    except Exception as exception:
        outputJson[Constants.OUT_EXCEPTION_KEY] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: Constants.OUT_EXCEPTION_TITLE_VALUE,
            Constants.OUTPUT_ELEMENT_RESULT_KEY: str(exception)
        }
        return False

    return True