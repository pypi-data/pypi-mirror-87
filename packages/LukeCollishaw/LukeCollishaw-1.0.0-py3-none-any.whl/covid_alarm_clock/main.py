""" Main application module to handle Flask web interface, as well as alarm and notification logic and schedulers. """

import os
import json
import logging
from datetime import datetime
from flask import Flask, render_template, request, Markup
import pyttsx3
import dateutil.parser
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.base import JobLookupError
from fetch_data import fetch_news, fetch_weather, fetch_covid

# Create our Flask app object
app = Flask(__name__)

# Set up logger
logger = logging.getLogger(__name__)
logger_path = os.path.join(os.path.dirname(__file__), 'app.log')
logging.basicConfig(filename=logger_path, level=logging.INFO, format="[%(asctime)s] [%(name)s ~ %(threadName)s] [%(levelname)s]: %(message)s", datefmt="%Y/%m/%d %H:%M:%S")

# Load our configuration
config_path = os.path.join(os.path.dirname(__file__), 'config.json')
try:
    with open(config_path) as config:
        logger.info("Reading config...")
        data = json.load(config)
except FileNotFoundError as e:
    logger.info("Could not open config. Full strack trace: {}".format(e))

# Read from our configuration and set constants
FAVICON = data["static-file-paths"]["favicon"]
IMAGE = data["static-file-paths"]["image"]
APP_NAME = data["app-name"]
NEWS_SERVICE = data["external-services"]["news"]
COVID_SERVICE = data["external-services"]["covid"]
WEATHER_SERVICE = data["external-services"]["weather"]
REFRESH_RATE = data["external-services"]["refresh-rate"]

# Create our list of notifications and our list of alarms
# Restrictions for notifications: must have a unique title, and some content.
# Restrictions for alarms: must have a unique title, content which comprises the date, time, whether to show weather, and whether to show news. Should also have weather as a boolean, and news as a boolean.
notifications = []
completed_notifications = []
alarms = []
active_weather_notification = {"title": "", "content": "", "weather": []}
latest_covid_notification = {"title": "", "content": ""}

