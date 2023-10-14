# # Copyright (c) 2023 Akhil Sharma. All rights reserved.
# from __future__ import annotations

# import json
# import os

# import matplotlib.dates as mdates
# import numpy as np
# from matplotlib import pyplot as plt

# # from mplfinance import candlestick_ohlc


# class DisplayPattern:
#     # A function that loads pattern data
#     def load_patterns() -> list:
#         """A function that loads pattern data.

#         Patterns are store in /data/patterns directories, in json format.

#         :return: List of Pattern objects
#         """
#         patterns = []
#         pattern_directory = "../pystocktopus/Data/Pattern"
#         for filename in os.listdir(pattern_directory):
#             with open(os.path.join(pattern_directory, filename)) as json_file:
#                 try:
#                     data = json.load(json_file)

#                     pattern_name = data["pattern_name"]

#                     sups = []
#                     for json_support in data["sups"]:
#                         sup = TrendLineCriteria(
#                             json_support["id"],
#                             "SUPPORT",
#                             json_support["slope_min"],
#                             json_support["slope_max"],
#                         )
#                         sups.append(sup)

#                     ress = []
#                     for json_support in data["ress"]:
#                         res = TrendLineCriteria(
#                             json_support["id"],
#                             "RESISTANCE",
#                             json_support["slope_min"],
#                             json_support["slope_max"],
#                         )
#                         ress.append(res)

#                     intercepts = []
#                     for json_support in data["intercepts"]:
#                         intercept = InterceptCriteria(
#                             json_support["id"],
#                             json_support["sup"],
#                             json_support["res"],
#                             json_support["periods_till_intercept"],
#                         )
#                         intercepts.append(intercept)

#                     pattern = Pattern(pattern_name, sups, ress, intercepts)
#                     patterns.append(pattern)
#                 except (KeyError, json.decoder.JSONDecodeError) as err:
#                     print(
#                         f"Error in {DisplayPattern.load_patterns.__name__}: "
#                         f"{filename} incorrectly formatted.",
#                         end=" ",
#                     )
#                     print(err)

#         return patterns


# class TrendLineCriteria:
#     """
#     Object that stores trendline criteria for support and resistance lines.

#     Args:
#         tlc_id (int): The ID of the trendline criteria.
#         tlc_type (str): The type of the trendline criteria (either "support" or "resistance").
#         slope_min (float): The minimum slope of the trendline.
#         slope_max (float): The maximum slope of the trendline.
#     """

#     def __init__(self, tlc_id: int, tlc_type: str, slope_min: float, slope_max: float):
#         self.tlc_id = tlc_id
#         self.tlc_type = tlc_type
#         self.slope_min = slope_min
#         self.slope_max = slope_max


# class InterceptCriteria:
#     """
#     Object that stores intercept criteria for support and resistance lines.

#     Args:
#         int_id (int): The ID of the intercept criteria.
#         sup_id (int): The ID of the support trendline criteria.
#         res_id (int): The ID of the resistance trendline criteria.
#         periods_till_intercept (int): The number of periods until the intercept.
#     """

#     def __init__(
#         self, int_id: int, sup_id: int, res_id: int, periods_till_intercept: int
#     ):
#         self.int_id = int_id
#         self.sup_id = sup_id
#         self.res_id = res_id
#         self.periods_till_intercept = periods_till_intercept


# # Object to store chart pattern
# class Pattern:
#     """
#     Object to store chart pattern.

#     Args:
#         pattern_name (str): The name of the pattern.
#         sups (list[TrendLineCriteria]): A list of TrendLineCriteria objects for the support trendlines.
#         ress (list[TrendLineCriteria]): A list of TrendLineCriteria objects for the resistance trendlines.
#         intercepts (list[InterceptCriteria]): A list of InterceptCriteria objects for the intercepts.
#     """

#     def __init__(
#         self,
#         pattern_name: str,
#         sups: [TrendLineCriteria],
#         ress: [TrendLineCriteria],
#         intercepts: [InterceptCriteria],
#     ):
#         self.pattern_name = pattern_name
#         self.sups = sups
#         self.ress = ress
#         self.intercepts = intercepts

#     def __str__(self):
#         return (
#             f"name: {self.intercepts}, "
#             f"sups: {len(self.sups)}, "
#             f"ress: {len(self.ress)}, "
#             f"intercepts: {len(self.intercepts)}"
#         )


# class TrendLine:
#     """
#     Object that defines a trendline on a chart.

#     Args:
#         b (float): The y-intercept of the trendline.
#         m (float): The slope of the trendline.
#         touches (list[int]): A list of the indices of the points on the trendline.
#         first_day (int): The index of the first day on the trendline.
#     """

#     def __init__(self, b, m, touches, first_day):
#         self.b = b
#         self.m = m
#         self.touches = touches
#         self.first_day = first_day

#     def __repr__(self):
#         return f"TrendLine({self.b}, {self.m}, {self.touches}, {self.first_day})"

#     # A function to calculate the intercept point between two trendlines.
#     def intercept_point(self, other_line) -> (float, float):
#         """A function to calculate the intercept point between two trendlines.

#         :param other_line: A trendline
#         :return: A tuple in the form (x, y). None if other_trendline is None.
#         """
#         if other_line is None:
#             return None

#         intercept_x = (self.b - other_line.b) / (other_line.m - self.m)
#         intercept_y = self.b * intercept_x + self.b

#         return intercept_x, intercept_y


# class Chart:
#     """Object that holds all information needed to draw a chart"""

