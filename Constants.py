import os

DEBUG_FILE_NAME = "debug.json"
DEBUG = False


PYTHON_BASE_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

BACKEND_BASE_DIRECTORY_PATH = "java_backend"

DATASET_TIME_SERIES_PATH = "storage\\dataset"
DATASET_INPUT_PATH = "storage\\python\\input"
DATASET_OUTPUT_PATH = "storage\\python\\output"

DATE_COLUMN_NAME = "date"
DATA_COLUMN_NAME = "data"
DATE_TIME_FORMAT = "%Y/%m/%d-%H"

RANDOM_STRING_LENGTH = 36


ACTION_DICKEY_FULLER_TEST = "dicker_fuller_test"
ACTION_KPSS_TEST = "kpss_test"
ACTION_SEASONAL_DECOMPOSE = "seasonal_decompose"
ACTION_PERIODOGRAM = "periodogram"
ACTION_CORRELOGRAM_ACF = "correlogram_acf"
ACTION_CORRELOGRAM_PACF = "correlogram_pacf"
ACTION_ARCH_TEST = "arch_test"
ACTION_LJUNG_BOX_TEST = "ljung_box_test"

ACTION_DIFFERENCE = "difference"
ACTION_LOGARITHM = "logarithm"
ACTION_NORMALIZATION = "normalization"
ACTION_STANDARDIZATION = "standardization"

ACTION_ARIMA = "arima"
ACTION_HOLT_WINTER = "holt_winter"


INPUT_FILE_NAME_KEY = "file_name"
INPUT_P_VALUE_KEY = "p_value"
INPUT_ACTION_KEY = "action"


OUTPUT_ELEMENT_TITLE_KEY = "title"
OUTPUT_ELEMENT_RESULT_KEY = "result"


OUTPUT_SUCCESS_KEY = "success"

OUT_EXCEPTION_KEY = "exception"
OUT_EXCEPTION_TITLE_VALUE = "vzniknutá chyba"


PYTHON_FREQUENCY_TYPE_KEY = "python_frequency"
FREQUENCY_TYPE_KEY = "frequency"
FORECAST_COUNT_KEY = "forecast_count"


OUTPUT_TRANSFORMED_FILE_NAME_KEY = "transformed_file_name"
OUTPUT_TRANSFORMED_FILE_NAME_TITLE_VALUE = "transformovaný súbor"

OUTPUT_START_DATE_TIME_KEY = "start_date_time"
OUTPUT_START_DATE_TIME_TITLE_VALUE = "začiatočný dátum"


OUTPUT_P_VALUE_KEY = "result_p_value"
OUTPUT_P_VALUE_TITLE_VALUE = "výsledná p-hodnota"

OUTPUT_USED_P_VALUE_KEY = "used_p_value"
OUTPUT_USED_P_VALUE_TITLE_VALUE = "zvolená hladina významnosti"

OUTPUT_EVALUATION_KEY = "evaluation"
OUTPUT_EVALUATION_TITLE_VALUE = "vyhodnotenie"

OUTPUT_TEST_STATISTIC_KEY = "test_statistics"
OUTPUT_TEST_STATISTIC_TITLE_VALUE = "vypočítaná testovacia štatistika"

OUTPUT_NULL_HYPOTHESIS_KEY = "null_hypothesis"
OUTPUT_NULL_HYPOTHESIS_TITLE_VALUE = "nulová hypotéza"

OUTPUT_ALTERNATIVE_HYPOTHESIS_KEY = "alternative_hypothesis"
OUTPUT_ALTERNATIVE_HYPOTHESIS_TITLE_VALUE = "alternatívna hypotéza"

OUTPUT_CONFIDENCE_INTERVAL_UPPER_BOUND_KEY = "confidence_interval_upper_bound"
OUTPUT_CONFIDENCE_INTERVAL_LOWER_BOUND_KEY = "confidence_interval_lower_bound"


OUTPUT_SUMMARY_KEY = "summary"

OUTPUT_TRAIN_KEY = "train"
OUTPUT_TEST_KEY = "test"
OUTPUT_FORECAST_KEY = "forecast"

MODEL_DATE_KEY = "date"
MODEL_REAL_KEY = "real"
MODEL_FITTED_KEY = "fitted"
MODEL_RESIDUALS_KEY = "residuals"
