import streamlit as st
import json
import requests
import pandas as pd

st.set_page_config(page_title="DataGenie Hackathon", layout="wide")


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


def showForecastabilityScore(data):
    response = requests.post("http://127.0.0.1:8000/forecastabilityScore", json=data)
    fs = response.json()
    st.write("Forecastability Score: ", fs)


def showFeatureVector(data):
    response = requests.post("http://127.0.0.1:8000/featureVector", json=data)
    fv = response.json()
    st.write("Feature Vector: ", fv)




def main():
    st.subheader("Time Series Anomaly Detection")
    st.write("This page shows the feature vector,forecastability score and detects anomalies in the time series data")
    file = fileUploader()
    if file is not None:
        st.write("Preview")
        st.write(file.head())
        Data = file.to_dict(orient="records")
        data = {"Data": Data}


        if st.button("Show Feature Vector"):
            showFeatureVector(data)
            if st.button("Hide Feature Vector"):
                st.write("Feature Vector hidden")

        if st.button("Show Forecastability Score"):
            showForecastabilityScore(data)
            if st.button("Hide Forecastability Score"):
                st.write("Forecastability Score hidden")

        st.subheader("Anomalies")
        with st.form(key='anomalies_form'):
            fh = st.selectbox("Window size ", [1, 2, 3, 4, 5, 6, 7])
            frequency = st.selectbox(
                "Frequency",
                [
                    "D", "B", "H", "T", "S",
                    "L", "U", "N", "W", "M",
                    "SM", "BM", "CBM", "MS", "SMS",
                    "BMS", "CBMS", "Q", "BQ", "QS",
                    "BQS", "A", "BA", "AS", "BAS"
                ],
            )
            oos = st.number_input("Initial batch size ", min_value=1, value=120,max_value=len(Data))
            oos = len(Data) - oos
            submit_button = st.form_submit_button(label='Check for Anomalies')

            if submit_button:
                params={
                    "fh": fh,
                    "frequency": frequency,
                    "oos": oos
                }

                # show loading spinner until response is received
                with st.spinner(text="Detecting anomalies..."):
                    response = requests.post(
                        url="http://127.0.0.1:8000/anomalies",
                        json=data,
                        params=params
                    )
                output = response.json()
                st.write("Anomalies")
                st.write(output)

    else:
        st.write("Upload a file to get started")
    st.sidebar.success("Select ")


if __name__ == "__main__":
    main()


