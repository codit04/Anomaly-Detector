import streamlit as st
import plotly.io as pio
from statsmodels.tsa.seasonal import seasonal_decompose
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

pio.templates.default = "plotly"

st.set_page_config(page_title="Components Plot ", page_icon="📈",layout="wide")

def validFormat(dataframe):
    if len(dataframe.columns) != 2:
        return False
    return True

def fileUploader():
    uploaded_file = st.file_uploader("Upload your time series file", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        if validFormat(df):
            df.columns = ["ds", "y"]
            return df
        else:
            st.write("Invalid time series format")

    return None


def plot_df(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.ds, y=df.y, mode="lines", name="y"))
    fig.update_layout(title="Time Series Data", xaxis_title="Date", yaxis_title="Value")
    st.plotly_chart(fig)

def plot_components(df):
    result = seasonal_decompose(df.set_index("ds").y, model="additive")
    fig = make_subplots(rows=4, cols=1, shared_xaxes=True, subplot_titles=("Trend", "Seasonal", "Residual", "Observed"))
    fig.add_trace(go.Scatter(x=df.ds, y=result.trend, mode="lines", name="Trend"), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.ds, y=result.seasonal, mode="lines", name="Seasonal"), row=2, col=1)
    fig.add_trace(go.Scatter(x=df.ds, y=result.resid, mode="lines", name="Residual"), row=3, col=1)
    fig.add_trace(go.Scatter(x=df.ds, y=result.observed, mode="lines", name="Observed"), row=4, col=1)
    fig.update_layout(height=800, showlegend=False)
    st.plotly_chart(fig)

def main():
    st.title("Time Series Components")
    st.write("This page plots the components of the time series data")
    file = fileUploader()
    if file is not None:
        st.write("Preview")
        st.write(file.head())
        file.columns = ["ds", "y"]
        file["ds"] = pd.to_datetime(file["ds"])
        plot_df(file)
        plot_components(file)

if __name__ == "__main__":
    main()