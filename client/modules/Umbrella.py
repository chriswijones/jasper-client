# -*- coding: utf-8-*-
#import datetime
#from app_utils import getTimezone
#from semantic.dates import DateService
import forecastio
import time
import datetime
import json

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

    text_obj = json.loads(text)

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
    now = datetime.datetime.now() #this should be determined dynamically

    forecast = get_forecast(api_key, lat, lng)

    hourly = forecast.hourly()

    umbrella_needed = False
    for datum in hourly.data:
        timewindow = datum.time().time()
        #we should be subsetting this down based on time based config
        precipProbability = datum.d[u'precipProbability']
        precipIntensity = datum.d[u'precipIntensity']
        precipType = datum.d.get(u'precipType')
        if precipType == u'rain' and precipProbability >= .5 and precipIntensity >= .01:
            umbrella_needed = True

    output = hourly.summary

    mic.say(output)

forecast_cache = {}
def get_forecast(api_key, lat, lng):

    FORECAST_CACHE_EXPIRES_SECONDS = 15 * 60 #fifteen mintues

    forecast_key = (lat, lng)
    if forecast_key in forecast_cache:
        forecast = forecast_cache[forecast_key]
        if forecast['cache_date'] + FORECAST_CACHE_EXPIRES_SECONDS < time.time():
            forecast_cache.pop(forecast_key)
        else:
            return forecast['forecast']

    forecast = forecastio.load_forecast(api_key, lat, lng, datetime.datetime.now())
    forecast_cache[forecast_key] = {'cache_date': time.time(), 'forecast': forecast}
    return forecast


def isValid(text):
    """
        Returns True if the text is related to the weather.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    try:
        text_obj = json.loads(text)
        return any(d[u'intent'] == u'need_umbrella' for d in text_obj[u'outcomes'])
    except:
        return False
