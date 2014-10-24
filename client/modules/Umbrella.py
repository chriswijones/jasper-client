# -*- coding: utf-8-*-
import datetime
#from app_utils import getTimezone
#from semantic.dates import DateService
import forecastio
import json

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

    forecast = forecastio.load_forecast(api_key, lat, lng, now)

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


def isValid(text):
    """
        Returns True if the text is related to the weather.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    text_obj = json.loads(text)
    return any(d[u'intent'] == u'need_umbrella' for d in text_obj[u'outcomes'])
