"""
Copyright (c) 2023 Akhil Sharma. All rights reserved.

Stock_Analysiss.
"""
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller 
from statsmodels.tsa.arima_model import ARIMA
from pmdarima.arima.utils import ndiffs 
from StockyProphet.stock_analysis_tool import csv_data_extractor
plt.style.use(style="seaborn")

class ModelStock:
    def model_data(csv_path: any,row_name_for_closing_stock: str)-> any:
        df = pd.read_csv(csv_path)

        if row_name_for_closing_stock:
            df_close_values = df[row_name_for_closing_stock].copy
        else:
            df_close_values = df['closing_stock_data'].copy

        #Check if the data is stationary or not
        stationary_check = adfuller(df_close_values.dropna())
        #Storing the p-value 
        if(stationary_check[1]<0.05):
            p_value = stationary_check[1]
        else:
            p_value = ndiffs(df_close_values, test='adf')
    
        #p_value-> is the number of autoregressive terms, 
        # diff-> is the number of nonseasonal differences needed for stationarity, and. 
        # lagg-> is the number of lagged forecast errors in the prediction equation.

        #Splitting the model into train and test data
        number_of_testcases= int(len(df_close_values)*0.8)
        train_data = df_close_values[:number_of_testcases]
        test_data = df_close_values[number_of_testcases:] 
        
        #Fitting the ARIMA Model to dataset
        model = ARIMA(train_data,order=(p_value,diff,lagg))
        result_analysis = model.fit(disp=0)

        #Debugging the model 
        #print(result_analysis.summary)

        #Actual vs fitting analysis
        # result_analysis.plot_predict(
        #     start=1,
        #     end=60,
        #     dynamic=False,
        # );

        #Calculating the steps of the future
        steps: str = input("Number of days in future to predict: ")

        fc,se,conf = result_analysis.forecast(int(steps))
        forecast = pd.Series(fc, index=test_data[:int(steps)].index)
        Low_predictions = pd.Series(conf[:,0], index=test_data[:int(steps)].index)
        High_predictions = pd.Series(conf[:,1], index=test_data[:int(steps)].index)

        return model,forecast,Low_predictions,High_predictions

    #Create a comparsion graph for the data 
    def model_prediction_analysis(test_data: any,steps: str,forecast: list,lower_predictions: list,high_predictions: list)-> None:
        plt.figure(figsize=(16,8))
        plt.plot(test_data[:int(steps)], label="actual")
        plt.plot(forecast,label="forecast")
        plt.fill_between(lower_predictions.index,lower_predictions,high_predictions,color="k",alpha=0.1)
        plt.title("Forecast vs Actual data")
        plt.legend(loc="upper left")
