import Constants

from statsmodels.tsa.stattools import adfuller

def dickeyFullerTest(timeSeries, outputJson):
    try:
        result = adfuller(timeSeries.values)

        outputJson["adf"] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: "testovacia štatistika",
            Constants.OUTPUT_ELEMENT_RESULT_KEY: result[0]
        }
        outputJson[Constants.OUTPUT_P_VALUE_KEY] = {
            Constants.OUTPUT_ELEMENT_TITLE_KEY: "výsledná p-hodnota",
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
    except:
        return False

    return True