"""
Copyright (c) 2023 Akhil Sharma. All rights reserved.

PyStoAnalyzer.
"""
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller 
from statsmodels.tsa.arima_model import ARIMA
from pmdarima.arima.utils import ndiffs
from typing import cast,List,TypeVar,Tuple,Any
plt.style.use(style="seaborn")

# class ModelStockData:

#     # User defined input for the train test data split
#     user_train_data = input()
#     user_test_data = input()

#     def preprocessing(col_name_for_closing_stock: str,csv_file=None):
#         df = pd.read_csv(stock.csv_path)

#         if col_name_for_closing_stock is not None:
#             df_close_values = df[col_name_for_closing_stock].copy
#         else:
#             df_close_values = df['closing_stock_data'].copy

#         #Check if the data is stationary or not
#         stationary_check = adfuller(df_close_values.dropna())
#         #Storing the p-value 
#         if(stationary_check[1]<0.05):
#             p_value = stationary_check[1]
#         else:
#             p_value = ndiffs(df_close_values, test='adf')

#         #Splitting the model into train and test data
#         number_of_testcases= int(len(df_close_values)*0.8)
#         train_data = df_close_values[:number_of_testcases]
#         test_data = df_close_values[number_of_testcases:] 

#         return p_value,train_data,test_data
    
#     #p_value-> is the number of autoregressive terms, 
#     # diff-> is the number of nonseasonal differences needed for stationarity, and. 
#     # lagg-> is the number of lagged forecast errors in the prediction equation.

#     def stock_arima(p_value: int,diff: int,lagg: int,csv_path: Any,user_train_data=None,user_test_data=None)-> Any:

#         if user_train_data is not None:
#             #Fitting the ARIMA Model to dataset
#             model = ARIMA(user_train_data,order=(p_value,diff,lagg))
#             result_analysis = model.fit(disp=0)

#             #Debugging the model 
#             #print(result_analysis.summary)

#             #Actual vs fitting analysis
#             # result_analysis.plot_predict(
#             #     start=1,
#             #     end=60,
#             #     dynamic=False,
#             # );

#             #Calculating the steps of the future
#             steps: str = input("Number of days in future to predict: ")

#             fc,conf = result_analysis.forecast(int(steps))
#             forecast = pd.Series(fc, index=user_test_data[:int(steps)].index)
#             Low_predictions = pd.Series(conf[:,0], index=user_test_data[:int(steps)].index)
#             High_predictions = pd.Series(conf[:,1], index=user_test_data[:int(steps)].index)
        
#         else:
#             #Fitting the ARIMA Model to dataset
#             model = ARIMA(train_data,order=(p_value,diff,lagg))
#             result_analysis = model.fit(disp=0)
#             model
#             #Debugging the model 
#             #print(result_analysis.summary)

#             #Actual vs fitting analysis
#             # result_analysis.plot_predict(
#             #     start=1,
#             #     end=60,
#             #     dynamic=False,
#             # );

#             #Calculating the steps of the future
#             steps: str = input("Number of days in future to predict: ")

#             fc,conf = result_analysis.forecast(int(steps))
#             forecast = pd.Series(fc, index=test_data[:int(steps)].index)
#             Low_predictions = pd.Series(conf[:,0], index=test_data[:int(steps)].index)
#             High_predictions = pd.Series(conf[:,1], index=test_data[:int(steps)].index)

#         return model,forecast,Low_predictions,High_predictions

class DataAnalysis:
    """Class for performing data analysis on stock data."""
    @staticmethod
    def prediction_analysis(
                        test_data,
                        steps: str,
                        forecast: list,
                        lower_predictions: list,
                        high_predictions: list)-> None:
            """Creates a comparison graph for the predicted and actual stock data.

            Args:
                test_data (pd.Series): The actual stock data.
                steps (str): The number of periods to forecast.
                forecast (pd.Series): The predicted stock data.
                lower_predictions (pd.Series): The lower bound of the prediction interval.
                high_predictions (pd.Series): The upper bound of the prediction interval.
            """

            plt.figure(figsize=(16,8))
            plt.plot(test_data[:int(steps)], label="actual")
            plt.plot(forecast,label="forecast")
            plt.fill_between(lower_predictions.index,lower_predictions,high_predictions,color="k",alpha=0.1)
            plt.title("Forecast vs Actual data")
            plt.legend(loc="upper left") 