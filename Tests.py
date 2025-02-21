import Constants
import Helper

import pandas as pd
import numpy as np

from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import kpss
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import acf
from statsmodels.tsa.stattools import pacf
from statsmodels.stats.diagnostic import het_arch
from statsmodels.stats.diagnostic import acorr_ljungbox

from scipy.signal import periodogram as scipy_periodogram

def evaluatePValue(inputJson, outputJson):
    inputPValue = -1
    resultPValue = -1

    if Constants.OUTPUT_P_VALUE_KEY in outputJson:
        resultPValue = float(outputJson[Constants.OUTPUT_P_VALUE_KEY][Constants.OUTPUT_ELEMENT_RESULT_KEY])

    if Constants.INPUT_P_VALUE_KEY in inputJson:
        inputPValue = float(inputJson[Constants.INPUT_P_VALUE_KEY])

    outputJson[Constants.OUTPUT_USED_P_VALUE_KEY] = {
        Constants.OUTPUT_ELEMENT_TITLE_KEY: Constants.OUTPUT_USED_P_VALUE_TITLE_VALUE,
        Constants.OUTPUT_ELEMENT_RESULT_KEY: inputPValue
    }

    outputJson[Constants.OUTPUT_EVALUATION_KEY] = {
        Constants.OUTPUT_ELEMENT_TITLE_KEY: Constants.OUTPUT_EVALUATION_TITLE_VALUE,
        Constants.OUTPUT_ELEMENT_RESULT_KEY: ""
    }

    if inputPValue == -1 or resultPValue == -1:
        outputJson[Constants.OUTPUT_EVALUATION_KEY][Constants.OUTPUT_ELEMENT_RESULT_KEY] = "p-hodnoty nebolo možné vyhodnotiť"
        return

    if resultPValue < inputPValue:
        outputJson[Constants.OUTPUT_EVALUATION_KEY][Constants.OUTPUT_ELEMENT_RESULT_KEY] = "p-hodnota je nižšia ako zvolená hladina významnosti, zamietame nulovú hypotézu v prospech alternatívnej hypotézy"
    else:
        outputJson[Constants.OUTPUT_EVALUATION_KEY][Constants.OUTPUT_ELEMENT_RESULT_KEY] = "p-hodnota je rovná ale vyššia ako hladina významnosti, nezamietame nulovú hypotézu"

def dickeyFullerTest(timeSeries, inputJson, outputJson):
    try:
        args = Helper.buildArguments(inputJson, ["maxlag", "regression", "autolag"])
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
        outputJson[Constants.OUTPUT_EXCEPTION_KEY] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: Constants.OUTPUT_EXCEPTION_TITLE_VALUE,
            Constants.OUTPUT_ELEMENT_RESULT_KEY: str(exception)
        }
        return False

    return True

def kpssTest(timeSeries, inputJson, outputJson):
    try:
        args = Helper.buildArguments(inputJson, ["regression", "nlags"])
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
        outputJson[Constants.OUTPUT_EXCEPTION_KEY] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: Constants.OUTPUT_EXCEPTION_TITLE_VALUE,
            Constants.OUTPUT_ELEMENT_RESULT_KEY: str(exception)
        }
        return False

    return True

def seasonalDecompose(timeSeries, inputJson, outputJson):
    try:
        args = Helper.buildArguments(inputJson, ["model", "period"])
        result = seasonal_decompose(timeSeries.values, **args)

        outputJson["observed"] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: "pozorované hodnoty",
            Constants.OUTPUT_ELEMENT_RESULT_KEY: Helper.convertToJsonArray(result.observed)
        }
        outputJson["trend"] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: "trend",
            Constants.OUTPUT_ELEMENT_RESULT_KEY: Helper.convertToJsonArray(result.trend)
        }
        outputJson["seasonal"] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: "sezónna zložka",
            Constants.OUTPUT_ELEMENT_RESULT_KEY: Helper.convertToJsonArray(result.seasonal)
        }
        outputJson["resid"] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: "reziduá",
            Constants.OUTPUT_ELEMENT_RESULT_KEY: Helper.convertToJsonArray(result.resid)
        }
    except Exception as exception:
        outputJson[Constants.OUTPUT_EXCEPTION_KEY] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: Constants.OUTPUT_EXCEPTION_TITLE_VALUE,
            Constants.OUTPUT_ELEMENT_RESULT_KEY: str(exception)
        }
        return False

    return True

