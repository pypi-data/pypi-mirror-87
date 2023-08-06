# pylint: disable = import-outside-toplevel
from databricksbundle.detector import isDatabricks

def createDisplay():
    if isDatabricks():
        import IPython  # pylint: disable = import-error
        return IPython.get_ipython().user_ns['display']

    import importlib.util
    from pyspark.sql.dataframe import DataFrame

    spec = importlib.util.find_spec('pandas')
    if spec is None:
        raise Exception('Run "poetry install -E local-spark-dev" to add support for local display() function')

    import pandas as pd  # pylint: disable = import-error

    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)

    def displayLocal(df: DataFrame):
        print(df.limit(100).toPandas())

    return displayLocal

display = createDisplay()
