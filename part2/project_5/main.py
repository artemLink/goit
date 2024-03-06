import sys
import aiohttp
import asyncio
import platform
from datetime import datetime, timedelta


async def fetch_data(date, session):
    try:
        async with session.get(f'https://api.privatbank.ua/p24api/exchange_rates?json&date={date}') as response:
            json_data = await response.json()
            return date, json_data['exchangeRate']
    except Exception as e:
        print(f"Error fetching data for date {date}: {e}")
        return date, []


async def main(currencies):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_data(date, session) for date in dates_list]
        results = await asyncio.gather(*tasks)
        answer = []
        for date, currency in results:
            tmp = {
                date: {
                    currency['currency']: {
                        'sale': currency['saleRate'],
                        'purchase': currency['purchaseRate']
                    } for currency in currency if currency['currency'] in currencies
                }
            }
            answer.append(tmp)
        return answer


def generate_dates_list(days):
    today = datetime.now().date()
    dates_list = [today.strftime("%d.%m.%Y")]
    for i in range(1, min(days, 10)):
        previous_date = today - timedelta(days=i)
        dates_list.append(previous_date.strftime("%d.%m.%Y"))
    return dates_list


if __name__ == "__main__":
    if len(sys.argv) < 2 or not sys.argv[1].isdigit():
        print("Usage: python main.py <number_of_days> <currency1> <currency2> ...")
        sys.exit(1)

    days = int(sys.argv[1])
    currencies = sys.argv[2:]

    if days <= 10:
        dates_list = generate_dates_list(days)
        asyncio.run(main(currencies))
    else:
        print('Max days: 10')
