#!/usr/bin/env python3
"""
    Python porting of Impulse MACD [LazyBear]
    https://www.tradingview.com/script/qt6xLfLi-Impulse-MACD-LazyBear/
    Developed by @edyatl <edyatl@yandex.ru> March 2023
    https://github.com/edyatl

"""
# Standard imports
import pandas as pd
import numpy as np
import talib as tl
import os
from os import environ as env
from dotenv import load_dotenv
from binance import Client

# Load API keys from env
project_dotenv = os.path.join(os.path.abspath(""), ".env")
if os.path.exists(project_dotenv):
    load_dotenv(project_dotenv)

api_key, api_secret = env.get("ENV_API_KEY"), env.get("ENV_SECRET_KEY")

# Make API Client instance
client = Client(api_key, api_secret)

short_col_names = [
    "open_time",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "close_time",
    "qav",
    "num_trades",
    "taker_base_vol",
    "taker_quote_vol",
    "ignore",
]

# Load Dataset
# Get last 500 records of ATOMUSDT 15m Timeframe
klines = client.get_klines(symbol="ATOMUSDT", interval=Client.KLINE_INTERVAL_15MINUTE)
data = pd.DataFrame(klines, columns=short_col_names)

# Convert Open and Close time fields to DateTime
data["open_time"] = pd.to_datetime(data["open_time"], unit="ms")
data["close_time"] = pd.to_datetime(data["close_time"], unit="ms")

#--------------------------INPUTS--------------------------------
lengthMA: int = 34
lengthSignal: int = 9

#--------------------------FUNCIONS------------------------------
def calc_smma(src: np.ndarray, length: int) -> np.ndarray:
    """
    Calculate Smoothed Moving Average (SMMA) for a given numpy array `src` with a specified `length`.

    :param src: A numpy ndarray of shape (n,) containing the input values of float64 dtype.
    :param length: An integer representing the length of the SMMA window.
    :return: A numpy ndarray of the same shape as `src` containing the SMMA values.
    """
    smma = np.full_like(src, fill_value=np.nan)
    sma = tl.SMA(src, length)

    for i in range(1, len(src)):
        smma[i] = (
            sma[i]
            if np.isnan(smma[i - 1])
            else (smma[i - 1] * (length - 1) + src[i]) / length
        )

    return smma

def calc_zlema(src: np.ndarray, length: int) -> np.ndarray:
    """
    Calculates the zero-lag exponential moving average (ZLEMA) of the given price series.

    :param src: The input price series of float64 dtype to calculate the ZLEMA for.
    :param length: int The number of bars to use for the calculation of the ZLEMA.
    :return: A numpy ndarray of ZLEMA values for the input price series.
    """
    ema1 = tl.EMA(src, length)
    ema2 = tl.EMA(ema1, length)
    d = ema1 - ema2
    return ema1 + d


def main():
    src = (
        data["high"].to_numpy(dtype=np.double)
        + data["low"].to_numpy(dtype=np.double)
        + data["close"].to_numpy(dtype=np.double)
    ) / 3
    hi = calc_smma(data["high"].to_numpy(dtype=np.double), lengthMA)
    lo = calc_smma(data["low"].to_numpy(dtype=np.double), lengthMA)
    mi = calc_zlema(src, lengthMA)

    md = np.full_like(mi, fill_value=np.nan)

    conditions = [mi > hi, mi < lo]
    choices = [mi - hi, mi - lo]

    md = np.select(conditions, choices, default=0)

    sb = tl.SMA(md, lengthSignal)
    sh = md - sb

    res = pd.DataFrame(
        {
            "open_time": data["open_time"],
            "ImpulseMACD": md,
            "ImpulseHisto": sh,
            "ImpulseMACDCDSignal": sb,
        }
    )
    res.to_csv('impulse_macd-ATOMUSDT-15m.csv', index = None, header=True)


if __name__ == "__main__":
    main()