# Notifications
def fetch_for_notifications(news: bool, weather: bool, covid: bool) -> None:
    """
    Depending on the boolean keyword arguments 'news', 'covid', and 'weather', where any of these arguments are True, it will call the function jobs to fetch data
    from the respective API. For example, if news is True, it will call a function to fetch the latest news from a news API. It will then put itself back
    into the scheduler's queue.

    Keyword arguments:
    news (bool) -- Whether to fetch the latest news
    covid (bool) -- Whether to fetch the latest COVID-19 updates
    weather (bool) -- Whether to fetch the latest weather updates

    No return argument.
    """

    if news:
        if fetch_news().status_code == 200:
            logger.info("Fetched news data successfully!")
            news_data = fetch_news().json()
            articles = news_data["articles"]

            for article in articles:
                title = article["title"]
                content = Markup('<a href="{}">View full article</a>'.format(article["url"]))
                notification = {"title": title, "content": content}
                if notification not in notifications and notification not in completed_notifications:
                    notifications.append(notification)
                    logger.info("New news notification!")
        else:
            logger.warning("Was unable to fetch news data: response returned status code {}!".format(fetch_news().status_code))

    if weather:
        if fetch_weather().status_code == 200:
            logger.info("Fetched weather data successfully!")
            weather = fetch_weather().json()
            
            weather_types = WEATHER_SERVICE["notify-automatically-for"]
            current_weather_types = weather["weather"]
            formatted_current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            formatted_title = Markup("Weather at: <i>{}</i>".format(formatted_current_time))

            temperature = str(weather["main"]["temp"])
            if WEATHER_SERVICE["units"] == "metric":
                temperature += " degrees celcius"
            elif WEATHER_SERVICE["units"] == "imperial":
                temperature += " degrees faranheit"
            elif WEATHER_SERVICE["units"] == "standard":
                temperature += " kelvin"

            raw_content = {"weather": [], "temperature": temperature}

            if weather_types["thunderstorm"] == "y":
                SEARCH_FOR = "Thunderstorm"
                # Can be multiple weather types simultaneously
                for current_weather_type in current_weather_types:
                    if str(current_weather_type["main"]) == SEARCH_FOR:
                        raw_content["weather"].append(current_weather_type["description"])
            if weather_types["drizzle"] == "y":
                SEARCH_FOR = "Drizzle"
                for current_weather_type in current_weather_types:
                    if str(current_weather_type["main"]) == SEARCH_FOR:
                        raw_content["weather"].append(current_weather_type["description"])
            if weather_types["rain"] == "y":
                SEARCH_FOR = "Rain"
                for current_weather_type in current_weather_types:
                    if str(current_weather_type["main"]) == SEARCH_FOR:
                        raw_content["weather"].append(current_weather_type["description"])
            if weather_types["snow"] == "y":
                SEARCH_FOR = "SNOW"
                for current_weather_type in current_weather_types:
                    if str(current_weather_type["main"]) == SEARCH_FOR:
                        raw_content["weather"].append(current_weather_type["description"])
            if weather_types["atmosphere"] == "y":
                SEARCH_FOR = range(700, 800)
                for current_weather_type in current_weather_types:
                    if current_weather_type["id"] in SEARCH_FOR:
                        raw_content["weather"].append(current_weather_type["description"])
            if weather_types["clear"] == "y":
                SEARCH_FOR = "Clear"
                for current_weather_type in current_weather_types:
                    if str(current_weather_type["main"]) == SEARCH_FOR:
                        raw_content["weather"].append(current_weather_type["description"])
            if weather_types["clouds"] == "y":
                SEARCH_FOR = "Clouds"
                for current_weather_type in current_weather_types:
                    if str(current_weather_type["main"]) == SEARCH_FOR:
                        raw_content["weather"].append(current_weather_type["description"])
            
            raw_content_weather_as_string = ""
            for item in raw_content["weather"]:
                # If first item
                if raw_content_weather_as_string == "":
                    raw_content_weather_as_string += item
                else:
                    raw_content_weather_as_string += ", "
                    raw_content_weather_as_string += item

            formatted_content = Markup("Weather is currently: {}<br>Temperature is currently: {}".format(raw_content_weather_as_string, temperature))
            notification = {"title": formatted_title, "content": formatted_content, "weather": raw_content["weather"]}

            # If the type of weather has changed then and only then do we want to produce a new notification
            global active_weather_notification
            if notification["weather"] != active_weather_notification["weather"]:
                active_weather_notification = notification
                notifications.append(notification)
                logger.info("New weather notification!")
        else:
            logger.warning("Was unable to fetch weather data: response returned status code {}!".format(fetch_news().status_code))
    if covid:
        covid_data = fetch_covid()
        new_cases = covid_data["data"][0]["newCasesByPublishDate"]
        total_cases = covid_data["data"][0]["cumCasesByPublishDate"]

        formatted_current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_title = Markup("COVID data at: <i>{}</i>".format(formatted_current_time))
        content = Markup("Daily cases: {}<br>Total cases: {}".format(new_cases, total_cases))
        notification = {"title": formatted_title, "content": content}

        global latest_covid_notification
        if notification["content"] != latest_covid_notification["content"]:
            notifications.append(notification)
            latest_covid_notification = notification
            logger.info("New COVID notification!") 

def remove_notification(notification: dict) -> None:
    """
    Utility function to remove a notification from the list of notifications.

    Keyword arguments:
    notification (dictionary) -- The notification to remove.

    No return argument.
    """

    logger.info("Removed notification: {}".format(notification["title"]))
    notifications.remove(notification)
    completed_notifications.append(notification)

# Alarms
def process_alarm(alarm: dict) -> None:
    """
    This function takes an alarm and processes its data to decide what announcement is given to the read_announcement function that will read
    the announcement using TTS.

    Keyword arguments:
    alarm (dictionary) -- The alarm to form the announcement for.

    No return argument.
    """

    alarm_id = alarm["title"]
    date = alarm["time"]
    news = alarm["news"]
    weather = alarm["weather"]

    announcement = ""
    try:
        if news:
            if fetch_news().status_code == 200:
                news_data = fetch_news().json()
                articles = news_data["articles"]
                for article in articles:
                    title = article["title"]
                    announcement += title
            else:
                logger.warning("Was unable to fetch news data: response returned status code {}!".format(fetch_news().status_code))            


        if weather:
            if fetch_weather().status_code == 200:
                weather = fetch_weather().json()
                weather_description = ""

                temperature = str(weather["main"]["temp"])
                if WEATHER_SERVICE["units"] == "metric":
                    temperature += " degrees celcius"
                elif WEATHER_SERVICE["units"] == "imperial":
                    temperature += " degrees faranheit"
                elif WEATHER_SERVICE["units"] == "standard":
                    temperature += " kelvin"

                for item in weather["weather"]:
                    # If first item
                    if weather_description == "":
                        weather_description += item["description"]
                    else:
                        weather_description += ", "
                        weather_description += item["description"]

                announcement += "The weather is currently {}. The temperature is currently {}. ".format(weather_description, temperature)
            else:
                logger.warning("Was unable to fetch weather data: response returned status code {}!".format(fetch_news().status_code))               

        covid_data = fetch_covid()
        new_cases = covid_data["data"][0]["newCasesByPublishDate"]
        total_cases = covid_data["data"][0]["cumCasesByPublishDate"]
        announcement += "There are {} new cases today, bringing the total number of cases to {}! ".format(new_cases, total_cases)

        alarm["announcement"] = announcement

        scheduler.add_job(func=read_announcement, args=[alarm], trigger="date", run_date=date, id=alarm_id)
    except Exception as e:
        # Handles the exception so that the error is logged but it will not error the page or add the alarm to the list of alarms when we know that the alarm won't run
        logger.warning("Was unable to process alarm. Stack trace: \n{}".format(e))
    else:
        # Only add the alarm to the list of alarms if we know that it will run (i.e. it's in the scheduler's queue)
        alarms.append(alarm)

