import datetime
import os

import pandas as pd

from config.constants import DATA_DIR
from utils.exceptions import DataNotPresentError

OPTION_DATA_DIR = os.path.join(DATA_DIR, 'weekly_option_data')

EXPIRY_DAYS = [
    datetime.datetime.strptime(_str, "%Y-%m-%d") for _str in
    [
        '2019-11-07',
        '2019-11-14',
        '2019-11-21',
        '2019-11-28',
    ]
]


def get_expiry_day(date_obj):
    """
    :param date_obj: datetime object
    :return: expiry day from the EXPIRY_DAYS
    """
    for i in EXPIRY_DAYS:
        if date_obj <= i:
            return i


def get_file_path(expiry_date_obj, strike_price, option_type):
    possible_file_names = [
        "NIFTYWK{strike_price}{option_type}.csv".format(
            strike_price=strike_price, option_type=option_type),
        "NIFTY{strike_price}{option_type}.csv".format(
            strike_price=strike_price, option_type=option_type),
    ]
    dir = os.path.join(OPTION_DATA_DIR, expiry_date_obj.strftime("%Y-%m-%d"))
    for root, subFolders, files in os.walk(dir):
        for tile_name in files:
            if tile_name in possible_file_names:
                return os.path.join(root, tile_name)


def main(strike_price, option_type, date_str, open_time="09:30", close_time="15:15"):
    """
    :param strike_price: strike_price, eg: 11400
    :param option_type: CE/PE
    :param date_str: %Y/%m/%d format
    :param open_time: time to consider as market open
    :param close_time: time to consider as close time
    :return: open, high, low, close, day_of_the_week, days_for_expiry of the option
    """
    date_obj = datetime.datetime.strptime(date_str, "%Y/%m/%d")
    day_of_the_week = date_obj.strftime('%A')
    strike_price = int(strike_price)
    expiry_date_obj = get_expiry_day(date_obj)
    if not expiry_date_obj:
        raise DataNotPresentError("Expiry date doesn't exist")
    days_for_expiry = (expiry_date_obj - date_obj).days
    file_path = get_file_path(expiry_date_obj, strike_price, option_type)
    if not file_path:
        raise DataNotPresentError("file_path doesn't exist")
    header = ['name', 'date', 'time', 'open', 'high', 'low', 'close', 'volume']
    df = pd.read_csv(file_path, header=None, names=header)
    df = df[df['date'] == date_str]
    sub_df = df[(df['time'] >= open_time) & (df['time'] <= close_time)].sort_values(
        by=['date', 'time'])
    if sub_df.empty:
        raise DataNotPresentError("Empty data")
    open_data = sub_df.iloc[0, :].to_dict()
    close_data = sub_df.iloc[-1, :].to_dict()
    open = open_data['open']
    close = close_data['close']
    high = sub_df.high.max()
    low = sub_df.low.min()
    response = {
        'open': open,
        'high': high,
        'low': low,
        'close': close,
        'day_of_the_week': day_of_the_week,
        'days_for_expiry': days_for_expiry,
    }
    return response
