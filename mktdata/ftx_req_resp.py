import requests
from datetime import datetime
from collections import defaultdict
import copy

from symbol import Symbol
from exchange import Exchange
from md_interface import MDExchange
import os
import ast
import json



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

        # For some reason requests does not work and hence using curl
        #data = requests.get(url, params=params).json()
        if len(params) > 0:
            url = url + '?'
            cnt = 0
            for (key, val) in params.items():
                if cnt > 0:
                    url = url + '&'
                url = url + str(key)
                url = url + '='
                url = url + str(val)
                cnt = cnt + 1
        cmd = "curl " + url
        print(cmd)
        data_str = os.popen(cmd).read()
        #print(data_str)

        length = 12
        success = data_str[length-1]
        #print(success)

        # The response for FTX is broken: "success":true. Here true is not a string/int
        # So need to remove this part from the string prior to converting to dict
        # Example = '{"success":true,"result":[{"startTime":"2020-03-23T00:00:00+00:00","time":1584921600000.0,"open":6350.0,"high":6873.0,"low":6030.25,"close":6253.75,"volume":0.0}]}'
        if success == 't':
            print("TRUE")
            length = length + 5
        else:
            length = length + 6

        data_str = '{"success":"' + success + '",' + data_str[length-1:]
        #print(data_str)

        data = ast.literal_eval(data_str)
        #print(type(data))
        #print(data)


        return data

    def get_order_book(self, sym: Symbol, depth: int):
        params = {
                    "depth" : depth,
                 }

        normalised_ob = {}
        ftx_ob = self.get_data(sym, "orderbook", params)

        if ftx_ob["success"] != "t":
            return normalised_hist_cdls

        ftx_ob = ftx_ob["result"]

        '''
        Response format from FTX : https://docs.ftx.com/#get-orderbook
        https://ftx.us/api/markets/BTC/USD/orderbook?depth=20
        {
          "success": true,
          "result": {
            "asks": [
              [
                4114.25,
                6.263
              ]
            ],
            "bids": [
              [
                4112.25,
                49.29
              ]
            ]
          }
        }
        '''

        normalised_ob['timestamp']  = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
        normalised_ob['symbol']     = Symbol(sym).name
        normalised_ob['ecn']        = Exchange.FTX.name
        normalised_ob['ecn_symbol'] = self.get_security(sym)
        normalised_ob['bids']       = copy.deepcopy(ftx_ob['bids'])
        normalised_ob['asks']       = copy.deepcopy(ftx_ob['asks'])
        #print("normalised_ob = %s" % normalised_ob)

        return normalised_ob

    def get_historical_candles(
        self,
        symbol: Symbol,
        start_time: int,
        end_time: int
        ):
        params = {
                    "resolution" : 3600, # 1 hour
                    #"resolution" : 864000*2, # For testing
                    "start_time" : int(round(start_time)),
                    "end_time" : int(round(end_time))
                 }
        normalised_hist_cdls = []
        ftx_response = self.get_data(symbol, "candles", params)

        if ftx_response["success"] != "t":
            return normalised_hist_cdls

        '''
        Response format from FTX : https://docs.ftx.com/#get-historical-prices
        https://ftx.us/api/markets/BTC/USD/candles?resolution=1728000&start_time=1651334400000&end_time=1651939200000
        {
          "success": true,
          "result": [
            {
              "close": 11055.25,
              "high": 11089.0,
              "low": 11043.5,
              "open": 11059.25,
              "startTime": "2019-06-24T17:15:00+00:00",
              "time":1584921600000.0,
              "volume": 464193.95725
            }
          ]
        }
        '''

        ftx_hist_cdls = ftx_response["result"]
        for cdl in ftx_hist_cdls:
            print("cdl=%s" % type(cdl))
            print(cdl)

            candle = {}
            candle["time"]      = int(cdl["time"])
            candle["open"]      = float(cdl["open"])
            candle["high"]      = float(cdl["high"])
            candle["low"]       = float(cdl["low"])
            candle["close"]     = float(cdl["close"])
            candle["volume"]    = float(cdl["volume"])
            normalised_hist_cdls.append(candle)

        return normalised_hist_cdls
