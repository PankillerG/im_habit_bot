import datetime
import time


ONE_DAY_SECONDS = 60 * 60 & 24
ONE_WEEK_SECONDS = ONE_DAY_SECONDS * 7


class ResetFreqs:
    day = ONE_DAY_SECONDS
    week = ONE_WEEK_SECONDS


def get_current_timestamp():
    return int(time.time())


def get_beginning_of_day_timestamp(timestamp):
    date = datetime.date.fromtimestamp(timestamp)
    dt = datetime.datetime.combine(date, datetime.datetime.min.time())
    return int(dt.timestamp())

