def age_young(df):
    return df.loc[df["Age"] < 13, :]


def sex_female(df):
    return df.loc[df["Sex"] == "female", :]


def sex_male(df):
    return df.loc[df["Sex"] == "male", :]


slicing_functions = {"children": age_young, "female": sex_female, "male": sex_male}
