import os

import requests
from bs4 import BeautifulSoup

from config.constants import HISTORICAL_INDICES_URL, DATA_DIR
from utils.main import parse, csv_dict_writer


def get_index_data(from_date, to_date, index_type="NIFTY 50"):
    params = {
        'indexType': index_type,
        'fromDate': from_date,
        'toDate': to_date,
    }
    url = HISTORICAL_INDICES_URL
    r = requests.get(url, params=params)
    rows = []
    r.raise_for_status()
    soup = BeautifulSoup(r.text, features="html.parser")
    table = soup.table
    if not table:
        return rows
    table = table.find_all('tr')
    header = [parse(x) for x in table[2].find_all('th')]
    for i in range(3, len(table) - 1):
        row = {header[j]: parse(cell) for j, cell in enumerate(table[i].find_all('td'))}
        row['indexType'] = index_type
        yield row


def main(from_date='01-02-2019', to_date='11-07-2019', file_name='nifty_50_data.csv'):
    field_names = ['indexType', 'Date', 'Open', 'High', 'Low', 'Close', 'Shares Traded',
                   'Turnover (  Cr)']
    file_path = os.path.join(DATA_DIR, file_name)
    csv_dict_writer(get_index_data(from_date, to_date), file_path, field_names)


if __name__ == '__main__':
    main()
