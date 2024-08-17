import datetime
import time


def get_current_timestamp():
    return int(time.time())


def is_equal(timestamp1, timestamp2, datetime_type):
    date1 = datetime.date.fromtimestamp(timestamp1)
    date2 = datetime.date.fromtimestamp(timestamp2)

    if datetime_type == 'day':
        return date1.day == date2.day

    elif datetime_type == 'week':
        return date1.isocalendar().week == date2.isocalendar().week

    elif datetime_type == 'month':
        return date1.month == date2.month

    return False
