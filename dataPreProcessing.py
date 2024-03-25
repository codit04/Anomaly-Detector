import pandas as pd
import os

hourly = os.listdir("/home/codit/Documents/Sample Time Series/hourly")
daily = os.listdir("/home/codit/Documents/Sample Time Series/daily")
weekly = os.listdir("/home/codit/Documents/Sample Time Series/weekly")
monthly = os.listdir("/home/codit/Documents/Sample Time Series/monthly")


def convertToJson(data):
    if data.columns[0] == "Unnamed: 0":
        data = data.drop(data.columns[0], axis=1)
    mean = data["point_value"].mean()
    data["point_value"] = data["point_value"].fillna(mean)
    json = data.to_json(orient="records")
    return json


for i in hourly:
    data = pd.read_csv("/home/codit/Documents/Sample Time Series/hourly/" + i)
    json = convertToJson(data)
    with open(
        "/home/codit/Documents/Time Series JSON/hourly/" + i.split(".")[0] + ".json",
        "w",
    ) as f:
        f.write(json)

for i in daily:
    data = pd.read_csv("/home/codit/Documents/Sample Time Series/daily/" + i)
    json = convertToJson(data)
    with open(
        "/home/codit/Documents/Time Series JSON/daily/" + i.split(".")[0] + ".json", "w"
    ) as f:
        f.write(json)

for i in weekly:
    data = pd.read_csv("/home/codit/Documents/Sample Time Series/weekly/" + i)
    json = convertToJson(data)
    with open(
        "/home/codit/Documents/Time Series JSON/weekly/" + i.split(".")[0] + ".json",
        "w",
    ) as f:
        f.write(json)

for i in monthly:
    data = pd.read_csv("/home/codit/Documents/Sample Time Series/monthly/" + i)
    json = convertToJson(data)
    with open(
        "/home/codit/Documents/Time Series JSON/monthly/" + i.split(".")[0] + ".json",
        "w",
    ) as f:
        f.write(json)
