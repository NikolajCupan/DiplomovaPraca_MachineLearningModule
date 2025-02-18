import Constants
import Helper
import Tests

import numpy as np
import pandas as pd

from math import sqrt

from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

def performLjungBoxTest(inputJson, timeSeries):
    outputJson = {}

    success = Tests.ljungBoxTest(timeSeries, inputJson, outputJson)
    Tests.evaluatePValue(inputJson, outputJson)

    outputJson[Constants.OUTPUT_SUCCESS_KEY] = success
    return outputJson

def performArchTest(inputJson, timeSeries):
    outputJson = {}

    success = Tests.archTest(timeSeries, inputJson, outputJson)
    Tests.evaluatePValue(inputJson, outputJson)

    outputJson[Constants.OUTPUT_SUCCESS_KEY] = success
    return outputJson

def getAccuracy(real, fitted):
    if len(real) != len(fitted):
        return {}

    outputJson = {
        "mse": mean_squared_error(real, fitted),
        "rmse": sqrt(mean_squared_error(real, fitted)),
        "mae": mean_absolute_error(real, fitted),
        "r2": r2_score(real, fitted)
    }
    return outputJson

def arima(timeSeries, inputJson, outputJson):
    try:
        args = Helper.buildArguments(inputJson, [
            Constants.PYTHON_FREQUENCY_TYPE_KEY,
            Constants.FREQUENCY_TYPE_KEY,
            "train_percent", "season_length", "normal_p", "normal_d", "normal_q", "seasonal_p", "seasonal_q", "seasonal_d",
            Constants.FORECAST_COUNT_KEY
        ])

        trainSize = int(len(timeSeries) * (args["train_percent"] / 100))
        trainSet, testSet = timeSeries[:trainSize], timeSeries[trainSize:]

        model = SARIMAX(
            trainSet.values,
            order = (args["normal_p"], args["normal_d"], args["normal_q"]),
            seasonal_order = (args["seasonal_p"], args["seasonal_d"], args["seasonal_q"], args["season_length"])
        )

        trainResult = model.fit()
        outputJson["train_accuracy"] = getAccuracy(trainSet.values, trainResult.fittedvalues)

        outputJson[Constants.FREQUENCY_TYPE_KEY] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: "frekvencia",
            Constants.OUTPUT_ELEMENT_RESULT_KEY: args[Constants.FREQUENCY_TYPE_KEY]
        }
        outputJson[Constants.OUTPUT_SUMMARY_KEY] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: "výsledok",
            Constants.OUTPUT_ELEMENT_RESULT_KEY: str(trainResult.summary())
        }

        outputJson[Constants.OUTPUT_TRAIN_KEY] = {
            Constants.MODEL_DATE_KEY: Helper.convertToJsonDatesArray(trainSet.index),
            Constants.MODEL_REAL_KEY: Helper.convertToJsonArray(trainSet),
            Constants.MODEL_FITTED_KEY: Helper.convertToJsonArray(trainResult.fittedvalues),
            Constants.MODEL_RESIDUALS_KEY: Helper.convertToJsonArray(trainResult.resid)
        }


        if len(testSet) > 0:
            testFittedValues = trainResult.forecast(steps = len(testSet))
            testResiduals = testSet.values - testFittedValues

            outputJson[Constants.OUTPUT_TEST_KEY] = {
                Constants.MODEL_DATE_KEY: Helper.convertToJsonDatesArray(testSet.index),
                Constants.MODEL_REAL_KEY: Helper.convertToJsonArray(testSet),
                Constants.MODEL_FITTED_KEY: Helper.convertToJsonArray(testFittedValues),
                Constants.MODEL_RESIDUALS_KEY: Helper.convertToJsonArray(testResiduals)
            }
            outputJson["test_accuracy"] = getAccuracy(testSet.values, testFittedValues)


        if len(testSet) + args[Constants.FORECAST_COUNT_KEY] > 0:
            allForecast = trainResult.forecast(
                steps = len(testSet) + args[Constants.FORECAST_COUNT_KEY]
            )
            allFittedValues = np.concatenate((trainResult.fittedvalues, allForecast), axis = 0)
            allIndex = pd.date_range(
                start = timeSeries.index[0], periods = len(allFittedValues), freq = args[Constants.PYTHON_FREQUENCY_TYPE_KEY]
            )

            outputJson[Constants.OUTPUT_FORECAST_KEY] = {
                Constants.MODEL_DATE_KEY: Helper.convertToJsonDatesArray(allIndex),
                Constants.MODEL_REAL_KEY: Helper.convertToJsonArray(timeSeries),
                Constants.MODEL_FITTED_KEY: Helper.convertToJsonArray(allFittedValues)
            }
        else:
            outputJson[Constants.OUTPUT_FORECAST_KEY] = {
                Constants.MODEL_DATE_KEY: Helper.convertToJsonDatesArray(trainSet.index),
                Constants.MODEL_REAL_KEY: Helper.convertToJsonArray(trainSet),
                Constants.MODEL_FITTED_KEY: Helper.convertToJsonArray(trainResult.fittedvalues)
            }

        outputJson["ljung_box_test"] = performLjungBoxTest(inputJson, trainSet)
        outputJson["arch_test"] = performArchTest(inputJson, trainSet)
    except Exception as exception:
        outputJson[Constants.OUT_EXCEPTION_KEY] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: Constants.OUT_EXCEPTION_TITLE_VALUE,
            Constants.OUTPUT_ELEMENT_RESULT_KEY: str(exception)
        }
        return False

    return True
