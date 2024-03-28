import json

import pandas as pd
from featureVector import featureVector
from FS import forcastability_score_cosine_with_rep as fscr
from prophet import Prophet
from sklearn.metrics import mean_absolute_percentage_error as mape
import time


def hasAnomoly(y, yUpper, yLower):
    if y < yLower or y > yUpper:  # out of the confidence interval
        return "yes"
    return "no"


def anomolyDetector(df, oos=120, fh=1, frequency="D",params=None):
    # df - dataframe, window_size - size of the window, threshold - threshold value, oos - out of sample data, fh - forecast horizon
    #prophet compatibility
    df.columns = ["ds", "y"]
    df["ds"] = pd.to_datetime(df["ds"])
    df["ds"] = df["ds"].dt.strftime("%Y-%m-%d")

    with open("/home/codit/PycharmProjects/DataGenie-Hackathon/threshold.json") as f:
        data = json.load(f)
    threshold = float(data["threshold"])

    dfForFv = df.copy()
    fv = list(featureVector(dfForFv).values())
    fs = fscr(fv)

    oos = max(
        oos, int(len(df) * 0.9)
    )  # making sure that the initial batch size is atmost 10%

    dates = df["ds"].to_list()[-oos:]
    test = df["y"].to_list()[-oos:]
    yhat = []
    yLower = []
    yUpper = []
    timePerFit = []
    if fs > threshold:
        count = 0
        for i in range(-oos, 0, fh):
            start = time.time()
            model = Prophet(**params)
            model.fit(df[:i])
            # assuming that the window size mentioned is for fh since window size is incremental in expanding window
            if i+fh<=0:
                future = model.make_future_dataframe(periods=fh, freq=frequency)
                forecast = model.predict(future)
                yhat.extend(forecast["yhat"].tail(fh).to_list())
                yLower.extend(forecast["yhat_lower"].tail(fh).to_list())
                yUpper.extend(forecast["yhat_upper"].tail(fh).to_list())
            else:
                fh=-i
                future = model.make_future_dataframe(periods=fh, freq=frequency)
                forecast = model.predict(future)
                yhat.extend(forecast["yhat"].tail(fh).to_list())
                yLower.extend(forecast["yhat_lower"].tail(fh).to_list())
                yUpper.extend(forecast["yhat_upper"].tail(fh).to_list())
            count += 1
            end = time.time()
            timePerFit.append(end - start)
        response = {}
        results = []
        for i in range(len(test)):
            result = {
                "timestamp": dates[i],
                "point_value": test[i],
                "predicted": yhat[i],
                "is_anomaly": hasAnomoly(test[i], yUpper[i], yLower[i]),
            }
            results.append(result)
        response["forecastability_score"] = fs
        response["number_of_batch_fits"] = count
        response["mape"] = mape(test, yhat)
        response["avg_time_per_fit_in_seconds"] = sum(timePerFit) / len(timePerFit)
        response["results"] = results
        return response
    else:
        return {
            "forecastability_score": fs,
            "anomaly_detection_done": "No"
        }
"""
f=open("Electric_Production_output.json","w+")
output=anomolyDetector(pd.read_csv("/home/codit/PycharmProjects/DataGenie-Hackathon/App/Electric_Production.csv"), threshold=5,fh=4 , frequency="MS")
json.dump(output,f)

f=open("monthly_csv_output.json","w+")
output=anomolyDetector(pd.read_csv("/home/codit/PycharmProjects/DataGenie-Hackathon/App/monthly_csv.csv"), threshold=5,fh=4 , frequency="MS")
json.dump(output,f)
"""