""" Module to fetch news, weather, and UK COVID-19 data from restful APIs. """
import os
import json
import logging
from typing import Dict, Any
import requests
from requests import Response
from uk_covid19 import Cov19API

# Set up logger
logger = logging.getLogger(__name__)
logger_path = os.path.join(os.path.dirname(__file__), 'app.log')
logging.basicConfig(filename=logger_path, level=logging.INFO, format="[%(asctime)s] [%(name)s ~ %(threadName)s] [%(levelname)s]: %(message)s", datefmt="%Y/%m/%d %H:%M:%S")
logger.propagate = False

# Load our configuration
config_path = os.path.join(os.path.dirname(__file__), 'config.json')
try:
    with open(config_path) as config:
        logger.info("Reading config...")
        data = json.load(config)
except FileNotFoundError as e:
    logger.info("Could not open config. Full strack trace: {}".format(e))

# Read from our configuration and set constants
NEWS_SERVICE = data["external-services"]["news"]
COVID_SERVICE = data["external-services"]["covid"]
WEATHER_SERVICE = data["external-services"]["weather"]

def fetch_news() -> Response:
    """
    This function will fetch the news and if any news matches the criteria,
    a new notification will be added to the list of notifications.

    Returns:
    (Response) -- A response object returned by the news API from our GET request.
    """

    if NEWS_SERVICE["use-sources"] == "y":
        request_url = "{}sources={}&q={}&apiKey={}".format(NEWS_SERVICE["url"], NEWS_SERVICE["sources"], NEWS_SERVICE["search-term"], NEWS_SERVICE["api-key"])
    else:
        request_url = "{}country={}&category={}&q={}&apiKey={}".format(NEWS_SERVICE["url"], NEWS_SERVICE["country"], NEWS_SERVICE["category"], NEWS_SERVICE["search-term"], NEWS_SERVICE["api-key"])

    response = requests.get(request_url)

    logger.info("Fetching news data...")
    return response

def fetch_weather() -> Response:
    """
    This function will fetch the latest weather data, and if the weather data matches the criteria,
    a new notification will be added to the list of notifications.

    Returns:
    (Response) -- A response object returned by the weather API from our GET request.
    """

    request_url = "{}q={}&units={}&appid={}".format(WEATHER_SERVICE["url"], WEATHER_SERVICE["city"], WEATHER_SERVICE["units"], WEATHER_SERVICE["api-key"])
    response = requests.get(request_url)

    logger.info("Fetching news data...")
    return response

def fetch_covid() -> Dict[str, Any]:
    """
    This function will fetch the latest COVID data and if the covid data matches the criteria,
    a new notification will be added to the list of notifications.

    Returns:
    (JSON) - A JSON object returned by the COVID API.
    """

    filters = []
    if COVID_SERVICE["filter-by"] == "overview":
        filters = ['areaType=overview']
    elif COVID_SERVICE["filter-by"] == "nation":
        filters = [
            'areaType=nation',
            'areaName={}'.format(COVID_SERVICE["nation"])
        ]
    elif COVID_SERVICE["filter-by"] == "region":
        filters = [
            'areaType=region',
            'areaName={}'.format(COVID_SERVICE["region"])
        ]

    structure = {
        "date": "date",
        "areaName": "areaName",
        "areaCode": "areaCode",
        "newCasesByPublishDate": "newCasesByPublishDate",
        "cumCasesByPublishDate": "cumCasesByPublishDate",
        "newDeathsByDeathDate": "newDeathsByDeathDate",
        "cumDeathsByDeathDate": "cumDeathsByDeathDate"
    }

    covid_api = Cov19API(filters=filters, structure=structure)

    logger.info("Fetching COVID data...")
    covid_data = covid_api.get_json()
    return covid_data
