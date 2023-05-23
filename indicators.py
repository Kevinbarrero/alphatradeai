import numpy as np


def calcSma(data, smaPeriod):
    j = next(i for i, x in enumerate(data) if x is not None)
    our_range = range(len(data))[j + smaPeriod - 1 :]
    empty_list = [None] * (j + smaPeriod - 1)
    sub_result = [np.mean(data[i - smaPeriod + 1 : i + 1]) for i in our_range]

    return np.array(empty_list + sub_result)


def calculate_ema(prices, fixed, period, smoothing=2):
    ema = [sum(prices[:period]) / period]
    for price in prices[period:]:
        ema.append(
            (price * (smoothing / (1 + period)))
            + ema[-1] * (1 - (smoothing / (1 + period)))
        )
    return fix_ema(ema, fixed)


def fix_ema(data, fixed):
    while len(data) != len(fixed):
        data.insert(0, sum(data) / len(data))
    return data


def heikin_ashi(df):
    df_ha = df.copy()
    for i, row in df_ha.iterrows():
        if i > 0:
            opn = df["open"][i - 1]
            close = df["close"][i - 1]
            df_ha.loc[df_ha.index[i], "open"] = (opn + close) / 2
            opn = df["open"][i]
            close = df["close"][i]
            low = df["low"][i]
            high = df["high"][i]
            df_ha.loc[df_ha.index[i], "close"] = (opn + close + low + high) / 4
    # df_ha = df_ha.iloc[1:, :]
    return df_ha


def percent_classifier(df, window):
    df[f"window_percent{window}"] = None
    for i, row in df.iterrows():
        if i > len(df) - window - 1:
            continue
        else:
            if df["close"][i] < df["close"][i + window]:
                df[f"window_percent{window}"][i] = 1
            if df["close"][i] > df["close"][i + window]:
                df[f"window_percent{window}"][i] = 0
    return df


def percent_classifier_v2(df, percent_target, analisys_window):
    df["window_percent"] = None

    for j, row in df.iterrows():
        if row["Ema20"] > row["Ema70"]:

            for i in range(j, len(df) - 1):
                # Nothing label
                if i > j + analisys_window:
                    df["window_percent"][j] = 2
                    break

                # Long label
                if df["close"][j] < df["close"][i]:
                    percent_cal = (df["close"][i] - df["close"][j]) / df["close"][j]
                    percent = percent_cal * 100
                    if percent > percent_target:
                        df["window_percent"][j] = 1
                        break

        if row["Ema20"] < row["Ema70"]:
            for i in range(j, len(df) - 1):
                # Nothing label
                if i > j + analisys_window:
                    df["window_percent"][j] = 2
                    break

                # Short label
                if df["close"][j] > df["close"][i]:
                    percent_cal = (df["close"][j] - df["close"][i]) / df["close"][i]
                    percent = percent_cal * 100
                    if percent > percent_target:
                        df["window_percent"][j] = 0
                        break

    return df



def price_transformer(df, predict_window):
    df['f_price'] = df['close'].shift(-predict_window)
    return df

