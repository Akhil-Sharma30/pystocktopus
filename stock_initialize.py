from polygon import RESTClient
import config
import requests
from typing import cast,List
from urllib3 import HTTPResponse
import json

# API Declarations
API_Key = config.api_key
client = RESTClient(api_key=API_Key)

class stock:
    #Initializing the parameters for the stock preditions
    ticker: List[str]=input("Give your stock name {eg: Apple:APPL}: ")
    timespan: str = input("Give size of the time window {eg: day}: ")
    multiplier: int = input("Give size of the timespan multiplier {eg: 1}: ")
    start_date: str = input("Give the starting date {format '2023-0X-XX'} : ")
    end_date: str = input("Give the ending date {format '2023-0X-XX'} : ")