import Constants

import json
import pandas as pd
import numpy as np

from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import kpss
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.stats.diagnostic import het_arch
from statsmodels.stats.diagnostic import acorr_ljungbox

from scipy.signal import periodogram as scipy_periodogram

def convertToJsonArray(array):
    listArray = array.tolist()
    return [None if np.isnan(x) else x for x in listArray]

def buildArguments(inputJson, keys):
    args = {}

    for key in keys:
        if key in inputJson:
            if inputJson[key] == "None":
                args[key] = None
            else:
                args[key] = inputJson[key]

    print("\n=============================================================== ARGS ===============================================================")
    print(json.dumps(args, ensure_ascii = False, indent = 4))
    print("============================================================= ARGS END =============================================================")

    return args

def dickeyFullerTest(timeSeries, inputJson, outputJson):
    try:
        args = (buildArguments(inputJson, ["maxlag", "regression", "autolag"]))
        result = adfuller(timeSeries.values, **args)

        outputJson[Constants.OUTPUT_P_VALUE_KEY] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: Constants.OUTPUT_P_VALUE_TITLE_VALUE,
            Constants.OUTPUT_ELEMENT_RESULT_KEY: result[1]
        }
        outputJson[Constants.OUTPUT_TEST_STATISTIC_KEY] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: Constants.OUTPUT_TEST_STATISTIC_TITLE_VALUE,
            Constants.OUTPUT_ELEMENT_RESULT_KEY: result[0]
        }

        outputJson["used_lag"] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: "počet použitých lagov",
            Constants.OUTPUT_ELEMENT_RESULT_KEY: result[2]
        }
        outputJson["nobs"] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: "počet použitých pozorovaní pre ADF regresiu a výpočet kritických hodnôt",
            Constants.OUTPUT_ELEMENT_RESULT_KEY: result[3]
        }
        outputJson["critical_values"] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: "kritické hodnoty",
            Constants.OUTPUT_ELEMENT_RESULT_KEY: result[4]
        }

        outputJson[Constants.OUTPUT_NULL_HYPOTHESIS_KEY] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: Constants.OUTPUT_NULL_HYPOTHESIS_TITLE_VALUE,
            Constants.OUTPUT_ELEMENT_RESULT_KEY: "časový rad nie je stacionárny"
        }
        outputJson[Constants.OUTPUT_ALTERNATIVE_HYPOTHESIS_KEY] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: Constants.OUTPUT_ALTERNATIVE_HYPOTHESIS_TITLE_VALUE,
            Constants.OUTPUT_ELEMENT_RESULT_KEY: "časový rad je stacionárny"
        }
    except Exception as exception:
        outputJson[Constants.OUT_EXCEPTION_KEY] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: Constants.OUT_EXCEPTION_TITLE_VALUE,
            Constants.OUTPUT_ELEMENT_RESULT_KEY: str(exception)
        }
        return False

    return True

def kpssTest(timeSeries, inputJson, outputJson):
    try:
        args = (buildArguments(inputJson, ["regression", "nlags"]))
        result = kpss(timeSeries.values, **args)

        outputJson[Constants.OUTPUT_P_VALUE_KEY] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: Constants.OUTPUT_P_VALUE_TITLE_VALUE,
            Constants.OUTPUT_ELEMENT_RESULT_KEY: result[1]
        }
        outputJson[Constants.OUTPUT_TEST_STATISTIC_KEY] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: Constants.OUTPUT_TEST_STATISTIC_TITLE_VALUE,
            Constants.OUTPUT_ELEMENT_RESULT_KEY: result[0]
        }

        outputJson["lags"] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: "počet použitých lagov",
            Constants.OUTPUT_ELEMENT_RESULT_KEY: result[2]
        }
        outputJson["crit"] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: "kritické hodnoty",
            Constants.OUTPUT_ELEMENT_RESULT_KEY: result[3]
        }

        outputJson[Constants.OUTPUT_NULL_HYPOTHESIS_KEY] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: Constants.OUTPUT_NULL_HYPOTHESIS_TITLE_VALUE,
            Constants.OUTPUT_ELEMENT_RESULT_KEY: "časový rad je trendovo stacionárny"
        }
        outputJson[Constants.OUTPUT_ALTERNATIVE_HYPOTHESIS_KEY] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: Constants.OUTPUT_ALTERNATIVE_HYPOTHESIS_TITLE_VALUE,
            Constants.OUTPUT_ELEMENT_RESULT_KEY: "časový rad nie je trendovo stacionárny"
        }
    except Exception as exception:
        outputJson[Constants.OUT_EXCEPTION_KEY] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: Constants.OUT_EXCEPTION_TITLE_VALUE,
            Constants.OUTPUT_ELEMENT_RESULT_KEY: str(exception)
        }
        return False

    return True

