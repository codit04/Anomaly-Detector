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
    fv = featureVector(data.Data)
    return fv


@app.post("/forecastabilityScore")
async def forecastability_score(data: TimeSeries):
    fs = forcastability_score_cosine_with_rep(data.Data)
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
    with open("/home/codit/PycharmProjects/DataGenie-Hackathon/threshold.json") as f:
        data = json.load(f)
    thrsh = float(data["threshold"])
    output = anomolyDetector(
        df, threshold=thrsh, fh=fh, frequency=frequency, oos=oos
    )
    return output


