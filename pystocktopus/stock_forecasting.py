# Copyright (c) 2023 Akhil Sharma. All rights reserved.
from __future__ import annotations

import mplfinance as fplt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import tensorflow as tf
from plotly.subplots import make_subplots
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam


class ModelStockData:
    def _csvDataCollection(
        csv_file: str, sequence_length, stock_closing_price_column_name: str
    ):
        """Collects and prepares data from a CSV file for training a sequential model.

        Args:
            csv_file (str): The path to the CSV file containing the data.
            sequence_length (int): The length of the sequences to create from the data.
            stock_closing_price_column_name (str): The name of the column in the CSV file containing
                the stock closing price data.

        Returns:
            tuple[tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor]: A tuple of four TensorFlow tensors,
                representing the training input sequences (X), training target values (y), test input
                sequences (X_test), and test target values (y_test).
        """
        dataframe = pd.read_csv(csv_file)
        data = dataframe[stock_closing_price_column_name].values.reshape(-1, 1)

        # Scale the data to be between 0 and 1
        scaler = MinMaxScaler()
        data = scaler.fit_transform(data)

        # Split the data into training and testing sets
        train_size = int(len(data) * 0.8)
        train_data = data[:train_size]
        test_data = data[train_size:]

        # Create sequences of data for training
        def create_sequences(data, seq_length):
            sequences = []
            for i in range(len(data) - seq_length):
                X = data[i : i + seq_length]
                y = data[i + seq_length]
                sequences.append((X, y))
            return np.array(sequences)

        seq_length = sequence_length
        train_sequences = create_sequences(train_data, seq_length)
        test_sequences = create_sequences(test_data, seq_length)

        # Separate input sequences (X) and target values (y)
        X_train = np.stack(train_sequences[:, 0])  # Stack input sequences
        y_train = np.stack(train_sequences[:, 1])  # Stack target sequences

        X_test = np.stack(test_sequences[:, 0])  # Stack input sequences
        y_test = np.stack(test_sequences[:, 1])  # Stack target sequences

        # Convert NumPy arrays to TensorFlow tensors
        X_tensorflow_train = tf.convert_to_tensor(X_train, dtype=tf.float32)
        y_tensorflow_train = tf.convert_to_tensor(y_train, dtype=tf.float32)
        X_tensorflow_test = tf.convert_to_tensor(X_test, dtype=tf.float32)
        y_tensorflow_test = tf.convert_to_tensor(y_test, dtype=tf.float32)

        return (
            X_tensorflow_train,
            y_tensorflow_train,
            X_tensorflow_test,
            y_tensorflow_test,
            scaler,
        )

    def _mean_absolute_percentage_error(y_true, y_pred):
        """Calculates the mean absolute percentage error (MAPE) between two arrays.

        Args:
            y_true (np.ndarray): The true values.
            y_pred (np.ndarray): The predicted values.

        Returns:
            float: The MAPE.
        """
        return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

    def create_and_fit_lstm_model(
        csv_file: str,
        sequence_length: int = 10,
        layers: int = 10,
        lstm_units: list | None = None,
        epochs=50,
        lr: float = 0.0008,
        stacked: bool = False,
        stock_closing_price_column_name: str = "closing_stock_data_SONY",
    ) -> None:
        """Creates and fits a long short-term memory (LSTM) model to predict stock prices, and returns the predicted value with the lowest MAPE.

        Args:
            csv_file (str): The path to the CSV file containing the stock price data.
            sequence_length (int): The length of the sequences to create from the data.
            layers (int): The number of LSTM layers in the model.
            lstm_units (list): A list of the number of units in each LSTM layer.
            epochs (int): The number of epochs to train the model for.
            lr (float): The learning rate to use during training.
            stacked (bool): Whether to use a stacked LSTM model or Single Layer LSTM.
            stock_closing_price_column_name (str): The name of the column in the CSV file containing
                the stock closing price data.

        Returns:
            float: The predicted stock price with the lowest MAPE.
        """
        # setting the from the user csv file
        if lstm_units is None:
            lstm_units = [16]
        (
            X_tensorflow_train,
            y_tensorflow_train,
            X_tensorflow_test,
            y_tensorflow_test,
            scaler,
        ) = ModelStockData._csvDataCollection(
            csv_file, sequence_length, stock_closing_price_column_name
        )

        input_shape = (X_tensorflow_train.shape[1], X_tensorflow_train.shape[2])
        if stacked is False:
            model = Sequential()
            model.add(LSTM(layers, activation="relu", input_shape=input_shape))
            model.add(Dense(1))
        else:
            model = Sequential()
            model.add(LSTM(1, activation="relu", input_shape=input_shape))
            model.add(Dense(1))

        custom_optimizer = Adam(learning_rate=lr)
        model.compile(optimizer=custom_optimizer, loss="mean_squared_error")
        model.fit(X_tensorflow_train, y_tensorflow_train, epochs=epochs)
        predicted_prices = model.predict(X_tensorflow_test)

        # Inverse transform the scaled data to get the actual stock prices
        predicted_prices = scaler.inverse_transform(predicted_prices)
        mape_values = []

        # Calculate MAPE for each prediction and store it in mape_values
        for i in range(len(y_tensorflow_test)):
            mape = ModelStockData._mean_absolute_percentage_error(
                y_tensorflow_test[i], predicted_prices[i]
            )
            mape_values.append(mape)

        # Find the index of the prediction with the lowest MAPE
        min_mape_index = np.argmin(mape_values)

        # Get the corresponding predicted value
        return predicted_prices[min_mape_index][0]
        # print(predicted_value)


