
import pandas as pd
def industry_rotation(df):
    if df is None or len(df)==0:return pd.DataFrame()
    return df.groupby("主流族群")["AI冠軍分數"].mean().sort_values(ascending=False).reset_index()
