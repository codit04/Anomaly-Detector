from hyperopt import tpe, hp, fmin, STATUS_OK, Trials
from prophet import Prophet
from prophet.diagnostics import cross_validation, performance_metrics
import pandas as pd
from anomolyDetection import anomolyDetector

def hyperparameter_tuning(params, df):
    model = Prophet(**params).fit(df)
    cv = cross_validation(
        model, initial="100 days", period="10 days", horizon="10 days"
    )
    df_p = performance_metrics(cv, rolling_window=1)
    return {"loss": -df_p["mape"].values[0], "status": STATUS_OK}


def findBestParams(df):
    space = {
        "changepoint_prior_scale": hp.uniform("changepoint_prior_scale", 0.001, 0.5),
        "seasonality_prior_scale": hp.uniform("seasonality_prior_scale", 0.01, 10),
        "seasonality_mode": hp.choice(
            "seasonality_mode", ["additive", "multiplicative"]
        ),
    }
    trials = Trials()

    best = fmin(
        fn=lambda params: hyperparameter_tuning(params, df), # could use logging method to improve mape
        space=space,
        algo=tpe.suggest,  # Tree of Parzen Estimator
        max_evals=3,   # number of evals increases quality of the hyper parameters
        trials=trials,
    )

    return best


def hyperOptAnomolyDetector(df, oos=120, fh=1, frequency="D"):
    df.columns = ["ds", "y"]
    params=findBestParams(df)
    if params["seasonality_mode"]==0:
        params["seasonality_mode"]="additive"
    else:
        params["seasonality_mode"]="multiplicative"
    result=anomolyDetector(df,oos=oos,fh=fh,frequency=frequency,params=params)
    return result

if __name__ == "__main__":
    df = pd.read_csv(
        "/home/codit/PycharmProjects/DataGenie-Hackathon/App/Electric_Production.csv"
    )
    print(hyperOptAnomolyDetector(df,120,7,'MS'))