def read_announcement(alarm: dict) -> None:
    """
    This function takes any argument and reads it aloud with text-to-speech. After it is done reading the announcement, it will remove the alarm.

    Keyword arguments:
    alarm (dictionary) -- The alarm to read out information from the 'information' attribute

    No return argument.
    """

    announcement = str(alarm["announcement"])
    engine = pyttsx3.init()
    engine.say(announcement)
    logger.info("Trying to read announcement: {}".format(announcement))
    try:
        engine.runAndWait()
    except RuntimeError as e:
        logger.warning("Unable to read announcement! Stack trace: \n{}".format(e))
    alarms.remove(alarm)

def remove_alarm(alarm: dict) -> None:
    """
    Utility function to remove an alarm from the list of alarms.

    Keyword arguments:
    alarm (dictionary) -- The alarm to remove.

    No return argument.
    """

    try:
        scheduler.remove_job(alarm["title"])
        logger.info("Attempting to remove alarm from job queue...")
    except JobLookupError as e:
        # Handle the exception if we cannot remove the alarm processing job from the scheduler
        logger.warning("Unable to remove alarm! Stack trace: \n{}".format(e))
    else:
        # Only remove if we know the alarm has been successfully removed from the scheduler
        logger.info("Removed alarm: {}".format(alarm["title"]))
        alarms.remove(alarm)

# If the user sends a GET request to the '/' or '/index' end points
@app.route("/")
@app.route("/index")
def index_page():
    """
    If the user sends a GET request to the '/' or '/index' end points this function will run. It will return a rendered HTML template.
    """

    # User is removing a notification
    if request.args.get("notif"):
        title = request.args.get("notif")
        logger.info("Attempting to remove notification: {}".format(title))
        for notification in notifications:
            if notification["title"] == title:
                remove_notification(notification)
                break

    # User is removing an alarm
    if request.args.get("alarm_item"):
        title = request.args.get("alarm_item")
        logger.info("Attempting to remove alarm: {}".format(title))
        for alarm in alarms:
            if alarm["title"] == title:
                remove_alarm(alarm)
                break

    # User is scheduling a new alarm
    if request.args.get("alarm"):
        time = request.args.get("alarm")
        time = dateutil.parser.parse(time)        

        can_run = True
        for alarm in alarms:
            if time.strftime("%Y-%m-%d %H:%M:%S") == alarm["time"]:
                can_run = False
                logger.error("Cannot schedule an alarm if an alarm since an alarm is already set for {}".format(alarm["time"]))
        if datetime.now() >= time:
            can_run = False
            logger.error("Cannot schedule an alarm for the past!")

        if can_run:
            title = Markup(request.args.get("two") + " <!-- {} -->".format(len(alarms)))
            time = time.strftime("%Y-%m-%d %H:%M:%S")

            news = False
            weather = False

            if request.args.get("news"):
                news = True

            if request.args.get("weather"):
                weather = True

            content = Markup("Time: {}<br>News: {}<br>Weather: {}".format(time, news, weather))

            alarm = {"title": title, "content": content, "time": time, "news": news, "weather": weather, "announcement": ""}
            process_alarm(alarm)

    return render_template("index.html", favicon = FAVICON, image = IMAGE, title = APP_NAME, notifications = notifications, alarms = alarms)

if __name__ == "__main__":
    # Create our scheduler that will run in a different thread
    scheduler = BackgroundScheduler()
    # Fetch for notifications every 60 minutes
    scheduler.add_job(func=fetch_for_notifications, args=(True, True, True), trigger="interval", seconds=REFRESH_RATE)
    # Make scheduler start completing jobs in its queue
    scheduler.start()

    # Run our Flask app
    app.run()

    print(os.getcwd())
