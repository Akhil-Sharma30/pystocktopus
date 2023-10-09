import pytest

from pystocktopus.stock_forecasting import ModelStockData

def test__csvDataCollection():
    """Tests the `_csvDataCollection()` method."""

    # Arrange
    csv_file = "tests/stock_data-2.csv"
    sequence_length = 10
    stock_closing_price_column_name = "closing_stock_data_SONY"

    # Act
    X_tensorflow_train, y_tensorflow_train, X_tensorflow_test, y_tensorflow_test, scaler = ModelStockData._csvDataCollection(
        csv_file, sequence_length, stock_closing_price_column_name
    )

    # Assert
    assert X_tensorflow_train.shape[0] == y_tensorflow_train.shape[0]
    assert X_tensorflow_test.shape[0] == y_tensorflow_test.shape[0]
    assert isinstance(scaler, MinMaxScaler)


def test_create_and_fit_lstm_model():
    """Tests the `create_and_fit_lstm_model()` method."""

    # Arrange
    csv_file = "test_data.csv"
    sequence_length = 10
    layers = 50
    lstm_units = [16]
    epochs = 50
    lr = 0.0008
    stacked = False
    stock_closing_price_column_name = "closing_stock_data_SONY"

    # Act
    predicted_value = ModelStockData.create_and_fit_lstm_model(
        csv_file,
        sequence_length,
        layers,
        lstm_units,
        epochs,
        lr,
        stacked,
        stock_closing_price_column_name,
    )

    # Assert
    assert isinstance(predicted_value, float)