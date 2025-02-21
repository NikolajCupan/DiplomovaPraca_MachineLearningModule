import Constants
import Helper
import Tests

import numpy as np
import pandas as pd

from math import sqrt

from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.api import SimpleExpSmoothing
from statsmodels.tsa.api import Holt
from statsmodels.tsa.holtwinters import ExponentialSmoothing

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

def processModelResult(inputJson, timeSeries, trainSet, testSet, trainResult, outputJson):
    outputJson["train_accuracy"] = getAccuracy(trainSet.values, trainResult.fittedvalues)

    outputJson[Constants.INPUT_FREQUENCY_TYPE_KEY] = {
        Constants.OUTPUT_ELEMENT_TITLE_KEY: "frekvencia",
        Constants.OUTPUT_ELEMENT_RESULT_KEY: inputJson[Constants.INPUT_FREQUENCY_TYPE_KEY]
    }
    outputJson[Constants.OUTPUT_SUMMARY_KEY] = {
        Constants.OUTPUT_ELEMENT_TITLE_KEY: "výsledok",
        Constants.OUTPUT_ELEMENT_RESULT_KEY: str(trainResult.summary())
    }

    outputJson[Constants.OUTPUT_TRAIN_KEY] = {
        Constants.OUTPUT_MODEL_DATE_KEY: Helper.convertToJsonDatesArray(trainSet.index),
        Constants.OUTPUT_MODEL_REAL_KEY: Helper.convertToJsonArray(trainSet),
        Constants.OUTPUT_MODEL_FITTED_KEY: Helper.convertToJsonArray(trainResult.fittedvalues),
        Constants.OUTPUT_MODEL_RESIDUALS_KEY: Helper.convertToJsonArray(trainResult.resid)
    }

    if len(testSet) > 0:
        testFittedValues = trainResult.forecast(steps = len(testSet))
        testResiduals = testSet.values - testFittedValues

        outputJson[Constants.OUTPUT_TEST_KEY] = {
            Constants.OUTPUT_MODEL_DATE_KEY: Helper.convertToJsonDatesArray(testSet.index),
            Constants.OUTPUT_MODEL_REAL_KEY: Helper.convertToJsonArray(testSet),
            Constants.OUTPUT_MODEL_FITTED_KEY: Helper.convertToJsonArray(testFittedValues),
            Constants.OUTPUT_MODEL_RESIDUALS_KEY: Helper.convertToJsonArray(testResiduals)
        }
        outputJson["test_accuracy"] = getAccuracy(testSet.values, testFittedValues)

    if len(testSet) + inputJson[Constants.INPUT_FORECAST_COUNT_KEY] > 0:
        allForecast = trainResult.forecast(
            steps = len(testSet) + inputJson[Constants.INPUT_FORECAST_COUNT_KEY]
        )
        allFittedValues = np.concatenate((trainResult.fittedvalues, allForecast), axis = 0)
        allIndex = pd.date_range(
            start = timeSeries.index[0], periods = len(allFittedValues), freq = inputJson[Constants.INPUT_PYTHON_FREQUENCY_TYPE_KEY]
        )

        outputJson[Constants.OUTPUT_FORECAST_KEY] = {
            Constants.OUTPUT_MODEL_DATE_KEY: Helper.convertToJsonDatesArray(allIndex),
            Constants.OUTPUT_MODEL_REAL_KEY: Helper.convertToJsonArray(timeSeries),
            Constants.OUTPUT_MODEL_FITTED_KEY: Helper.convertToJsonArray(allFittedValues)
        }
    else:
        outputJson[Constants.OUTPUT_FORECAST_KEY] = {
            Constants.OUTPUT_MODEL_DATE_KEY: Helper.convertToJsonDatesArray(trainSet.index),
            Constants.OUTPUT_MODEL_REAL_KEY: Helper.convertToJsonArray(trainSet),
            Constants.OUTPUT_MODEL_FITTED_KEY: Helper.convertToJsonArray(trainResult.fittedvalues)
        }

