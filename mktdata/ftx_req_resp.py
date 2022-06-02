import requests
from datetime import datetime
from collections import defaultdict

from symbol import Symbol
from md_interface import MDExchange



# BINU TODO: We need a mechanism to be able to manage different websockets!

class FTX(MDExchange):
    def __init__(self):

        # Build security mapping. Ideally we should be having
        # a SecurityManager class and all configs should be read from config
        self.securties = dict()
        self.securties[Symbol.BTCUSDT.value] = "BTC/USD"
        self.securties[Symbol.ETHUSDT.value] = "ETH/USD"
        self.securties[Symbol.SOLUSDT.value] = "SOL/USD"

        # Using api as below.
        #https://ftx.us/api/markets/BTC/USD/orderbook?depth=20
        self.base_url = "https://ftx.us/api/markets/"


    def get_security(self, sym: Symbol):
        if sym in self.securties:
            return self.securties[sym]

        raise "Security not found: %s" % sym 

    def get_data(self, sym: Symbol, typ: str, params):
        url = self.base_url + self.get_security(sym) + "/" + typ

        print(url)
        print(params)

        data = requests.get(url, params=params).json()
        print(data)

        return data

    def get_order_book(self, sym: Symbol, depth: int):
        params = {
                    "depth" : depth,
                 }
        return self.get_data(sym, "orderbook", params)

    def get_historical_candles(
        self,
        symbol: Symbol,
        start_time: datetime,
        end_time: datetime
        ):
        params = {
                    "interval" : "1h",
                    "startTime" : int(round(start_time.timestamp()))*1000,
                    "endTime" : int(round(end_time.timestamp()))*1000
                 }
        return self.get_data(symbol, "klines", params)
