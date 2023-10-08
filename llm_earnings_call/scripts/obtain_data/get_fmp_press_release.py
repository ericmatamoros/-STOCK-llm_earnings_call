"""Function to download Financial Modeling Prep - Press Release"""

import pandas as pd
import numpy as np
import time

from llm_earnings_call import DATA_PATH, PRESS_RELEASE_PATH
from llm_earnings_call.settings import Settings

from ._utils import get_jsonparsed_data


DATE_LIMIT = pd.to_datetime("2017-01-01")


def download_press_release(df: pd.DataFrame):
    "Download Financial Modeling Prep Press Release"

    settings = Settings()
    fmp_secret_key = settings.fmp_api

    ticker_list = np.unique(df['ticker'])

    url_init = "https://financialmodelingprep.com/api/v3/press-releases/"
    
    for ticker in ticker_list:
        news_json = []
        for page in range(0, 1000000000000):
            print("Looping in: " + str(page) + " for ticker: " + ticker)
            url = url_init + ticker + "?page=" + str(page) + "&apikey=" + fmp_secret_key
            parsed_url = get_jsonparsed_data(url)
            len_x = len(parsed_url) -1 
            
            if len(parsed_url) == 0:
                break

            if pd.Timestamp(parsed_url[len_x]['date']) < DATE_LIMIT:
                break

            if page % 100 == 0:
                time.sleep(40.0)
            
            parsed_url = pd.DataFrame.from_dict(parsed_url, orient='columns')
            news_json.append(parsed_url)
            print("Success for: " + str(page) + " for ticker: " + ticker)

        if len(news_json) != 0:
            df_complete = pd.concat(news_json, sort = False)
            df_complete.to_pickle(PRESS_RELEASE_PATH / f"{ticker}.pkl")
        

if __name__ == "__main__":
    download_press_release(pd.read_pickle(DATA_PATH / "main_df.pkl"))