#     def __init__(
#         self,
#         symbol: str,
#         prices: list,
#         support: TrendLine,
#         resistance: TrendLine,
#         support_points: list,
#         resistance_points: list,
#         patterns: [Pattern],
#     ):
#         """
#         Initializes a new Chart object.

#         Args:
#             symbol (str): The symbol of the stock being charted.
#             prices (list): A list of the stock's prices.
#             support (TrendLine): A TrendLine object representing the support line.
#             resistance (TrendLine): A TrendLine object representing the resistance line.
#             support_points (list): A list of the indices of the support points.
#             resistance_points (list): A list of the indices of the resistance points.
#             patterns (list[Pattern]): A list of Pattern objects representing the patterns to detect.
#         """

#         self.symbol = symbol
#         self.prices = prices
#         self.support = support
#         self.resistance = resistance
#         self.support_points = support_points
#         self.resistance_points = resistance_points
#         self.patterns = patterns
#         self.detected_patterns = []
#         self.detect_pattern()

#     def __repr__(self):
#         return (
#             f"TrendLine({self.symbol}, {self.prices}, "
#             f"{self.support}, {self.resistance}), "
#             f"{self.support_points}, {self.resistance_points}"
#             f", {self.patterns})"
#         )

#     def detect_pattern(self):
#         """
#         Detects the patterns in the chart.

#         Sets the `detected_patterns` attribute to a list of trade criteria for the detected patterns.
#         """

#         for pattern in self.patterns:
#             pattern_found = True

#             for sup in pattern.sups:
#                 if self.support:
#                     if sup.slope_min and self.support.m < sup.slope_min:
#                         pattern_found = False
#                     if sup.slope_max and self.support.m > sup.slope_max:
#                         pattern_found = False
#                 else:
#                     pattern_found = False

#             for res in pattern.ress:
#                 if self.resistance:
#                     if res.slope_min and self.resistance.m < res.slope_min:
#                         pattern_found = False

#                     if res.slope_max and self.resistance.m > res.slope_max:
#                         pattern_found = False
#                 else:
#                     pattern_found = False

#             for intercept in pattern.intercepts:
#                 intercept_point = self.support.intercept_point(self.resistance)

#                 if intercept_point:
#                     detected_periods_till_intercept = intercept_point[0] - len(
#                         self.prices
#                     )

#                     if intercept_point and (
#                         detected_periods_till_intercept
#                         > intercept.periods_till_intercept
#                     ):
#                         pattern_found = False
#                 else:
#                     pattern_found = False

#             trade_criteria = None
#             if pattern_found:
#                 height_ratio = 0.70
#                 buy_threshold = 0.01

#                 print("Pattern Found - " + pattern.pattern_name)

#                 resistance_price = (
#                     self.resistance.m * self.support.first_day + self.resistance.b
#                 )
#                 support_price = self.support.m * self.support.first_day + self.support.b

#                 triangle_height = resistance_price - support_price
#                 print("Triangle Height: " + str(round(triangle_height, 2)))

#                 buy_price = resistance_price + (triangle_height * buy_threshold)
#                 print("Buy price: " + str(round(buy_price, 2)))

#                 sell_price = height_ratio * triangle_height + resistance_price
#                 print("Target price: " + str(round(sell_price, 2)))

#                 stop_price = resistance_price - (triangle_height * 0.1)
#                 print("Stop price: " + str(round(stop_price, 2)))

#                 profit_margin = (sell_price - buy_price) / buy_price * 100
#                 print("Profit Margin: " + str(round(profit_margin, 1)) + "%")

#                 loss_margin = (stop_price - buy_price) / buy_price * 100
#                 print("Down Side: " + str(round(loss_margin, 1)) + "%")

#                 self.detected_patterns.append(trade_criteria)


# # A function that draws the data on a matplotlib chart
# def draw_chart(chart_data: Chart) -> None:
#     """
#     Draws a chart of the given chart data.

#     Args:
#         chart_data (Chart): The chart data to draw.
#     """
#     ax1 = plt.subplot2grid((1, 1), (0, 0))
#     candlestick_ohlc(
#         ax1, chart_data.prices.values, width=0.0001, colorup="g", colordown="r"
#     )
#     ax1.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
#     plt.title(chart_data.symbol)

#     for label in ax1.xaxis.get_ticklabels():
#         label.set_rotation(45)

#     # Plot points for each maxima/minima found
#     for i in chart_data.support_points:
#         plt.plot(chart_data.prices["datetime"][i], chart_data.prices["low"][i], "b+")

#     for i in chart_data.resistance_points:
#         plt.plot(chart_data.prices["datetime"][i], chart_data.prices["high"][i], "y+")

#     axes = plt.gca()

#     ymin, ymax = axes.get_ylim()
#     xmin, xmax = axes.get_xlim()

#     x_vals = np.array(range(len(chart_data.prices["datetime"])))
#     x_dates = np.array(chart_data.prices["datetime"])

#     if chart_data.resistance:
#         y_vals_res = chart_data.resistance.m * x_vals + chart_data.resistance.b
#         plt.plot(x_dates, y_vals_res, "--")

#     if chart_data.support:
#         y_vals_sup = chart_data.support.m * x_vals + chart_data.support.b
#         plt.plot(x_dates, y_vals_sup, "--")

#     # re-set the y limits
#     axes.set_ylim(ymin, ymax)
#     axes.set_xlim(xmin, xmax)
#     plt.show()
