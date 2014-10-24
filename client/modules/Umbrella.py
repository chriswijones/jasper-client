# -*- coding: utf-8-*-
#import datetime
#from app_utils import getTimezone
#from semantic.dates import DateService
import forecastio

WORDS = ["WEATHER", "TODAY", "TOMORROW"]

#hardcoded latitude and longitude for Vulcan



def handle(text, mic, profile):
    """
    Responds to user-input, typically speech text, with a summary of
    the relevant weather for the requested date (typically, weather
    information will not be available for days beyond tomorrow).

    Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
    """

    if not profile['location']:
        mic.say(
            "I don't know where you are.")
        return

    if not profile['keys']['forecastio']:
        mic.say(
            "I do not have a forecast api key."
        )

    api_key = profile['keys']['forecastio']
    lat = profile['location']['latitude']
    lng = profile['location']['longitude']

    forecast = forecastio.load_forecast(api_key, lat, lng)

    hourly = forecast.hourly()
    output = hourly.summary

    mic.say(output)


def isValid(text):
    """
        Returns True if the text is related to the weather.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return any(d[u'intent'] == u'need_umbrella' for d in text[u'outcomes'])
