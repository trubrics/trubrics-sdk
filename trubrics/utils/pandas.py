import pandas as pd


def schema_is_equal(df1: pd.DataFrame, df2: pd.DataFrame) -> bool:
    return df1.dtypes.equals(df2.dtypes)
