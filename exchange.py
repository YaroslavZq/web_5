import asyncio
import httpx
from datetime import datetime, timedelta
import sys

url = 'https://api.privatbank.ua/p24api/exchange_rates'
# API_KEY = "563492ad6f91700001000001ad14c80fca434af7b27534a05d90262b"
# SEARCH_WORD = 'audi a4'


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
                    # result.update(f'')
                    result.update({item['currency']:
                                    {'sale': item['saleRateNB'],
                                     'purchase': item['purchaseRateNB']}})
        else:
            print(f'{response.status_code=}, {response.json()=}')
    return {day: result}


def pretty_view(data: list):
    for day in data:
        print(day.strftime)
        pattern = '|{:^10}|{:^10}|{:^10}|'
        print(pattern.format('currency', 'sale', 'purchase'))
        for el in data:
            currency, *_ = el.keys()
            buy = el.get(currency).get('buy')
            sale = el.get(currency).get('purchase')
            print(pattern.format(currency, sale, buy))


async def main():
    # tasks = []
    # days = int(sys.argv[1])
    # print(days, type(days))

    days = arg_to_int()
    currency_list = ['USD', 'EUR']
    tasks = []
    for count in range(days):
        day = datetime.today() - timedelta(days=count)
        # print(day)
        task = asyncio.create_task(download(day.strftime("%d.%m.%Y"), currency_list))
        tasks.append(task)
    results = await asyncio.gather(*tasks, return_exceptions=True)
    print(results)


def arg_to_int() -> int:
    if len(sys.argv) == 1:
        return 1
    if len(sys.argv) == 2:
        count_days = int(sys.argv[-1])
        if 0 < count_days <= 10:
            return count_days
        raise ValueError('You can see only 10 last days')
    # if len(sys.argv) == 3:
    #     new_currency = sys.argv[-1]
    #     actual_currency.append(new_currency.upper())
    #     count_days = int(sys.argv[-2])
    #     if 0 < count_days <= 10:
    #         return count_days
    #     raise ValueError('You can see only 10 last days')
    # raise ValueError('Invalid args')


if __name__ == '__main__':
    asyncio.run(main())
