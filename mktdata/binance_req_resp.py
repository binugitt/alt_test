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
        print(url)
        print(params)

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
        start_time: int,
        end_time: int
        #start_time: datetime,
        #end_time: datetime
        ):
        params = {
                    "interval" : "1h",
                    "startTime" : int(round(start_time)),
                    "endTime" : int(round(end_time))
                    #"startTime" : int(round(start_time.timestamp()))*1000,
                    #"endTime" : int(round(end_time.timestamp()))*1000
                 }
        binance_hist_cdls = self.get_data(symbol, "klines", params)
        print(binance_hist_cdls)

        normalised_hist_cdls = []
        for cdl in binance_hist_cdls:
            print("cdl=%s" % type(cdl))
            print(cdl)

            '''
            Response format from Binance : https://binance-docs.github.io/apidocs/spot/en/#kline-candlestick-data
            [
              [
                1499040000000,      // Open time
                "0.01634790",       // Open
                "0.80000000",       // High
                "0.01575800",       // Low
                "0.01577100",       // Close
                "148976.11427815",  // Volume
                1499644799999,      // Close time
                "2434.19055334",    // Quote asset volume
                308,                // Number of trades
                "1756.87402397",    // Taker buy base asset volume
                "28.46694368",      // Taker buy quote asset volume
                "17928899.62484339" // Ignore.
              ]
            ]
            '''

            candle = {}
            candle["time"]      = int(cdl[0])
            candle["open"]      = float(cdl[1])
            candle["high"]      = float(cdl[2])
            candle["low"]       = float(cdl[3])
            candle["close"]     = float(cdl[4])
            candle["volume"]    = float(cdl[5])
            normalised_hist_cdls.append(candle)

        return normalised_hist_cdls
