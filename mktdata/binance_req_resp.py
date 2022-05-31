import requests
from symbol import Symbol
from datetime import datetime
from collections import defaultdict


class MDExchange:
    
    def get_hist_candles(
        self,
        symbol: Symbol,
        start_time: datetime,
        end_time: datetime
        ):
        raise Exception("Not Implemented")

    def get_order_book(self, symbol: Symbol):
        """
        Returns 20 best bids and 20 best asks
        """
        raise Exception("Not Implemented")


# BINU TODO: We need a mechanism to be able to manage different websockets!

class Binance(MDExchange):
    def __init__(self):

        # Build security mapping. Ideally we should be having
        # a SecurityManager class and all configs should be read from config
        self._securties = dict()
        self._securties[Symbol.BTCUSDT.value] = "BTCUSDT"
        self.base_url = "https://api.binance.com/api/v1/"


    def get_security(self, sym: Symbol):
        if sym in self._securties:
            return self._securties[sym]

        raise "Security not found: %s" % sym 

    def get_data(self, sym: Symbol, typ: str, params):
        url = self.base_url + typ

        print(url)
        params['symbol'] = self.get_security(sym)
        print(params)
        data = requests.get(url, params=params).json()
        #print(data)
        return data

    def get_order_book(self, sym: Symbol):
        return self.get_data(sym, "trades", {})

    def get_hist_candles(
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
