import numpy as np
import pandas as pd
import time
import os
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller #pip install statsmodels
from pmdarima.arima.utils import ndiffs # pip install --skip-lock pmdarima

plt.style.use(style="seaborn")

df = pd.read_csv('path')

df_close_values = df['c'].copy
