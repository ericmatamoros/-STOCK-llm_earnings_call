"""
Top-level package global definitions
"""
import os

from pathlib import Path


BASE_PATH = Path(os.path.dirname(__file__))
CONFIG_PATH = BASE_PATH / "config"
DATA_PATH = BASE_PATH / "data"
DAILY_SENTIMENT_PATH = DATA_PATH / "daily_market_sentiment"
EARNINGS_CALL_PATH = DATA_PATH / "earning_calls_financialmodeling"
STOCK_NEW_PATH = DATA_PATH / "news"
ARTICLES_PATH = DATA_PATH / "articles"
PRESS_RELEASE_PATH = DATA_PATH / "press_release"