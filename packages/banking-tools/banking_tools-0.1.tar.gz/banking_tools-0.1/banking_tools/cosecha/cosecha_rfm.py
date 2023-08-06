import gc
import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings('always')
warnings.filterwarnings('ignore')

gc.enable()


def get_r_score(x, p, d):
    if x <= d[p][0.2]:
        return 5
    elif x <= d[p][0.4]:
        return 4
    elif x <= d[p][0.6]:
        return 3
    elif x <= d[p][0.8]:
        return 2
    else:
        return 1


def get_fm_score(x, p, d):
    if x <= d[p][0.2]:
        return 1
    elif x <= d[p][0.4]:
        return 2
    elif x <= d[p][0.6]:
        return 3
    elif x <= d[p][0.8]:
        return 4
    else:
        return 5


def cosecha_agg_func(var_list, aggfunc=""):
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
    return df, agg_col_name


def agg_cosecha_rfm(df,
                    df_index=[],
                    df_hue="",
                    month_cosechas=[],
                    prefix_col="",
                    lags=[],
                    frequency_col="",
                    monetary_col="",
                    windows=0):
    """
    :param df: DataFrame
    :param df_index: Array -> ["one", "two"]
    :param df_hue: String -> "three"
    :param month_cosechas: Array -> ["201903", "20192", etc..]
    :param prefix_col: String -> "prefix column"
    :param lags: Array -> [2,3]
    :param frequency_col: String -> "Frequency column"
    :param monetary_col: String -> "Monetary column"
    :param windows: Array -> [0]
    :return:
    """
    global df3, df5

    for index_cosecha, month_cosecha in enumerate(month_cosechas):
        print(f" |COSECHA TARGET: {month_cosecha}|")

        df2 = df.copy()
        col_list_lag = list()

        list_period = list(sorted(df[df_hue].unique()))

        if len(lags) == 1 and int(lags[0]) == 0:
            lags = [(len(list_period))]
        elif len(lags) == 0:
            lags = [(len(list_period))]

        for index_lag, lag in enumerate(lags):
            col = list(sorted([col for col in list_period if int(col) <= int(month_cosecha)],
                              reverse=True))
            new_lag = lag + windows
            var_list = col[0:int(new_lag)]
            print(f" |{lag}_LAG: {var_list}")

            df_group = df2[df2[df_hue].isin(var_list)] \
                .groupby(df_index) \
                .agg(
                MAX_PERIOD=(df_hue, np.max),
                MIN_PERIOD=(df_hue, np.min),
                FREQUENCY=(f"{frequency_col.upper()}", np.size),
                MONETARY=(f"{monetary_col.upper()}", np.sum)
            ) \
                .reset_index() \
                .fillna(0)
            df_group["LAST_DAY"] = pd.to_datetime(df_group['MAX_PERIOD'], format="%Y%m") + pd.offsets.MonthEnd(1)
            df_group["RECENCY"] = (pd.to_datetime(df_group["LAST_DAY"]) -
                                   pd.to_datetime(df_group["MIN_PERIOD"], format="%Y%m")) / pd.offsets.Day(1)

            df_group2 = df_group[df_index + ["RECENCY", "FREQUENCY", "MONETARY"]]
            df_rfm = df_group2[["RECENCY", "FREQUENCY", "MONETARY"]]
            quantiles = df_rfm.quantile(q=[0.2, 0.4, 0.6, 0.8])
            quantiles = quantiles.to_dict()

            R = 'R_{0}_MONTH_{1}'.format(str(lag), prefix_col)
            F = 'F_{0}_MONTH_{1}'.format(str(lag), prefix_col)
            M = 'M_{0}_MONTH_{1}'.format(str(lag), prefix_col)
            rfm_score = 'RFMSCORE_{0}_MONTH_{1}'.format(str(lag), prefix_col)
            rfm_seg = 'RFMSEG_{0}_MONTH_{1}'.format(str(lag), prefix_col)

            df_group2[R] = df_group2['RECENCY'].fillna(0).apply(get_r_score, args=('RECENCY', quantiles,))
            df_group2[F] = df_group2['FREQUENCY'].fillna(0).apply(get_fm_score, args=('FREQUENCY', quantiles,))
            df_group2[M] = df_group2['MONETARY'].fillna(0).apply(get_fm_score, args=('MONETARY', quantiles,))
            df_group2[rfm_score] = df_group2[[R, F, M]].sum(axis=1)

            score_labels = ['BRONZE', 'SILVER', 'GOLD']
            score_groups = pd.qcut(df_group2[rfm_score], q=3, labels=score_labels)
            df_group2[rfm_seg] = score_groups.values

            df_group2[R] = df_group2['RECENCY']
            df_group2[F] = df_group2['FREQUENCY']
            df_group2[M] = df_group2['MONETARY']

            col_list_lag.append(rfm_seg)

            del df_group2['RECENCY'], df_group2['FREQUENCY'], df_group2['MONETARY']
            del df_group2[rfm_score]
            del df_group
            gc.collect()

            if index_lag == 0:
                df3 = df_group2.copy()
            else:
                df3 = df_group2.merge(df3, on=df_index, how='left')

        df4 = df3.copy()
        df4[df_hue] = int(month_cosecha)

        if index_cosecha == 0:
            df5 = df4.copy()
        else:
            df5 = pd.concat([df4, df5], ignore_index=True)

        gc.collect()
    return df5
