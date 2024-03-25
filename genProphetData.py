import numpy as np
import pandas as pd
from prophet import Prophet
from datetime import datetime, timedelta
from dataPreProcessing import convertToJson

date_from = datetime(2020, 1, 1)
n = 5000  # number of time series to generate
rows = 500  # number of samples per time series


def genProphetData(seed):
    np.random.seed(seed)
    dateRange = [date_from + timedelta(days=i) for i in range(0, rows)]
    newData = np.random.randn(rows)  # random data

    df = pd.DataFrame({"ds": dateRange, "y": newData})  # prophet compatible dataframe

    model = Prophet()
    model.fit(df)

    future = model.make_future_dataframe(periods=rows)
    forecast = model.predict(future)
    syntheticDataGen = forecast["yhat"][-rows:].values

    return dateRange, syntheticDataGen


for i in range(n):
    dateRange, syntheticData = genProphetData(i) # get similar data whenever run
    dateRange = [date.strftime("%Y-%m-%d") for date in dateRange]
    df = pd.DataFrame({"point_timestamp": dateRange, "point_value": syntheticData})
    json = convertToJson(df)
    with open(f"Prophet Data/sample_{i}.json", "w") as f:
        f.write(json)
