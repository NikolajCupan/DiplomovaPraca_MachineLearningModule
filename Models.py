import Constants
import Helper

from statsmodels.tsa.arima.model import ARIMA

def arima(timeSeries, inputJson, outputJson):
    try:
        args = Helper.buildArguments(inputJson, [
            Constants.FREQUENCY_TYPE_KEY, "train_percent", "season_length", "normal_p", "normal_d", "normal_q", "seasonal_p", "seasonal_q", "seasonal_d"
        ])

        trainSize = int(len(timeSeries) * (args["train_percent"] / 100))
        train, test = timeSeries[:trainSize], timeSeries[trainSize:]

        model = ARIMA(
            train.values,
            order = (args["normal_p"], args["normal_d"], args["normal_q"]),
            seasonal_order = (args["seasonal_p"], args["seasonal_d"], args["seasonal_q"], args["season_length"])
        )
        result = model.fit()

        outputJson[Constants.FREQUENCY_TYPE_KEY] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: "frekvencia",
            Constants.OUTPUT_ELEMENT_RESULT_KEY: args[Constants.FREQUENCY_TYPE_KEY]
        }
        outputJson[Constants.OUTPUT_SUMMARY_KEY] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: "výsledok",
            Constants.OUTPUT_ELEMENT_RESULT_KEY: str(result.summary())
        }

        outputJson[Constants.OUTPUT_TRAIN_KEY] = {
            Constants.MODEL_DATE_KEY: Helper.convertToJsonDatesArray(train.index),
            Constants.MODEL_REAL_KEY: Helper.convertToJsonArray(train),
            Constants.MODEL_FITTED_KEY: Helper.convertToJsonArray(result.fittedvalues),
            Constants.MODEL_RESIDUALS_KEY: Helper.convertToJsonArray(result.resid)
        }

        # print(result.summary())
        #
        # fitted_values = result.fittedvalues
        # forecast = result.forecast(steps=len(test))
        # future_forecast = result.forecast(steps=20)
        #
        # plt.plot(timeSeries.index, timeSeries.values, label='Real')
        # plt.plot(train.index, fitted_values, label='Fitted', linestyle='--')
        # plt.plot(test.index, forecast, label='Forecast', linestyle='--', color='red')
        # plt.plot(pd.date_range(test.index[-1], periods=21, freq='MS')[1:], future_forecast, label='Future Forecast',
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
