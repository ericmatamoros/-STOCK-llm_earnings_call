"""Function to download Financial Modeling Prep - Articles"""
import pandas as pd
import time

from llm_earnings_call import ARTICLES_PATH
from llm_earnings_call.settings import Settings
from ._utils import get_jsonparsed_data


def download_fmp_articles():
    "Download Financial Modeling Prep Articles"

    settings = Settings()
    secret_key = settings.fmp_api

    url_init = "https://financialmodelingprep.com/api/v3/fmp/articles?"
    news_json = []

    consecutive_fails = 0
    page = 1
    while consecutive_fails <= 3:
        print("Looping in: " + str(page))
        url = url_init + "&page=" + str(page) + "&size=1&apikey=" + secret_key
        parsed_url = get_jsonparsed_data(url)
        parsed_url = parsed_url['content']
            
        if len(parsed_url) <= 0:
                consecutive_fails += 1
                continue
        else:
             consecutive_fails = 0

        if (page % 100) == 0:
            time.sleep(40.0)
            
        parsed_url = pd.DataFrame.from_dict(parsed_url, orient='columns')
        news_json.append(parsed_url)
        print("Success for : " + str(page))
        parsed_url.to_pickle(ARTICLES_PATH / f"{str(page)}.pkl")

        page += 1

    if len(news_json) != 0:
        df_complete = pd.concat(news_json, sort = False)
        df_complete.to_pickle(ARTICLES_PATH / "fmp_df.pkl")
        
if __name__ == "__main__":
    download_fmp_articles()