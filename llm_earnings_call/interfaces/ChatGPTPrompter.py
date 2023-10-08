"""Class to ask Large Language Model about a specific property."""

import pandas as pd
import numpy as np
import openai
import json


class ChatGPTPrompter:
    def __init__(self, api_key: str, llm_model: str = '"gpt-3.5-turbo"') -> None:
        self._api_key = api_key
        self._llm_model = llm_model

    
    def obtain_earnings_call_info(self, ticker: str, cfo_intervention: str):

        def _get_completion(api_key: str, prompt: str, model : str):
            openai.api_key =api_key
            messages = [{"role": "user", "content": prompt}]
            response = openai.ChatCompletion.create(
                model=self._llm_model,
                messages=messages,
                temperature=0,
            )
            return response.choices[0].message["content"]
        
        prompt = f"""Analyze financial statement for company {ticker} and provide me a json with different
          growth/loss metrics, the earnings per share (growth or loss), and interpret if the overall sentiment 
          is positive or negative. Give me the output in a json-friendly format  {cfo_intervention}"""
        
        output = _get_completion(self._api_key, prompt, self._llm_model)

        # Removing newline characters and spaces from the string response
        cleaned_response = output.replace('\n', '').replace(' ', '')

        # Converting the cleaned string response to a dictionary
        response_dict = json.loads(cleaned_response)

        # Convert values in the dictionary using the convert_values function
        for key, value in response_dict.items():
            response_dict[key] = _convert_values(value)

        return response_dict



def _convert_values(value):
    try:
        # Convert percentage strings to floats
        if '%' in value:
            return float(value.strip('%'))
        # Convert "N/A" to NaN
        elif value.lower() == 'n/a':
            return np.nan
        else:
            # Handle other types of values if needed
            return value
    except ValueError:
        # Handle invalid float conversion if needed
        return value