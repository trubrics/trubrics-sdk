import pandas as pd


def age_young(df: pd.DataFrame) -> pd.DataFrame:
    return df.loc[df["Age"] < 4, :]


def sex_female(df: pd.DataFrame) -> pd.DataFrame:
    return df.loc[df["Sex"] == "female", :]


def sex_male(df: pd.DataFrame) -> pd.DataFrame:
    return df.loc[df["Sex"] == "male", :]


slicing_functions = {"children": age_young, "female": sex_female, "male": sex_male}