def periodogram(timeSeries, inputJson, outputJson):
    try:
        args = Helper.buildArguments(inputJson, ["fs", "nfft", "return_onesided", "scaling"])
        frequency, power = scipy_periodogram(timeSeries.values, **args)

        frequency, power = np.array(frequency[1:]), np.array(power[1:])
        period = 1 / frequency
        period = period[::-1]

        outputJson["power"] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: "sila",
            Constants.OUTPUT_ELEMENT_RESULT_KEY: Helper.convertToJsonArray(power)
        }
        outputJson["reversed_power"] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: "sila",
            Constants.OUTPUT_ELEMENT_RESULT_KEY: Helper.convertToJsonArray(power[::-1])
        }
        outputJson["frequency"] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: "frekvencia",
            Constants.OUTPUT_ELEMENT_RESULT_KEY: Helper.convertToJsonArray(frequency)
        }
        outputJson["period"] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: "perióda",
            Constants.OUTPUT_ELEMENT_RESULT_KEY: Helper.convertToJsonArray(period)
        }
    except Exception as exception:
        outputJson[Constants.OUTPUT_EXCEPTION_KEY] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: Constants.OUTPUT_EXCEPTION_TITLE_VALUE,
            Constants.OUTPUT_ELEMENT_RESULT_KEY: str(exception)
        }
        return False

    return True

def correlogramAcf(timeSeries, inputJson, outputJson):
    try:
        args = Helper.buildArguments(inputJson, ["adjusted", "nlags", "fft", "alpha", "bartlett_confint"])
        acfResult, confintResult = acf(timeSeries.values, **args)
        confintResultLowerBound, confintResultUpperBound = confintResult[:, 0], confintResult[:, 1]

        outputJson["acf_values"] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: "hodnoty acf",
            Constants.OUTPUT_ELEMENT_RESULT_KEY: Helper.convertToJsonArray(acfResult)
        }
        outputJson[Constants.OUTPUT_CONFIDENCE_INTERVAL_UPPER_BOUND_KEY] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: "interval spoľahlivosti horné ohraničenie",
            Constants.OUTPUT_ELEMENT_RESULT_KEY: Helper.convertToJsonArray(confintResultUpperBound)
        }
        outputJson[Constants.OUTPUT_CONFIDENCE_INTERVAL_LOWER_BOUND_KEY] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: "interval spoľahlivosti dolné ohraničenie",
            Constants.OUTPUT_ELEMENT_RESULT_KEY: Helper.convertToJsonArray(confintResultLowerBound)
        }
    except Exception as exception:
        outputJson[Constants.OUTPUT_EXCEPTION_KEY] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: Constants.OUTPUT_EXCEPTION_TITLE_VALUE,
            Constants.OUTPUT_ELEMENT_RESULT_KEY: str(exception)
        }
        return False

    return True

def correlogramPacf(timeSeries, inputJson, outputJson):
    try:
        args = Helper.buildArguments(inputJson, ["nlags", "method", "alpha"])
        pacfResult, confintResult = pacf(timeSeries.values, **args)
        confintResultLowerBound, confintResultUpperBound = confintResult[:, 0], confintResult[:, 1]

        outputJson["pacf_values"] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: "hodnoty pacf",
            Constants.OUTPUT_ELEMENT_RESULT_KEY: Helper.convertToJsonArray(pacfResult)
        }
        outputJson[Constants.OUTPUT_CONFIDENCE_INTERVAL_UPPER_BOUND_KEY] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: "interval spoľahlivosti horné ohraničenie",
            Constants.OUTPUT_ELEMENT_RESULT_KEY: Helper.convertToJsonArray(confintResultUpperBound)
        }
        outputJson[Constants.OUTPUT_CONFIDENCE_INTERVAL_LOWER_BOUND_KEY] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: "interval spoľahlivosti dolné ohraničenie",
            Constants.OUTPUT_ELEMENT_RESULT_KEY: Helper.convertToJsonArray(confintResultLowerBound)
        }
    except Exception as exception:
        outputJson[Constants.OUTPUT_EXCEPTION_KEY] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: Constants.OUTPUT_EXCEPTION_TITLE_VALUE,
            Constants.OUTPUT_ELEMENT_RESULT_KEY: str(exception)
        }
        return False

    return True

def archTest(timeSeries, inputJson, outputJson):
    try:
        args = Helper.buildArguments(inputJson, ["nlags", "ddof"])
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
        outputJson[Constants.OUTPUT_EXCEPTION_KEY] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: Constants.OUTPUT_EXCEPTION_TITLE_VALUE,
            Constants.OUTPUT_ELEMENT_RESULT_KEY: str(exception)
        }
        return False

    return True

def ljungBoxTest(timeSeries, inputJson, outputJson):
    try:
        args = Helper.buildArguments(inputJson, ["period", "lags", "auto_lag", "model_df"])
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
        outputJson[Constants.OUTPUT_EXCEPTION_KEY] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: Constants.OUTPUT_EXCEPTION_TITLE_VALUE,
            Constants.OUTPUT_ELEMENT_RESULT_KEY: str(exception)
        }
        return False

    return True