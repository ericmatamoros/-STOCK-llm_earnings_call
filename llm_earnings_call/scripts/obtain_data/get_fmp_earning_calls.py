"""Function to download Financial Modeling Prep - Earnings Call"""
import pandas as pd
import numpy as np
import time
from datetime import datetime

from os import listdir
from os.path import isfile, join

from llm_earnings_call import DATA_PATH, EARNINGS_CALL_PATH
from llm_earnings_call.settings import Settings

from ._utils import get_jsonparsed_data, expand_grid

FIRST_YEAR = 1999
LAST_YEAR = datetime.now().year + 1

def download_earnings_call_fmp(df: pd.DataFrame):
    "Download Financial Modeling Prep Earnings Call"

    settings = Settings()
    fmp_secret_key = settings.fmp_api

    # Restart from last available ticker
    ticker_list = _restart_last(df.copy(), EARNINGS_CALL_PATH)

    url_init = "https://financialmodelingprep.com/api/v3/earning_call_transcript/"

    years_array = range(FIRST_YEAR, LAST_YEAR)
    quarters_array = range(1, 5)
    combs = {'years': years_array, 'quarters': quarters_array}
    combs = expand_grid(combs)
    combs.sort_values(by = 'years', inplace = True)
    
    # Loop over every ticker
    for ticker in ticker_list:
        earnings_json = []
        
        counter  = 0
        for year, quarter in zip(combs['years'], combs['quarters']):
            print("Looping in: " + str(year) + " and quarter : " + str(quarter) + " for ticker: " + ticker)
            url = url_init + ticker + "?quarter=" + str(quarter) + "&year=" + str(year) + "&apikey=" + fmp_secret_key
            parsed_url = get_jsonparsed_data(url)
            counter += 1

            if counter % 100 == 0:
                time.sleep(40.0)
                
            if len(parsed_url) == 0:
                continue
                
            parsed_url = pd.DataFrame.from_dict(parsed_url, orient='columns')
            earnings_json.append(parsed_url)
            print("Success for: " + str(year) + " and quarter : " + str(quarter) + " for ticker: " + ticker)

        if len(earnings_json) != 0:
            print("Storing for ticker: " + ticker)
            df_complete = pd.concat(earnings_json, sort = False)
            df_complete.to_pickle(EARNINGS_CALL_PATH / ticker + ".pkl")
        

def _restart_last(df: pd.DataFrame, earnings_path: str) -> list:
    onlyfiles = [f for f in listdir(earnings_path) if isfile(join(earnings_path, f))]
    if len(onlyfiles) != 0:
        onlyfiles = [s.replace(".pkl", "") for s in onlyfiles]
        ticker_list = np.unique(df[~df['ticker'].isin(onlyfiles)]['ticker'])
    else:
        ticker_list = np.unique(df['ticker'])
        
    return ticker_list

if __name__ == "__main__":
    download_earnings_call_fmp(df = pd.read_pickle(DATA_PATH / "main_df.pkl"))