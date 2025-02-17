import numpy as np
import pandas as pd

import Constants
import Helper

from statsmodels.tsa.arima.model import ARIMA

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

        model = ARIMA(
            trainSet.values,
            order = (args["normal_p"], args["normal_d"], args["normal_q"]),
            seasonal_order = (args["seasonal_p"], args["seasonal_d"], args["seasonal_q"], args["season_length"])
        )

        trainResult = model.fit()

        testFittedValues = trainResult.forecast(steps = len(testSet))
        testResiduals = testSet.values - testFittedValues


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
        outputJson[Constants.OUTPUT_TEST_KEY] = {
            Constants.MODEL_DATE_KEY: Helper.convertToJsonDatesArray(testSet.index),
            Constants.MODEL_REAL_KEY: Helper.convertToJsonArray(testSet),
            Constants.MODEL_FITTED_KEY: Helper.convertToJsonArray(testFittedValues),
            Constants.MODEL_RESIDUALS_KEY: Helper.convertToJsonArray(testResiduals)
        }


        if args[Constants.FORECAST_COUNT_KEY] != 0:
            forecast = trainResult.forecast(
                steps = len(testSet) + args[Constants.FORECAST_COUNT_KEY]
            )

            allFittedValues = np.concatenate((trainResult.fittedvalues, forecast), axis = 0)
            allIndex = pd.date_range(
                start = timeSeries.index[0], periods = len(allFittedValues), freq = args[Constants.PYTHON_FREQUENCY_TYPE_KEY]
            )

            outputJson[Constants.OUTPUT_FORECAST_KEY] = {
                Constants.MODEL_DATE_KEY: Helper.convertToJsonDatesArray(allIndex),
                Constants.MODEL_REAL_KEY: Helper.convertToJsonArray(timeSeries),
                Constants.MODEL_FITTED_KEY: Helper.convertToJsonArray(allFittedValues)
            }

        # print(result.summary())
        #
        # fitted_values = result.fittedvalues
        # forecast = result.forecast(steps=len(testSet))
        # forecast = result.forecast(steps=20)
        #
        # plt.plot(timeSeries.index, timeSeries.values, label='Real')
        # plt.plot(trainSet.index, fitted_values, label='Fitted', linestyle='--')
        # plt.plot(testSet.index, forecast, label='Forecast', linestyle='--', color='red')
        # plt.plot(pd.date_range(testSet.index[-1], periods=21, freq='MS')[1:], forecast, label='Future Forecast',
        #          linestyle='--', color='green')
        # plt.legend()
        # plt.show()
    except Exception as exception:
        outputJson[Constants.OUT_EXCEPTION_KEY] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: Constants.OUT_EXCEPTION_TITLE_VALUE,
            Constants.OUTPUT_ELEMENT_RESULT_KEY: str(exception)
        }
        return False

    return True
