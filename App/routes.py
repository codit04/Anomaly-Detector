# add routes
import os
import pandas as pd
import json
from __init__ import app
from typing import Optional
from schema import TimeSeries, TimeSeriesRow
from FS import forcastability_score_cosine_with_rep
from featureVector import featureVector
from anomolyDetection import anomolyDetector


@app.post("/featureVector")
async def feature_vector(data: TimeSeries):
    df = data.to_dataframe()
    fv = featureVector(df)
    return fv


@app.post("/forecastabilityScore")
async def forecastability_score(data: TimeSeries):
    df=data.to_dataframe()
    fv=list(featureVector(df).values())
    fs = forcastability_score_cosine_with_rep(fv)
    return fs


@app.get("/threshold")
async def threshold():
    with open("/home/codit/PycharmProjects/DataGenie-Hackathon/threshold.json") as f:
        data = json.load(f)
    return data


@app.post("/anomalies")
async def anomalies(
        data: TimeSeries,
        fh: Optional[int] = 4,
        frequency: Optional[str] = "D",
        oos: Optional[int] = 120,
):
    df = data.to_dataframe()
    output = anomolyDetector(
        df, fh=fh, frequency=frequency, oos=oos
    )
    return output
