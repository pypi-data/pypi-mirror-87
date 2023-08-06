""" Test external APIs """

import covid_alarm_clock.fetch_data as fd
from covid_alarm_clock.fetch_data import fetch_news, fetch_weather

# Assume the user has put in a correct key in their config...
def test_fetch_news_with_current_key():
    assert fetch_news().status_code == 200

# Assume the user has put in a correct key in their config...
def test_fetch_weather_with_current_key():
    assert fetch_weather().status_code == 200

def test_fetch_news_with_incorrect_key():
    fd.NEWS_SERVICE["api-key"] = ""
    assert fetch_news().status_code == 401

def test_fetch_weather_with_incorrect_key():
    fd.WEATHER_SERVICE["api-key"] = ""
    assert fetch_weather().status_code == 401