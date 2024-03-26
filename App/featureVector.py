import pandas as pd
import numpy as np
import nolds
from scipy.stats import skew, kurtosis, entropy, variation
from statsmodels.tsa.stattools import adfuller, acf, pacf, kpss
from arch.unitroot import PhillipsPerron
import statsmodels.api as sm


def featureVector(json):
    df = pd.read_json(json)
    df.columns= ['point_timestamp', 'point_value']
    df['point_timestamp'] = pd.to_datetime(df['point_timestamp'])
    df['point_value'] = pd.to_numeric(df['point_value'])

    # Features
    feature_vector = {}
    feature_vector['SampEn'] = nolds.sampen(df['point_value'])  # Sample Entropy
    feature_vector['Hurst'] = nolds.hurst_rs(df['point_value'])  # Hurst Exponent
    feature_vector['dfa'] = nolds.dfa(df['point_value'])  # Detrended Fluctuation Analysis
    feature_vector['Skew'] = skew(df['point_value'])  # Skewness
    feature_vector['Kurt'] = kurtosis(df['point_value'])  # Kurtosis
    feature_vector['Entropy'] = entropy(df['point_value'])  # Entropy
    time_intervals = df['point_value'].diff().dropna()
    feature_vector['ADI'] = time_intervals.mean()  # Average Demand Interval
    cv = df['point_value'].std() / df['point_value'].mean()
    feature_vector['cv2'] = cv ** 2  # Coefficient of Variation
    feature_vector['ADF'] = adfuller(df['point_value'])[1]  # Augmented Dickey-Fuller Test
    feature_vector['ACF'] = acf(df['point_value'])[1]  # Auto Correlation
    feature_vector['PACF'] = pacf(df['point_value'])[1]  # Partial Auto Correlation
    feature_vector['KPSS'] = kpss(df['point_value'])[1]  # Kwiatkowski-Phillips-Schmidt-Shin Test
    feature_vector['Stationary'] = bool(
        feature_vector['ADF'] <= 0.05 and feature_vector['KPSS'] > 0.05)  # Stationarity Check
    feature_vector['PP'] = PhillipsPerron(df['point_value']).pvalue  # Phillips-Perron Test
    feature_vector['Normality'] = bool(sm.stats.diagnostic.normal_ad(df['point_value'])[1] > 0.05)  # Normality Check
    decompose = sm.tsa.seasonal_decompose(df['point_value'], model='additive',
                                          period=6)  # Seasonal Decomposition -Half yearly since few time series given have less records
    trend = decompose.trend.dropna()
    seasonal = decompose.seasonal.dropna()
    residual = decompose.resid.dropna()
    seasonal = decompose.seasonal.dropna()
    feature_vector['Trend Strenth'] = max(0, variation(residual) / (
                variation(trend) + variation(residual)))  # Trend Strength
    feature_vector['Seasonal Strength'] = max(0, variation(residual) / (
                variation(seasonal) + variation(residual)))  # Seasonal Strength
    rolling_mean = df['point_value'].rolling(window=7).mean()
    rolling_std = df['point_value'].rolling(window=7).std()
    feature_vector['Rolling Mean'] = rolling_mean.mean()  # Rolling Mean
    feature_vector['Rolling Std'] = rolling_std.mean()  # Rolling Standard Deviation
    for key in feature_vector.keys():
        if feature_vector[key] == float('inf') or feature_vector[key] == float('-inf') or feature_vector[key] == float(
                'nan'):
            feature_vector[key] = 0
    return feature_vector
