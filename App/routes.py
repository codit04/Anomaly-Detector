
# add routes
import os
import pandas as pd
import json
from __init__ import app
from schema import TimeSeries,TimeSeriesRow
from FS import forcastability_score_cosine_with_rep
from featureVector import  featureVector

@app.post('/featureVector')
async def feature_vector(data: TimeSeries):
    fv = featureVector(data.Data)
    return fv

@app.post('/forecastabilityScore')
async def forecastability_score(data: TimeSeries):
    fs = forcastability_score_cosine_with_rep(data.Data)
    return fs

@app.get('/threshold')
def threshold():
    with open('/home/codit/PycharmProjects/DataGenie-Hackathon/threshold.json') as f:
        data = json.load(f)
    return data