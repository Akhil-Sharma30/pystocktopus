# Copyright (c) 2023 Akhil Sharma. All rights reserved.
from __future__ import annotations
import logging  # Import the logging module

import mplfinance as fplt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import tensorflow as tf
from plotly.subplots import make_subplots
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adamax
from tqdm import tqdm  # Import tqdm for progress bar

## New implementation for RNN s
import torch
import torch.nn as nn
import torch.optim as optim
from tqdm import tqdm

# Configure logging
logging.basicConfig(
    filename="stock_model.log",  # Log file name
    filemode="a",  # Append to the log file
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
    level=logging.INFO,  # Log level
)


# Define a simple RNN class using PyTorch
class RNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, num_layers):
        super(RNN, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.rnn = nn.RNN(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        out, _ = self.rnn(x, h0)
        out = self.fc(out[:, -1, :])
        return out


class ModelStockData:
    def _csvDataCollection(
        csv_file: str, sequence_length, stock_closing_price_column_name: str
    ):
        """Collects and prepares data from a CSV file for training a sequential model."""
        logging.info("Starting CSV data collection from %s.", csv_file)

        try:
            dataframe = pd.read_csv(csv_file)
            data = dataframe[stock_closing_price_column_name].values.reshape(-1, 1)

            # Scale the data to be between 0 and 1
            scaler = MinMaxScaler()
            data = scaler.fit_transform(data)
            logging.info("Data shape after scaling: %s", data.shape)

            # Create sequences of data for training
            def create_sequences(data, seq_length):
                sequences = []
                for i in range(len(data) - seq_length):
                    x = data[i : i + seq_length]
                    y = data[i + seq_length]
                    logging.debug(
                        "Sequence length: %d, Target length: %d", len(x), len(y)
                    )
                    sequences.append((x, y))

                logging.info("Total sequences created: %d", len(sequences))
                return np.array(sequences)

            # Convert NumPy arrays to TensorFlow tensors
            X_tensorflow_train = tf.convert_to_tensor(data, dtype=tf.float32)
            y_tensorflow_train = tf.convert_to_tensor(data, dtype=tf.float32)

            logging.info("Data collection completed successfully.")

            return (
                X_tensorflow_train,
                y_tensorflow_train,
                scaler,
            )

        except Exception as e:
            logging.error("Error during CSV data collection: %s", str(e))
            raise

    def _mean_absolute_percentage_error(y_true, y_pred):
        """Calculates the mean absolute percentage error (MAPE) between two arrays."""
        try:
            mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
            logging.info("MAPE calculated successfully.")
            return mape
        except Exception as e:
            logging.error("Error in calculating MAPE: %s", str(e))
            raise

    @staticmethod
    def create_fit_train_rnn(
        csv_file: str,
        stock_closing_price_column_name: str,
        hidden_size: int = 5,
        epochs: int = 650,
        lr: float = 0.0008,
        num_layers: int = 4,
        progress_callback=None,
    ) -> None:
        """
        Creates, trains, and fits a Recurrent Neural Network (RNN) model for stock price prediction based on historical stock data.

        Logs the progress of each epoch and the loss, while displaying the progress bar using `tqdm`.

        Parameters
        ----------
        csv_file : str
            The path to the CSV file containing the stock data.
        hidden_size : int, optional
            The number of hidden units in each RNN layer (default is 5).
        epochs : int, optional
            The number of training epochs (default is 650).
        lr : float, optional
            The learning rate for the Adam optimizer (default is 0.0008).
        num_layers : int, optional
            The number of RNN layers in the model (default is 4).
        progress_callback : callable, optional
            A callback function that will be called at the end of each epoch with the current epoch number and loss value.
        stock_closing_price_column_name : str,
            The column name in the CSV file representing the stock's closing price.

        Returns
        -------
        None

        Raises
        ------
        Exception
            If any error occurs during model creation, fitting, or prediction.

        Example
        -------
        >>> create_fit_train_rnn("stock_data.csv", hidden_size=10, epochs=500, lr=0.001, num_layers=3)
        """

        logging.info("Creating and fitting RNN model with %d epochs.", epochs)

        try:
            # Step 1: Load and preprocess the CSV data
            dataframe = pd.read_csv(csv_file)
            data = dataframe[stock_closing_price_column_name].values.reshape(-1, 1)

            # Scale the data between 0 and 1
            scaler = MinMaxScaler()
            data = scaler.fit_transform(data)

            def create_sequences(data, seq_length=64):
                src = []
                dst = []
                for i in range(len(data) - seq_length):
                    x = data[i : i + seq_length]
                    y = data[i + seq_length]

                    src.append(x)
                    dst.append(y)
                logging.info("Total sequences for training: %d", len(src))
                return np.array(src), np.array(dst)

            x, y = create_sequences(data)

            # Convert to torch tensors
            X_tensor = torch.tensor(x, dtype=torch.float32)
            y_tensor = torch.tensor(y, dtype=torch.float32)

            # Step 2: Define the RNN model
            input_size = X_tensor.shape[2]  # Assuming 1 feature (closing price)
            output_size = 1

            model = RNN(input_size, hidden_size, output_size, num_layers)

            criterion = nn.MSELoss()
            optimizer = optim.Adam(model.parameters(), lr=lr)

            # Step 3: Train the RNN model
            for epoch in tqdm(range(epochs), desc="Training RNN model", unit="epoch"):
                model.train()
                optimizer.zero_grad()

                # Forward pass
                outputs = model(X_tensor)
                loss = criterion(outputs, y_tensor)

                # Backward pass and optimize
                loss.backward()
                optimizer.step()

                # If a progress callback is provided, update progress
                if progress_callback:
                    progress_callback(epoch + 1, loss.item())

                # Logging progress every 100 epochs
                if (epoch + 1) % 100 == 0:
                    logging.info(
                        f"Epoch [{epoch + 1}/{epochs}], Loss: {loss.item():.4f}"
                    )

            logging.info("Model fitting completed successfully.")

            # Step 4: Make predictions and calculate MAPE
            model.eval()
            with torch.no_grad():
                predicted_prices = model(X_tensor).numpy()

            # Inverse transform to get actual prices
            predicted_prices = scaler.inverse_transform(predicted_prices)
            y_actual = scaler.inverse_transform(y_tensor.numpy())

            mape_values = []
            for i in range(len(y_actual)):
                mape = (
                    np.mean(np.abs((y_actual[i] - predicted_prices[i]) / y_actual[i]))
                    * 100
                )
                mape_values.append(mape)

            min_mape_index = np.argmin(mape_values)
            logging.info("Lowest MAPE achieved at index %d.", min_mape_index)

            return predicted_prices[min_mape_index][0]

        except Exception as e:
            logging.error("Error in creating and fitting RNN model: %s", str(e))
            raise

    @staticmethod
    def create_and_fit_lstm_model(
        csv_file: str,
        sequence_length: int = 10,
        layers: int = 10,
        lstm_units: list | None = None,
        epochs=650,
        lr: float = 0.0008,
        stacked: bool = True,
        progress_callback=None,
        stock_closing_price_column_name: str = "closing_stock_data_GOOGL",
    ) -> None:
        """
        Creates and fits an LSTM model for stock price prediction based on historical stock data.

        Parameters
        ----------
        csv_file : str
            The path to the CSV file containing the stock data.
        sequence_length : int, optional
            The length of the sequence to be used for training (default is 10).
        layers : int, optional
            The number of layers for the LSTM model (default is 10).
        lstm_units : list or None, optional
            List of integers specifying the number of units in each LSTM layer. If None, defaults to [16].
        epochs : int, optional
            The number of training epochs (default is 650).
        lr : float, optional
            The learning rate for the Adamax optimizer (default is 0.0008).
        stacked : bool, optional
            If True, a stacked LSTM model will be used; otherwise, a single LSTM layer will be used (default is True).
        progress_callback : callable, optional
            A callback function that will be called at the end of each epoch with the current epoch number and loss value.
        stock_closing_price_column_name : str, optional
            The column name in the CSV file representing the stock's closing price (default is "closing_stock_data_GOOGL").

        Returns
        -------
        None

        Raises
        ------
        Exception
            If any error occurs during model creation, fitting, or prediction.
        """

        logging.info(f"Creating and fitting LSTM model using data from: {csv_file}")
        logging.info(
            f"Parameters: sequence_length={sequence_length}, layers={layers}, epochs={epochs}, lr={lr}, stacked={stacked}"
        )

        if lstm_units is None:
            lstm_units = [16]
            logging.info(
                f"No LSTM units specified, defaulting to {lstm_units} units per layer."
            )

        try:
            # Data preparation
            logging.info("Starting data collection and preparation.")
            X_tensorflow_train, y_tensorflow_train, scaler = (
                ModelStockData._csvDataCollection(
                    csv_file, sequence_length, stock_closing_price_column_name
                )
            )
            logging.info(
                "Data collection completed. Number of training samples: %d",
                len(X_tensorflow_train),
            )

            input_shape = (1, 1)
            # Model creation
            if stacked is False:
                logging.info("Creating a single LSTM layer model.")
                model = Sequential()
                model.add(LSTM(layers, activation="relu", input_shape=input_shape))
                model.add(Dense(1))
            else:
                logging.info("Creating a stacked LSTM model with multiple layers.")
                model = Sequential()
                model.add(LSTM(1, activation="relu", input_shape=input_shape))
                model.add(Dense(1))

            # Compile the model
            custom_optimizer = Adamax(
                learning_rate=lr, weight_decay=0.001, epsilon=1e-08
            )
            model.compile(optimizer=custom_optimizer, loss="mean_squared_error")
            logging.info(
                "Model compiled with Adamax optimizer and mean squared error loss."
            )

            # Define a custom callback to log progress
            class ProgressCallback(tf.keras.callbacks.Callback):
                def on_epoch_end(self, epoch, logs=None):
                    if progress_callback:
                        loss = logs.get("loss")
                        progress_callback(epoch + 1, loss)  # Update progress
                        logging.info(f"Epoch {epoch + 1}/{epochs}, Loss: {loss}")

            # Initialize tqdm for tracking epochs
            logging.info(f"Training model for {epochs} epochs with tqdm progress bar.")
            with tqdm(total=epochs, desc="Training Progress", unit="epoch") as pbar:

                class TqdmCallback(tf.keras.callbacks.Callback):
                    def on_epoch_end(self, epoch, logs=None):
                        pbar.update(1)  # Update tqdm for each epoch
                        if logs is not None:
                            loss = logs.get("loss")
                            pbar.set_postfix({"Loss": loss})
                            if progress_callback:
                                progress_callback(epoch + 1, loss)
                            logging.info(f"Epoch {epoch + 1}/{epochs}, Loss: {loss}")

                # Fit the model with the TqdmCallback
                model.fit(
                    X_tensorflow_train,
                    y_tensorflow_train,
                    epochs=epochs,
                    callbacks=[ProgressCallback(), TqdmCallback()],
                    verbose=0,  # Turn off verbose to avoid interfering with tqdm
                )

            logging.info("Model training completed successfully.")

            # Predict using the trained model
            logging.info("Making predictions on training data.")
            predicted_prices = model.predict(X_tensorflow_train)

            # Inverse transform to get actual stock prices
            predicted_prices = scaler.inverse_transform(predicted_prices)
            logging.info("Inverse transformation of predictions completed.")

            # Calculate MAPE for each prediction
            mape_values = []
            for i in range(len(X_tensorflow_train)):
                mape = ModelStockData._mean_absolute_percentage_error(
                    y_tensorflow_train[i], predicted_prices[i]
                )
                mape_values.append(mape)

            # Find the index with the minimum MAPE
            min_mape_index = np.argmin(mape_values)
            logging.info(
                "Lowest MAPE achieved at index %d with a value of %.4f.",
                min_mape_index,
                mape_values[min_mape_index],
            )

            return predicted_prices[min_mape_index][0]

        except Exception as e:
            logging.error(f"Error in creating and fitting LSTM model: {str(e)}")
            raise


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
