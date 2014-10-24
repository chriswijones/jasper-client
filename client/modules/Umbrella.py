# -*- coding: utf-8-*-
#from app_utils import getTimezone
#from semantic.dates import DateService
import forecastio
import time
import datetime

WORDS = ["WEATHER", "TODAY", "TOMORROW"]


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

    if umbrella_needed:
        output += u' You should bring an umbrella today.'
    else:
        output += u' You do not need an umbrella today.'

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
    if type(text) is dict:
        return any(d.get(u'intent', u'') == u'need_umbrella' for d in text.get(u'outcomes', []))
    else:
        return False
