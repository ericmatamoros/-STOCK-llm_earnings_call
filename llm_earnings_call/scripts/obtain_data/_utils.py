""" Utils file"""
import pandas as pd
from itertools import product
from urllib.request import urlopen
import certifi
import json

def get_jsonparsed_data(url: str):
    try: 
        response = urlopen(url, cafile=certifi.where())
        data = response.read().decode("utf-8")
        return json.loads(data)
    except:
        return []
    

def expand_grid(dictionary: dict):
   return pd.DataFrame([row for row in product(*dictionary.values())], 
                       columns=dictionary.keys())