import Constants

import json
import pandas as pd

from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import kpss
from statsmodels.stats.diagnostic import acorr_ljungbox

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

        outputJson[Constants.OUTPUT_TEST_STATISTIC_KEY] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: Constants.OUTPUT_TEST_STATISTIC_TITLE_VALUE,
            Constants.OUTPUT_ELEMENT_RESULT_KEY: result[0]
        }
        outputJson[Constants.OUTPUT_P_VALUE_KEY] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: Constants.OUTPUT_P_VALUE_TITLE_VALUE,
            Constants.OUTPUT_ELEMENT_RESULT_KEY: result[1]
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

        outputJson[Constants.OUTPUT_TEST_STATISTIC_KEY] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: Constants.OUTPUT_TEST_STATISTIC_TITLE_VALUE,
            Constants.OUTPUT_ELEMENT_RESULT_KEY: result[0]
        }
        outputJson[Constants.OUTPUT_P_VALUE_KEY] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: Constants.OUTPUT_P_VALUE_TITLE_VALUE,
            Constants.OUTPUT_ELEMENT_RESULT_KEY: result[1]
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

def ljungBoxTest(timeSeries, inputJson, outputJson):
    try:
        args = (buildArguments(inputJson, ["period", "lags", "auto_lag", "model_df"]))
        result = acorr_ljungbox(timeSeries.values, **args)

        if pd.isna(result.iloc[-1]['lb_pvalue']):
            outputPValue = -1
        else:
            outputPValue = result.iloc[-1]['lb_pvalue']

        outputJson[Constants.OUTPUT_TEST_STATISTIC_KEY] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: Constants.OUTPUT_TEST_STATISTIC_TITLE_VALUE,
            Constants.OUTPUT_ELEMENT_RESULT_KEY: result.iloc[-1]['lb_stat']
        }
        outputJson[Constants.OUTPUT_P_VALUE_KEY] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: Constants.OUTPUT_P_VALUE_TITLE_VALUE,
            Constants.OUTPUT_ELEMENT_RESULT_KEY: outputPValue
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