class DataAnalysis:
    """Class for performing data analysis on stock data."""

    @staticmethod
    def stock_analysis(
        csv_file: str, stock_closing_price_column_name: str = "closing_stock_data_SONY"
    ) -> None:
        """Performs a basic analysis of a stock price dataset.

        Args:
            csv_file (str): The path to the CSV file containing the stock price data.
            stock_closing_price_column_name (str): The name of the column in the CSV file containing
                the stock closing price data.

        Returns:
            None
        """
        data = pd.read_csv(csv_file, index_col=0, parse_dates=True)
        fplt.plot(data, type="candle", title="Google", ylabel="Price ($)")

        fig = go.Figure(
            data=go.Scatter(
                x=data.index,
                y=data[stock_closing_price_column_name],
                mode="lines+markers",
            )
        )
        fig.show()

    def interactive_sticks(
        csv_file: str, stock_closing_price_column_name: str = "closing_stock_data_SONY"
    ):
        """Creates an interactive candlestick chart of a stock price dataset.

        Args:
            csv_file (str): The path to the CSV file containing the stock price data.
            stock_closing_price_column_name (str): The name of the column in the CSV file containing
                the stock closing price data.

        Returns:
            None
        """
        data = pd.read_csv(csv_file, index_col=0, parse_dates=True)
        fig3 = make_subplots(specs=[[{"secondary_y": True}]])
        fig3.add_trace(
            go.Candlestick(
                x=data.index,
                close=data[stock_closing_price_column_name],
            )
        )

    def interactive_bar(
        csv_file: str,
        stock_closing_price_column_name: str = "closing_stock_data_SONY",
        volume_column_name: str = "Volume",
        title_name: str = "data",
    ):
        """Creates an interactive bar chart of a stock price dataset with volume and 20-day moving average.

        Args:
            csv_file (str): The path to the CSV file containing the stock price data.
            stock_closing_price_column_name (str): The name of the column in the CSV file containing
                the stock closing price data.
            volume_column_name (str): The name of the column in the CSV file containing
                the volume data.
            title_name (str): The title of the chart.

        Returns:
            None
        """
        data = pd.read_csv(csv_file, index_col=0, parse_dates=True)
        fig3 = make_subplots(specs=[[{"secondary_y": True}]])
        fig3.add_trace(
            go.Bar(x=data.index, y=data[volume_column_name], name=volume_column_name),
            secondary_y=True,
        )
        fig3.update_layout(xaxis_rangeslider_visible=False)
        fig3.show()
        fig3.add_trace(
            go.Scatter(
                x=data.index,
                y=data[stock_closing_price_column_name].rolling(window=21).mean(),
                marker_color="blue",
                name="20 Day MA",
            )
        )
        fig3.add_trace(
            go.Bar(x=data.index, y=data[volume_column_name], name=volume_column_name),
            secondary_y=True,
        )
        fig3.update_layout(title={"text": title_name, "x": 0.5})
        fig3.update_yaxes(range=[0, 70000000], secondary_y=True)
        fig3.update_yaxes(visible=False, secondary_y=True)
        fig3.update_layout(xaxis_rangeslider_visible=False)  # hide range slider
        fig3.show()
