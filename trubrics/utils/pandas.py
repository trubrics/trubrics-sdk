def get_features(df, target):
    return [col for col in df.columns if col != target]
