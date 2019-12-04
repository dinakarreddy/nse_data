import logging.config

from config.log_config import LOG_CONFIG

logging.config.dictConfig(LOG_CONFIG)

import sys
from nifty_50.fetch_data.nifty_50 import main as store_nifty_50_data
from nifty_50.weekly_options.store_option_trades import main as store_nifty_50_option_trades
import datetime
from pytz import timezone
import argparse

LOGGER = logging.getLogger(__name__)
DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'


def valid_date(argument):
    try:
        return datetime.datetime.strptime(argument, DATE_FORMAT).replace(tzinfo=timezone('UTC'))
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(argument)
        raise argparse.ArgumentTypeError(msg)


def store_nifty_50_data_parser(arguments):
    parser = argparse.ArgumentParser()
    parser.add_argument('--start_datetime',
                        dest='start_datetime',
                        type=valid_date,
                        help='date in {format} in UTC'.format(format=DATE_FORMAT),
                        default=datetime.datetime.utcnow().replace(
                            tzinfo=timezone('UTC')) - datetime.timedelta(
                            days=30),
                        )
    parser.add_argument('--end_datetime',
                        dest='end_datetime',
                        type=valid_date,
                        help='date in {format} in UTC'.format(format=DATE_FORMAT),
                        default=datetime.datetime.utcnow().replace(tzinfo=timezone('UTC')),
                        )
    parser.add_argument('--file_name',
                        dest='file_name',
                        default='nifty_50_data.csv',
                        )
    return parser.parse_args(arguments)


def store_nifty_50_option_trades_parser(arguments):
    parser = argparse.ArgumentParser()
    parser.add_argument('--option_trade_file_name',
                        dest='option_trade_file_name',
                        default='nifty_50_option_trades.csv',
                        )
    parser.add_argument('--nifty_50_data_file_name',
                        dest='nifty_50_data_file_name',
                        default='nifty_50_data.csv',
                        )
    parser.add_argument('--up_percent',
                        dest='up_percent',
                        type=int,
                        default=1.67,
                        )
    parser.add_argument('--down_percent',
                        dest='down_percent',
                        type=float,
                        default=1.67,
                        )
    parser.add_argument('--open_time',
                        dest='open_time',
                        default='09:30',
                        )
    parser.add_argument('--close_time',
                        dest='close_time',
                        default='15:15',
                        )
    parser.add_argument('--stop_loss_percent',
                        dest='stop_loss_percent',
                        type=float,
                        default=100,
                        )
    return parser.parse_args(arguments)


def main():
    arguments = sys.argv
    for i, arg in enumerate(arguments):
        if arg == 'store_nifty_50_data':
            parsed = store_nifty_50_data_parser(arguments[i + 1:])
            store_nifty_50_data(
                from_date=parsed.start_datetime.strftime('%d-%m-%Y'),
                to_date=parsed.end_datetime.strftime('%d-%m-%Y'),
                file_name=parsed.file_name,
            )
            break
        if arg == 'store_nifty_50_option_trades':
            parsed = store_nifty_50_option_trades_parser(arguments[i + 1:])
            store_nifty_50_option_trades(
                option_trade_file_name=parsed.option_trade_file_name,
                nifty_50_data_file_name=parsed.nifty_50_data_file_name,
                up_percent=parsed.up_percent,
                down_percent=parsed.down_percent,
                open_time=parsed.open_time,
                close_time=parsed.close_time,
                stop_loss_percent=parsed.stop_loss_percent,
            )


if __name__ == '__main__':
    main()
