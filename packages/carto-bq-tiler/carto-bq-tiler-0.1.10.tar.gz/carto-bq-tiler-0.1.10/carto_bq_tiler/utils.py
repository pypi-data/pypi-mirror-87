from datetime import datetime


def datetime_to_timestamp(dt):
    return '{dt}Z'.format(dt=dt.isoformat().split('.')[0].split('+')[0])


def get_current_timestamp():
    return datetime_to_timestamp(datetime.utcnow())
