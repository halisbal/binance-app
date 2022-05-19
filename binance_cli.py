from binance.spot import Spot
import json

with open('/Users/halis/PycharmProjects/binance-app/helpers/config.json', 'r') as f:
    config = json.load(f)


class Binance(object):
    def __init__(self):
        self.client = Spot(key=config.get('BINANCE_API_KEY'), secret=config.get('BINANCE_SECRET_KEY'))

    def get_user_data(self):
        return self.client.account()

    def coin_specific_data(self,coin_name):
        list = self.get_user_data().get('balances')
        return next(item for item in list if item["asset"] == coin_name.upper())

    def order(self, coin, side, type, quantity, timeInForce=None, price=None):
        params = {
            'symbol': coin+"USDT",
            'side': side,
            'type': type,
            'timeInForce': timeInForce,
            'quantity': quantity,
            'price': price
        }
        response = self.client.new_order(**params)

    def limit_buying_order(self, coin, quantity, price):
        self.order(coin, "BUY", "LIMIT", quantity, "GTC", price)

    def limit_selling_order(self, coin, quantity, price):
        self.order(coin, "SELL", "LIMIT", quantity, "GTC", price)

    def market_buying_order(self, coin, quantity):
        self.order(coin, "BUY", "MARKET", quantity)

    def market_selling_order(self, coin, quantity):
        self.order(coin, "SELL", "MARKET", quantity)

    def sell_all_market_order(self,coin):
        self.market_selling_order(coin, self.coin_specific_data(coin).get('free'))

    def coin_price(self,name):
        return self.client.ticker_price(name)


binance = Binance()