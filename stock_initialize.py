from polygon import RESTClient
import config
import requests
from typing import cast,List
from urllib3 import HTTPResponse
import json

# API Declarations
API_Key = config.api_key
client = RESTClient(api_key=API_Key)

