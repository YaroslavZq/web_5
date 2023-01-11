import asyncio
import platform
import httpx
from datetime import datetime, timedelta
import sys

url = 'https://api.privatbank.ua/p24api/exchange_rates'
currency_list = ['USD', 'EUR']


async def download(day: str, currency: list):
    result = {}
    params = {
        "date": day,
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            for item in data['exchangeRate']:
                if item['currency'] in currency:
                    result.update({item['currency']:
                                    {'sale': item['saleRateNB'],
                                     'purchase': item['purchaseRateNB']}})
        else:
            print(f'{response.status_code=}, {response.json()=}')
    return {day: result}


def pretty_view(data: list):
    for day in data:
        print(*day.keys())
        pattern = '|{:^10}|{:^10}|{:^10}|'
        print(pattern.format('currency', 'sale', 'purchase'))
        for el in day.values():
            for currency, values in el.items():
                sale = "{:.2f}".format(el.get(currency).get('sale'))
                purchase = "{:.2f}".format(el.get(currency).get('purchase'))
                print(pattern.format(currency, sale, purchase))


async def exchange(days=1):
    # days = arg_to_int()
    tasks = []
    for count in range(days):
        day = datetime.today() - timedelta(days=count)
        task = asyncio.create_task(download(day.strftime("%d.%m.%Y"), currency_list))
        tasks.append(task)
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results


def arg_to_int() -> int:
    if len(sys.argv) == 1:
        return 1
    if len(sys.argv) == 2:
        count_days = int(sys.argv[-1])
        if 0 < count_days <= 10:
            return count_days
        raise ValueError('You can see only 10 last days')
    if len(sys.argv) == 3:
        new_currency = sys.argv[-1]
        currency_list.append(new_currency.upper())
        count_days = int(sys.argv[-2])
        if 0 < count_days <= 10:
            return count_days
        raise ValueError('You can see only 10 last days')
    raise ValueError('Invalid args')


if __name__ == '__main__':
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    show_exchange = asyncio.run(exchange())
    print(show_exchange)
