# -*- coding: utf-8-*-
#from app_utils import getTimezone
from semantic.dates import DateService
import forecastio
import time
import datetime
import logging

WORDS = ["WEATHER", "TODAY", "TOMORROW"]

logger = logging.getLogger(__name__)

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

    mic.say("Let me check the forecast.")

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

    logger.debug("Getting forecast for {lat}, {lng}".format(lat=lat, lng=lng))

    forecast = get_forecast(api_key, lat, lng)

    entities = text[u'outcomes'][0].get(u'entities', {})

    windows = get_time_windows(entities, profile)

    for window in windows:
        logger.debug("Window found from {} to {}".format(window[0], window[1]))

    umbrella_needed, summary = need_umbrella(windows, forecast)

    output = summary

    #Easter Egg!!!!
    if entities.get(u'location') == u'seattle':
        output += " But you won't bring one."

    mic.say(output)

def need_umbrella(windows, forecast):

    #first what sort of aggregation are we looking for
    two_days_delta = datetime.timedelta(days=2)
    ret = False
    summary = ''
    #both start and end are within 2 days
    for start, end in windows:
        forecasts = []
        if end < datetime.datetime.now() + two_days_delta:
            forecasts = forecast.hourly()
            start = start - datetime.timedelta(hours=1) #make sure we get the segment we are looking for
        else:
            forecasts = forecast.daily()
            start = start - datetime.timedelta(days=1)

        #p_norain = 1
        for f in forecasts.data:
            if f.time > start and f.time < end:
                precipProbability = f.d.get(u'precipProbability', 0)
                #if f.d.get(u'precipType',u'') == u'rain':
                #    p_norain = p_norain * (1 - precipProbability)
                intensity = f.d.get(u'precipIntensityMax', f.d.get(u'precipIntensity', 0))
                precipType = f.d.get(u'precipType')
                #if precipType == u'rain' and precipProbability >= .5 and Intensity >= .017:
                logger.debug("icon: {icon}, precipType: {precipType}, precipProbability: {precipProbability}, intensity: {intensity{".format(icon=f.d.icon,precipType=precipType,precipProbability=precipProbability,intensity=intensity))
                if f.d.icon == u'rain':
                    logger.debug("Rain found.")
                    ret = True
                    summary = f.d.get(u'summary', '') #we need our umbrella short circuit rest
                    break
        if ret:
            break

    if ret:
        summary = u' You should bring an umbrella.'
    else:
        summary = u' You do not need an umbrella.'

    return ret, summary



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

    forecast = forecastio.load_forecast(api_key, lat, lng)
    forecast_cache[forecast_key] = {'cache_date': time.time(), 'forecast': forecast}
    return forecast


def get_time_windows(entities, profile):
    ds = DateService()
    windows = []
    if u'datetime' in entities:
        parsed_dates = entities.get(u'datetime')
        for date in parsed_dates:
            if date[u'type'] == u'value':
                start_time = ds.extractDate(date[u'value'])
                delta = date[u'grain'] + u's' #wit returns singular names of intervals
                end_time = start_time + datetime.timedelta(**{delta: 1})
            elif date[u'type'] == u'interval':
                start_time = ds.extractDate(date[u'from'][u'value'])
                end_time = ds.extractDate(date[u'to'][u'value'])
            windows.append((start_time, end_time))
    #Need to support looking up commute windows from the profile
    else:
        start_time = datetime.datetime.combine(datetime.datetime.now(), datetime.time())
        end_time = start_time + datetime.timedelta(days=1)
        windows.append((start_time, end_time))
    return windows


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
#
# if __name__ == "__main__":
#     while True:
#         forecast = get_forecast('50c059b8e33da61e8273c9dca95f2177',47.597843,-122.328392)
#         start = datetime.datetime.now()
#         end = datetime.datetime.now()
#         end = end  + datetime.timedelta(hours=2)
#
#         start = datetime.datetime(2014,10,26)
#         end = datetime.datetime(2014,10,28)
#
#         windows = [(start, end)]
#
#         umbrella_needed, summary = aggregate_forecast(windows, forecast)