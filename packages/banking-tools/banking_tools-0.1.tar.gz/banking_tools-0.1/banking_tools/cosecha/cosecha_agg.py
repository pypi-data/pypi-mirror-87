import warnings

warnings.filterwarnings('always')
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np
import gc


def cosecha_agg_func(var_list, aggfunc=""):
    global score
    if aggfunc == 'var':
        score = np.var(var_list, ddof=1)
    elif aggfunc == 'min':
        score = np.min(var_list)
    elif aggfunc == 'max':
        score = np.max(var_list)
    elif aggfunc == 'mean':
        score = np.mean(var_list)
    elif aggfunc == 'median':
        score = np.median(var_list)
    elif aggfunc == 'list':
        score = np.array(var_list)
    elif aggfunc == 'sum':
        score = np.sum(var_list)
    elif aggfunc == 'std':
        score = np.std(var_list)
    elif aggfunc == 'count_nonzero':
        score = np.count_nonzero(var_list)
    return score


def iterations_agg_funcs(df, agg_func, lag, prefix_col, var_list):
    agg_col_name = f"{agg_func.upper()}_{lag}_MONTH_{prefix_col.upper()}"

    if agg_func == "list":
        df[agg_col_name] = df[var_list].apply(
            lambda x: cosecha_agg_func(var_list=x, aggfunc="list"), axis=1)
    if agg_func == "min":
        df[agg_col_name] = df[var_list].apply(
            lambda x: cosecha_agg_func(var_list=x, aggfunc="min"), axis=1)
    if agg_func == "max":
        df[agg_col_name] = df[var_list].apply(
            lambda x: cosecha_agg_func(var_list=x, aggfunc="max"), axis=1)
    if agg_func == "sum":
        df[agg_col_name] = df[var_list].apply(
            lambda x: cosecha_agg_func(var_list=x, aggfunc="sum"), axis=1)
    if agg_func == "var":
        df[agg_col_name] = df[var_list].apply(
            lambda x: cosecha_agg_func(var_list=x, aggfunc="var"), axis=1)
    if agg_func == "mean":
        df[agg_col_name] = df[var_list].apply(
            lambda x: cosecha_agg_func(var_list=x, aggfunc="mean"), axis=1)
    if agg_func == "std":
        df[agg_col_name] = df[var_list].apply(
            lambda x: cosecha_agg_func(var_list=x, aggfunc="std"), axis=1)
    if agg_func == "count_nonzero":
        df[agg_col_name] = df[var_list].apply(
            lambda x: cosecha_agg_func(var_list=x, aggfunc="count_nonzero"), axis=1)
    return df, agg_col_name


def agg_cosecha(df,
                df_index=[],
                df_hue="",
                df_values="",
                month_cosechas=[],
                prefix_col="",
                lags=[],
                agg_funcs=[],
                windows=0):

    """
    :param df: DataFrame
    :param df_index: Array -> ["one", "two"]
    :param df_hue: String -> "three"
    :param df_hue: String -> "PERIODO"
    :param month_cosechas: Array -> ["201903", "20192", etc..]
    :param prefix_col: String -> "prefix column"
    :param lags: Array -> [2,3]
    :param agg_funcs: ["min", "max", etc...]
    :param windows: Array -> [0]
    :return:
    """
    global df4
    df = pd.pivot_table(data=df,
                        index=df_index,
                        columns=df_hue,
                        values=df_values,
                        aggfunc=[np.sum],
                        fill_value=0)
    df.columns = [f'COSECHA_{str(j).upper()}' for i, j in df.columns]
    df = df.reset_index()

    for index_cosecha, month_cosecha in enumerate(month_cosechas):
        print(" |---------------|")
        print(f" |COSECHA TARGET: {month_cosecha}|")
        key_columns = list(sorted([col for col in df.columns if not str(col).startswith("COSECHA")]))
        list_period = list(sorted([col for col in df.columns if str(col).startswith("COSECHA")]))

        if len(lags) == 1 and int(lags[0]) == 0:
            lags = [(len(list_period))]
        elif len(lags) == 0:
            lags = [(len(list_period))]

        df2 = df.copy()
        col_list_lag = list()
        for lag in lags:
            col = list(sorted([col for col in df2.columns
                               if str(col).startswith("COSECHA") and int(str(col).split("_")[1]) <= int(month_cosecha)],
                              reverse=True))

            new_lag = lag + windows
            var_list = col[int(windows):int(new_lag)]
            print(f" |{lag}_LAG: {var_list}")
            print(" |---------------|")

            col_list = list()
            for agg_func in agg_funcs:
                df2, agg_col_name = iterations_agg_funcs(df2, agg_func, lag, prefix_col, var_list)
                col_list.append(agg_col_name)
                col_list_lag.append(agg_col_name)

        df3 = df2[key_columns + col_list_lag]
        df3["PERIODO"] = int(month_cosecha)

        if index_cosecha == 0:
            df4 = df3.copy()
        else:
            df4 = pd.concat([df3, df4], ignore_index=True)

    del df, df2, df3
    gc.collect()
    return df4
