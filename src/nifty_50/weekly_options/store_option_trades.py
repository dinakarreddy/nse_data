import pandas as pd
from config.constants import DATA_DIR
import os
import datetime
from nifty_50.weekly_options.data_parser import main as option_data_parser
from utils.exceptions import DataNotPresentError
import logging
LOGGER = logging.getLogger(__name__)


def get_call_strike(price, step):
    div = int(price / step)
    strike = div * step
    # if strike < price:
    #     strike += step
    return strike


def get_put_strike(price, step):
    div = int(price / step)
    strike = div * step
    return strike


def get_call_and_put_strike(price, step=50, up_percent=1.67, down_percent=1.67):
    price = float(price)
    up_price = price * (1 + (float(up_percent) / 100))
    down_price = price * (1 - (float(down_percent) / 100))
    call_strike = get_call_strike(up_price, step)
    put_strike = get_put_strike(down_price, step)
    return int(call_strike), int(put_strike)


def main(option_trade_file_name='nifty_50_option_trades.csv',
         nifty_50_data_file_name='nifty_50_data.csv',
         up_percent=2, down_percent=2,
         open_time="09:30", close_time="15:15"):
    file_path = os.path.join(DATA_DIR, nifty_50_data_file_name)
    rows = pd.read_csv(file_path).to_dict('records')
    final_data = []
    for row in rows:
        date_obj = datetime.datetime.strptime(row['Date'], '%Y-%m-%d %H:%M:%S')
        nifty_price = row['Open']
        call_strike, put_strike = get_call_and_put_strike(
            nifty_price, up_percent=up_percent, down_percent=down_percent)
        date_str = date_obj.strftime("%Y/%m/%d")
        try:
            call_response = option_data_parser(
                call_strike, 'CE', date_str, open_time=open_time, close_time=close_time)
            put_response = option_data_parser(
                put_strike, 'PE', date_str, open_time=open_time, close_time=close_time)
        except DataNotPresentError as e:
            LOGGER.warning("Data not present error, {e}".format(e=e))
            continue
        response = {
            'date_str': date_str,
            'nifty_open': row['Open'],
            'nifty_high': row['High'],
            'nifty_low': row['Low'],
            'nifty_close': row['Close'],
            'call_strike': call_strike,
            'call_open': call_response['open'],
            'call_high': call_response['high'],
            'call_low': call_response['low'],
            'call_close': call_response['close'],
            'put_strike': put_strike,
            'put_open': put_response['open'],
            'put_high': put_response['high'],
            'put_low': put_response['low'],
            'put_close': put_response['close'],
            'day_of_the_week': put_response['day_of_the_week'],
            'days_for_expiry': put_response['days_for_expiry'],
            'up_percent': up_percent,
            'down_percent': down_percent,
            'open_time': open_time,
            'close_time': close_time,
        }
        final_data.append(response)
    final_df = pd.DataFrame(final_data)
    final_df.to_csv(os.path.join(DATA_DIR, option_trade_file_name), index=False)
