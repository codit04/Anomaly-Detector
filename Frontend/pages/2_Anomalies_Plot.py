import streamlit as st
import plotly.io as pio
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests

pio.templates.default = "plotly"

st.set_page_config(page_title="Anomalies Plot ", page_icon="📊", layout="wide")


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


def plot_anomalies(json):
    if len(json) > 2:
        forecastability_score = json["forecastability_score"]
        number_of_batch_fits = json["number_of_batch_fits"]
        mape = json["mape"]
        avg_time_per_fit_in_seconds = json["avg_time_per_fit_in_seconds"]
        results = json["results"]
        anomalies = 0
        dates = []
        test = []
        predicted = []
        is_anomaly = []
        for result in results:
            dates.append(result["timestamp"])
            test.append(result["point_value"])
            predicted.append(result["predicted"])
            is_anomaly.append(result["is_anomaly"])
            if result["is_anomaly"]=="yes":
                anomalies += 1
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.02)
        fig.add_trace(
            go.Scatter(x=dates, y=test, mode="markers+lines", name="Actual"),
            row=1,
            col=1,
        )
        fig.add_trace(
            go.Scatter(x=dates, y=predicted, mode="markers+lines", name="Predicted"),
            row=1,
            col=1,
        )
        fig.add_trace(
            go.Scatter(
                x=dates,
                y=[predicted[i] if is_anomaly[i] == "yes" else None for i in range(len(test))],
                mode="markers",
                name="Anomalies",
            ),
            row=1,
            col=1,
        )

        fig.update_layout(
            title="Anomalies Plot",
            xaxis_title="Date",
            yaxis_title="Value",
            showlegend=True,
        )
        st.plotly_chart(fig)
        st.write("Forecastability Score: ", forecastability_score)
        st.write("Number of batch fits: ", number_of_batch_fits)
        st.write("Mean Absolute Percentage Error: ", mape)
        st.write("Average time per fit in seconds: ", avg_time_per_fit_in_seconds)
        st.write("Number of anomalies: ", anomalies)
    else:
        st.write("Forecastability score is below threshold, no anomalies detected")
        st.write("Forecastability Score: ", json["forecastability_score"])


def main():
    st.title("Anomalies Plot")
    st.write("This page plots the anomalies in the time series data")
    file = fileUploader()
    if file is not None:
        st.write("Preview")
        st.write(file.head())
        Data = file.to_dict(orient="records")
        data = {"Data": Data}

        with st.form(key="anomalies_form"):
            fh = st.selectbox("Window size ", [1, 2, 3, 4, 5, 6, 7])
            frequency = st.selectbox(
                "Frequency",
                [
                    "D",
                    "B",
                    "H",
                    "T",
                    "S",
                    "L",
                    "U",
                    "N",
                    "W",
                    "M",
                    "SM",
                    "BM",
                    "CBM",
                    "MS",
                    "SMS",
                    "BMS",
                    "CBMS",
                    "Q",
                    "BQ",
                    "QS",
                    "BQS",
                    "A",
                    "BA",
                    "AS",
                    "BAS",
                ],
            )
            oos = st.number_input(
                "Initial batch size ", min_value=1, value=120, max_value=len(Data)
            )
            oos = len(Data) - oos
            submit_button = st.form_submit_button(label="Check for Anomalies")

            if submit_button:
                params = {"fh": fh, "frequency": frequency, "oos": oos}

                with st.spinner(text="Detecting anomalies..."):
                    response = requests.post(
                        url="http://127.0.0.1:8000/anomalies", json=data, params=params
                    )
                output = response.json()
                plot_anomalies(output)


if __name__ == "__main__":
    main()
