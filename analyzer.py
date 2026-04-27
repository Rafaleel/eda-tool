import pandas as pd
import numpy as np

def analyze(df: pd.DataFrame) -> dict:

    overview = {
        "n_rows": df.shape[0],
        "n_cols": df.shape[1],
        "n_duplicates": int(df.duplicated().sum()),
        "memory_usage": f"{df.memory_usage(deep=True).sum() / 1024:.2f} KB",
        "columns": list(df.columns),
    }

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    categorical_cols = df.select_dtypes(include="object").columns.tolist()

    overview["n_numeric"] = len(numeric_cols)
    overview["n_categorical"] = len(categorical_cols)

    nulls = pd.DataFrame({
        "column": df.columns,
        "missing": df.isnull().sum().values,
        "percent": (df.isnull().sum().values / len(df) * 100).round(2)
    })
    nulls = nulls[nulls["missing"] > 0].sort_values("percent", ascending=False)
    nulls_list = nulls.to_dict(orient="records")

    if numeric_cols:
        desc = df[numeric_cols].describe().T.reset_index()
        desc.columns = ["column", "count", "mean", "std", "min", "q25", "median", "q75", "max"]
        desc = desc.round(4)
        desc_list = desc.to_dict(orient="records")
    else:
        desc_list = []

    skew_list = []
    for col in numeric_cols:
        skew_list.append({
            "column": col,
            "skewness": round(df[col].skew(), 4),
            "kurtosis": round(df[col].kurt(), 4),
        })

    cat_list = []
    for col in categorical_cols:
        value_counts = df[col].value_counts().head(10)
        cat_list.append({
            "column": col,
            "n_unique": df[col].nunique(),
            "top_values": value_counts.index.tolist(),
            "top_counts": value_counts.values.tolist(),
        })

    if len(numeric_cols) >= 2:
        corr = df[numeric_cols].corr().round(3)
        corr_columns = corr.columns.tolist()
        corr_values = corr.values.tolist()
    else:
        corr_columns = []
        corr_values = []

    return {
        "overview": overview,
        "numeric_cols": numeric_cols,
        "categorical_cols": categorical_cols,
        "nulls": nulls_list,
        "descriptive": desc_list,
        "skewness": skew_list,
        "categorical": cat_list,
        "corr_columns": corr_columns,
        "corr_values": corr_values,
    }
