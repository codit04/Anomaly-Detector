from pydantic import BaseModel
from datetime import datetime
from typing import List
import pandas as pd


class TimeSeriesRow(BaseModel):
    ds : str
    y : float


class TimeSeries(BaseModel):

    Data: List[TimeSeriesRow]

    def to_dataframe(self):
        return pd.DataFrame(
            [
                {"ds": row.ds, "y": row.y}
                for row in self.Data
            ]
        )