def seasonalDecompose(timeSeries, inputJson, outputJson):
    try:
        args = (buildArguments(inputJson, ["model", "period"]))
        result = seasonal_decompose(timeSeries.values, **args)

        outputJson["observed"] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: "pozorované hodnoty",
            Constants.OUTPUT_ELEMENT_RESULT_KEY: convertToJsonArray(result.observed)
        }
        outputJson["trend"] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: "trend",
            Constants.OUTPUT_ELEMENT_RESULT_KEY: convertToJsonArray(result.trend)
        }
        outputJson["seasonal"] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: "sezónna zložka",
            Constants.OUTPUT_ELEMENT_RESULT_KEY: convertToJsonArray(result.seasonal)
        }
        outputJson["resid"] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: "reziduá",
            Constants.OUTPUT_ELEMENT_RESULT_KEY: convertToJsonArray(result.resid)
        }
    except Exception as exception:
        outputJson[Constants.OUT_EXCEPTION_KEY] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: Constants.OUT_EXCEPTION_TITLE_VALUE,
            Constants.OUTPUT_ELEMENT_RESULT_KEY: str(exception)
        }
        return False

    return True

def periodogram(timeSeries, inputJson, outputJson):
    try:
        frequencies, power = scipy_periodogram(timeSeries.values)

        outputJson["frequency"] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: "frekvencia",
            Constants.OUTPUT_ELEMENT_RESULT_KEY: convertToJsonArray(frequencies)
        }
        outputJson["power"] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: "sila",
            Constants.OUTPUT_ELEMENT_RESULT_KEY: convertToJsonArray(power)
        }
    except Exception as exception:
        outputJson[Constants.OUT_EXCEPTION_KEY] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: Constants.OUT_EXCEPTION_TITLE_VALUE,
            Constants.OUTPUT_ELEMENT_RESULT_KEY: str(exception)
        }
        return False

    return True

def archTest(timeSeries, inputJson, outputJson):
    try:
        args = (buildArguments(inputJson, ["nlags", "ddof"]))
        result = het_arch(timeSeries.values, **args)

        outputJson[Constants.OUTPUT_P_VALUE_KEY] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: Constants.OUTPUT_P_VALUE_TITLE_VALUE,
            Constants.OUTPUT_ELEMENT_RESULT_KEY: result[1]
        }
        outputJson[Constants.OUTPUT_TEST_STATISTIC_KEY] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: Constants.OUTPUT_TEST_STATISTIC_TITLE_VALUE,
            Constants.OUTPUT_ELEMENT_RESULT_KEY: result[0]
        }

        outputJson["fval"] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: "testovacia štatistika F testu",
            Constants.OUTPUT_ELEMENT_RESULT_KEY: result[2]
        }
        outputJson["fpval"] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: "p-hodnota F testu",
            Constants.OUTPUT_ELEMENT_RESULT_KEY: result[3]
        }

        outputJson[Constants.OUTPUT_NULL_HYPOTHESIS_KEY] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: Constants.OUTPUT_NULL_HYPOTHESIS_TITLE_VALUE,
            Constants.OUTPUT_ELEMENT_RESULT_KEY: "reziduá nevykazujú známky heteroskedasticity"
        }
        outputJson[Constants.OUTPUT_ALTERNATIVE_HYPOTHESIS_KEY] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: Constants.OUTPUT_ALTERNATIVE_HYPOTHESIS_TITLE_VALUE,
            Constants.OUTPUT_ELEMENT_RESULT_KEY: "reziduá vykazujú známky heteroskedasticity"
        }
    except Exception as exception:
        outputJson[Constants.OUT_EXCEPTION_KEY] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: Constants.OUT_EXCEPTION_TITLE_VALUE,
            Constants.OUTPUT_ELEMENT_RESULT_KEY: str(exception)
        }
        return False

    return True

def ljungBoxTest(timeSeries, inputJson, outputJson):
    try:
        args = (buildArguments(inputJson, ["period", "lags", "auto_lag", "model_df"]))
        result = acorr_ljungbox(timeSeries.values, **args)

        if pd.isna(result.iloc[-1]['lb_pvalue']):
            outputPValue = -1
        else:
            outputPValue = result.iloc[-1]['lb_pvalue']

        outputJson[Constants.OUTPUT_P_VALUE_KEY] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: Constants.OUTPUT_P_VALUE_TITLE_VALUE,
            Constants.OUTPUT_ELEMENT_RESULT_KEY: outputPValue
        }
        outputJson[Constants.OUTPUT_TEST_STATISTIC_KEY] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: Constants.OUTPUT_TEST_STATISTIC_TITLE_VALUE,
            Constants.OUTPUT_ELEMENT_RESULT_KEY: result.iloc[-1]['lb_stat']
        }

        outputJson["lags_used"] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: "počet použitých lagov",
            Constants.OUTPUT_ELEMENT_RESULT_KEY: str(result.index[-1])
        }

        outputJson[Constants.OUTPUT_NULL_HYPOTHESIS_KEY] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: Constants.OUTPUT_NULL_HYPOTHESIS_TITLE_VALUE,
            Constants.OUTPUT_ELEMENT_RESULT_KEY: "reziduá sú nezávisle rozdelené"
        }
        outputJson[Constants.OUTPUT_ALTERNATIVE_HYPOTHESIS_KEY] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: Constants.OUTPUT_ALTERNATIVE_HYPOTHESIS_TITLE_VALUE,
            Constants.OUTPUT_ELEMENT_RESULT_KEY: "reziduá nie sú nezávisle rozdelené, vykazujú sériovú koreláciu"
        }
    except Exception as exception:
        outputJson[Constants.OUT_EXCEPTION_KEY] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: Constants.OUT_EXCEPTION_TITLE_VALUE,
            Constants.OUTPUT_ELEMENT_RESULT_KEY: str(exception)
        }
        return False

    return True