def arima(timeSeries, inputJson, outputJson):
    try:
        trainSize = int(len(timeSeries) * (inputJson["train_percent"] / 100))
        trainSet, testSet = timeSeries[:trainSize], timeSeries[trainSize:]

        model = ARIMA(
            trainSet.values,
            order = (inputJson["normal_p"], inputJson["normal_d"], inputJson["normal_q"]),
            seasonal_order = (inputJson["seasonal_p"], inputJson["seasonal_d"], inputJson["seasonal_q"], inputJson["season_length"])
        )

        trainResult = model.fit()
        processModelResult(inputJson, timeSeries, trainSet, testSet, trainResult, outputJson)

        outputJson["ljung_box_test"] = performLjungBoxTest(inputJson, trainSet)
        outputJson["arch_test"] = performArchTest(inputJson, trainSet)
    except Exception as exception:
        outputJson[Constants.OUTPUT_EXCEPTION_KEY] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: Constants.OUTPUT_EXCEPTION_TITLE_VALUE,
            Constants.OUTPUT_ELEMENT_RESULT_KEY: str(exception)
        }
        return False

    return True

def simpleExpSmoothing(timeSeries, inputJson, outputJson):
    try:
        trainSize = int(len(timeSeries) * (inputJson["train_percent"] / 100))
        trainSet, testSet = timeSeries[:trainSize], timeSeries[trainSize:]

        model = SimpleExpSmoothing(
            trainSet.values
        )

        trainResult = model.fit(
            smoothing_level = inputJson["alpha"]
        )
        processModelResult(inputJson, timeSeries, trainSet, testSet, trainResult, outputJson)
    except Exception as exception:
        outputJson[Constants.OUTPUT_EXCEPTION_KEY] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: Constants.OUTPUT_EXCEPTION_TITLE_VALUE,
            Constants.OUTPUT_ELEMENT_RESULT_KEY: str(exception)
        }
        return False

    return True

def doubleExpSmoothing(timeSeries, inputJson, outputJson):
    try:
        trainSize = int(len(timeSeries) * (inputJson["train_percent"] / 100))
        trainSet, testSet = timeSeries[:trainSize], timeSeries[trainSize:]

        model = Holt(
            trainSet.values
        )

        trainResult = model.fit(
            smoothing_level = inputJson["alpha"],
            smoothing_trend = inputJson["beta"]
        )
        processModelResult(inputJson, timeSeries, trainSet, testSet, trainResult, outputJson)
    except Exception as exception:
        outputJson[Constants.OUTPUT_EXCEPTION_KEY] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: Constants.OUTPUT_EXCEPTION_TITLE_VALUE,
            Constants.OUTPUT_ELEMENT_RESULT_KEY: str(exception)
        }
        return False

    return True

def holtWinter(timeSeries, inputJson, outputJson):
    try:
        trainSize = int(len(timeSeries) * (inputJson["train_percent"] / 100))
        trainSet, testSet = timeSeries[:trainSize], timeSeries[trainSize:]

        model = ExponentialSmoothing(
            trainSet.values,
            trend = inputJson["trend_type"],
            seasonal = inputJson["season_type"],
            seasonal_periods = inputJson["season_length"],
        )

        trainResult = model.fit(
            smoothing_level = inputJson["alpha"],
            smoothing_trend = inputJson["beta"],
            smoothing_seasonal = inputJson["gamma"]
        )
        processModelResult(inputJson, timeSeries, trainSet, testSet, trainResult, outputJson)
    except Exception as exception:
        outputJson[Constants.OUTPUT_EXCEPTION_KEY] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: Constants.OUTPUT_EXCEPTION_TITLE_VALUE,
            Constants.OUTPUT_ELEMENT_RESULT_KEY: str(exception)
        }
        return False

    return True
