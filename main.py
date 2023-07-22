import argparse
import asyncio
import aiohttp

class ExchangeRateAPI:
    BASE_URL = "https://api.privatbank.ua/p24api/pubinfo"

    async def get_exchange_rate(self, currency, date):
        async with aiohttp.ClientSession() as session:
            url = f"{self.BASE_URL}?exchange&json&coursid=11&date={date}"
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    for rate in data:
                        if rate['ccy'] == currency:
                            return {
                                'sale': float(rate['sale']),
                                'purchase': float(rate['buy'])
                            }
                return None

class CurrencyRateFetcher:
    def __init__(self):
        self.api = ExchangeRateAPI()

    async def fetch_rates(self, currency, days):
        today = datetime.date.today()
        rates = []
        for i in range(days):
            date = today - datetime.timedelta(days=i)
            formatted_date = date.strftime("%d.%m.%Y")
            rate_eur = await self.api.get_exchange_rate("EUR", formatted_date)
            rate_usd = await self.api.get_exchange_rate("USD", formatted_date)
            if rate_eur and rate_usd:
                data = {
                    formatted_date: {
                        'EUR': rate_eur,
                        'USD': rate_usd
                    }
                }
                rates.append(data)
        return rates

async def main(days):
    fetcher = CurrencyRateFetcher()
    rates = await fetcher.fetch_rates("EUR", days)
    print(rates)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch currency rates from PrivatBank API.")
    parser.add_argument("days", type=int, help="Number of days to fetch currency rates.")
    args = parser.parse_args()

    if args.days > 10:
        print("Error: You can fetch rates for up to 10 days only.")
    else:
        import datetime
        asyncio.run(main(args.days))




