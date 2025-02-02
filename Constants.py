import os

DEBUG_FILE_NAME = "debug.json"


PYTHON_BASE_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

BACKEND_BASE_DIRECTORY_PATH = "backend"

DATASET_TIME_SERIES_PATH = "storage\\dataset"
DATASET_INPUT_PATH = "storage\\python\\input"
DATASET_OUTPUT_PATH = "storage\\python\\output"

DATE_COLUMN_NAME = "date"
DATA_COLUMN_NAME = "data"
DATE_TIME_FORMAT = "%Y/%m/%d-%H"


ACTION_DICKEY_FULLER_TEST = "dicker_fuller_test"
ACTION_KPSS_TEST = "kpss_test"


INPUT_FILE_NAME_KEY = "file_name"
INPUT_P_VALUE_KEY = "p_value"
INPUT_ACTION_KEY = "action"


OUT_EXCEPTION_KEY = "exception"
OUT_EXCEPTION_TITLE_VALUE = "vzniknutá chyba"

OUTPUT_SUCCESS_KEY = "success"
OUTPUT_P_VALUE_KEY = "result_p_value"
OUTPUT_P_VALUE_TITLE_VALUE = "výsledná p-hodnota"

OUTPUT_USED_P_VALUE_KEY = "used_p_value"
OUTPUT_USED_P_VALUE_TITLE_VALUE = "zvolená hladina významnosti"

OUTPUT_EVALUATION_KEY = "evaluation"
OUTPUT_EVALUATION_TITLE_VALUE = "vyhodnotenie"

OUTPUT_TEST_STATISTIC_KEY = "test_statistics"
OUTPUT_TEST_STATISTIC_TITLE_VALUE = "testovacia štatistika"

OUTPUT_NULL_HYPOTHESIS_KEY = "null_hypothesis"
OUTPUT_NULL_HYPOTHESIS_TITLE_VALUE = "nulová hypotéza"

OUTPUT_ALTERNATIVE_HYPOTHESIS_KEY = "alternative_hypothesis"
OUTPUT_ALTERNATIVE_HYPOTHESIS_TITLE_VALUE = "alternatívna hypotéza"


OUTPUT_ELEMENT_TITLE_KEY = "title"
OUTPUT_ELEMENT_RESULT_KEY = "result"
