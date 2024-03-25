# DataGenie-Hackathon

### 1. Checkpoint 1:
 - Generated synthetic data(5000 time series , each of 500 rows) for Prophet model to extract features and calculate forecastability score with it
 - Constructed feature vectors for each time series in the synthetic data and selected a representative from it
 - Finds the threshold for forecastability score, by iterating through different values of threshold and selecting the one which gives the least RMSE value when forecasted with the Sample Time Series data provided.

Challenges Faced :
- Deciding upon the threshold finding method.
- Filtering the features to be extracted from the time series data.
 