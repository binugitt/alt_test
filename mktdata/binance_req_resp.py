import requests
from datetime import datetime
from collections import defaultdict
import copy

from symbol import Symbol
from exchange import Exchange
from md_interface import MDExchange



# BINU TODO: We need a mechanism to be able to manage different websockets!

class Binance(MDExchange):
    def __init__(self):

        # Build security mapping. Ideally we should be having
        # a SecurityManager class and all configs should be read from config
        self.securties = dict()
        self.securties[Symbol.BTCUSDT.value] = "BTCUSDT"
        self.securties[Symbol.ETHUSDT.value] = "ETHUSDT"
        self.securties[Symbol.SOLUSDT.value] = "SOLUSDT"

        # Using api as below.
        # https://api.binance.com/api/v3/depth?limit=10&symbol=BTCUSDT
        self.base_url = "https://api.binance.com/api/v1/"


    def get_security(self, sym: Symbol):
        if sym in self.securties:
            return self.securties[sym]

        raise "Security not found: %s" % sym 

    def get_data(self, sym: Symbol, typ: str, params):
        url = self.base_url + typ

        params['symbol'] = self.get_security(sym)
        #print(url)
        #print(params)

        data = requests.get(url, params=params).json()
        #print(data)

        return data

    #def format_order_book(
    def get_order_book(self, sym: Symbol, depth: int):
        params = {
                    "limit" : depth,
                 }
        binance_ob = self.get_data(sym, "depth", params)
        #print("binance_ob=%s" % type(binance_ob))
        #print("binance_ob = %s" % binance_ob)

        #normalised_ob = MDExchange.OrderBookData(
        normalised_ob = {}
        normalised_ob['timestamp']  = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
        normalised_ob['symbol']     = Symbol(sym).name
        normalised_ob['ecn']        = Exchange.BINANCE.name
        normalised_ob['ecn_symbol'] = self.get_security(sym)
        normalised_ob['bids']       = copy.deepcopy(binance_ob['bids'])
        normalised_ob['asks']       = copy.deepcopy(binance_ob['asks'])
        #print("normalised_ob = %s" % normalised_ob)

        return normalised_ob

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
