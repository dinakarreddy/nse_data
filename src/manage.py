import logging.config

from config.log_config import LOG_CONFIG

logging.config.dictConfig(LOG_CONFIG)

import sys
from nifty_50.fetch_data.nifty_50 import main as store_nifty_50_data
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
    parser = argparse.ArgumentParser(description='Run data_check')
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


def main():
    arguments = sys.argv
    for i, arg in enumerate(arguments):
        if arg == 'store_nifty_50_data':
            parsed = store_nifty_50_data_parser(arguments[i + 1:])
            store_nifty_50_data(
                parsed.start_datetime.strftime('%d-%m-%Y'),
                parsed.end_datetime.strftime('%d-%m-%Y'),
                parsed.file_name
            )
            break


if __name__ == '__main__':
    main()
