from pydantic import BaseModel
from datetime import datetime
from typing import List
import pandas as pd


class TimeSeriesRow(BaseModel):
    point_timestamp: str
    point_value: float


class TimeSeries(BaseModel):

    Data: List[TimeSeriesRow]

    def to_dataframe(self):
        return pd.DataFrame(
            [
                {"point_timestamp": row.point_timestamp, "point_value": row.point_value}
                for row in self.Data
            ]
        )


class Request(BaseModel):
    Date_from: str
    Data_to: str
    Frequency: str
