import datetime
from decimal import Decimal

DATE_FORMAT = '%Y-%m-%d'


def add(items, title, amount, expiration_date=None):
    if expiration_date is not None:
        expiration_date = datetime.datetime.strptime(
            expiration_date, DATE_FORMAT).date()
    if title in items:
        list.append(items[title], {'amount': amount,
                    'expiration_date': expiration_date})
    else:
        items[title] = [{'amount': amount, 'expiration_date': expiration_date}]


def add_by_note(items, note):
    note = str.split(note, ' ')
    if len(str.split(note[-1], '-')) == 3:
        expiration_date = str(note[-1])
        amount = Decimal(note[-2])
        title = str.join(' ', note[0: -2])
        add(items, str(title), amount, expiration_date)
    else:
        expiration_date = None
        amount = Decimal(note[-1])
        title = str.join(' ', note[0: -1])
        add(items, str(title), amount, expiration_date)


def find(items, needle):
    list_items = []
    for item, parameters in items.items():
        if needle.lower() in str.lower(str(item)):
            list_items.append(item)
    return list_items


def amount(items, needle):
    quantity = Decimal('0')
    for item, parameters in items.items():
        if needle.lower() in str.lower(item):
            for decitem in parameters:
                quantity += decitem['amount']
    return quantity


def expire(items, in_advance_days=0):
    list_items = []
    deadline = datetime.date.today() + datetime.timedelta(days=in_advance_days)
    for item, parameters in items.items():
        total_amount = Decimal('0')
        for parameter in parameters:
            data = parameter['expiration_date']
            amount = parameter['amount']
            if data is not None and data <= deadline:
                total_amount += amount
        if total_amount > 0:
            list_items.append(tuple([item, total_amount]))
    return list_items


goods = {
    'Пельмени Универсальные': [
        # Первая партия продукта 'Пельмени Универсальные':
        {'amount': Decimal(
            '0.5'), 'expiration_date': datetime.date(2023, 7, 15)},
        # Вторая партия продукта 'Пельмени Универсальные':
        {'amount': Decimal('2'), 'expiration_date': datetime.date(2023, 8, 1)},
    ],
    'Вода': [
        {'amount': Decimal('1.5'), 'expiration_date': None}
    ],
}

add(goods, 'пиво', Decimal('2'), '2024-9-15')
add_by_note(goods, 'пиво Жигулевское 4 2023-07-15')
print(find(goods, 'Пиво'))
print(expire(goods))
