import csv
from datetime import datetime


def csv_dict_writer(iterable, file, field_names, delimiter=',', quoting=csv.QUOTE_ALL):
    with open(file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, field_names, delimiter=delimiter, quoting=quoting)
        writer.writeheader()
        for _iter in iterable:
            writer.writerow(_iter)


def csv_dict_reader(file, delimiter=','):
    with open(file, 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=delimiter)
        for row in reader:
            yield row


def parse(cell):
    value = cell.text.strip()
    classes = cell.get('class') or []
    if 'number' in classes:
        value = value.replace(',', '')
        return None if value == '-' else float(value)
    elif 'date' in classes:
        return datetime.strptime(value, '%d-%b-%Y')
    else:
        return value


def get_call_strike(price, step):
    div = int(price / step)
    strike = div * step
    if strike < price:
        strike += step
    return strike


def get_put_strike(price, step):
    div = int(price / step)
    strike = div * step
    if strike > price:
        strike -= step
    return strike


def get_call_and_put_strike(price, step=50, up_percent=2, down_percent=2):
    price = float(price)
    up_price = price * (1 + (float(up_percent) / 100))
    down_price = price * (1 - (float(down_percent) / 100))
    call_strike = get_call_strike(up_price, step)
    put_strike = get_put_strike(down_price, step)
    return int(call_strike), int(put_strike)
