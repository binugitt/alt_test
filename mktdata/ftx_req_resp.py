import requests
from datetime import datetime
from collections import defaultdict

from symbol import Symbol
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
        data = os.popen(cmd).read()
        print(data)

        return data

    def get_order_book(self, sym: Symbol, depth: int):
        params = {
                    "depth" : depth,
                 }
        ftx_ob = self.get_data(sym, "orderbook", params)

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
        ):
        params = {
                    "resolution" : 3600, # 1 hour
                    #"resolution" : 864000*2, # For testing
                    "start_time" : int(round(start_time)),
                    "end_time" : int(round(end_time))
                 }
        ftx_response_str = self.get_data(symbol, "candles", params)
        #print(ftx_response_str)
        #print(type(ftx_response_str))
        length = 12
        #print(ftx_response_str[length-1])
        normalised_hist_cdls = []

        # The response is broken: "success":true
        # So need to remove this part from the string prior to converting to dict
        if ftx_response_str[length-1] == 't':
            print("TRUE")
            length = length + 5
        else:
            length = length + 6
            return normalised_hist_cdls

        ftx_response_str = '{' + ftx_response_str[length-1:]
        print(ftx_response_str)

        #ftx_response_str = '{"success":"true"}'
        #ftx_response_str = '{"success":"true","result":[{"startTime":"2020-03-23T00:00:00+00:00","time":1584921600000.0,"open":6350.0,"high":6873.0,"low":6030.25,"close":6253.75,"volume":0.0}]}'
        #ftx_response_str = '{"success":true,"result":[{"startTime":"2020-03-23T00:00:00+00:00","time":1584921600000.0,"open":6350.0,"high":6873.0,"low":6030.25,"close":6253.75,"volume":0.0},{"startTime":"2020-03-29T00:00:00+00:00","time":1585440000000.0,"open":6253.75,"high":7471.0,"low":5860.0,"close":7034.5,"volume":0.0},{"startTime":"2020-04-18T00:00:00+00:00","time":1587168000000.0,"open":7034.5,"high":10070.5,"low":6757.0,"close":9998.5,"volume":0.0},{"startTime":"2020-05-08T00:00:00+00:00","time":1588896000000.0,"open":9998.5,"high":10048.5,"low":8093.0,"close":9579.5,"volume":0.0},{"startTime":"2020-05-29T00:00:00+00:00","time":1590710400000.0,"open":9579.5,"high":10416.5,"low":8892.0,"close":9456.5,"volume":0.0},{"startTime":"2020-06-18T00:00:00+00:00","time":1592438400000.0,"open":9456.5,"high":9794.0,"low":8826.5,"close":9259.0,"volume":0.0},{"startTime":"2020-07-08T00:00:00+00:00","time":1594166400000.0,"open":9259.0,"high":11424.0,"low":9033.5,"close":11052.0,"volume":0.0},{"startTime":"2020-07-28T00:00:00+00:00","time":1595894400000.0,"open":11055.5,"high":12112.0,"low":10581.0,"close":11916.5,"volume":0.0},{"startTime":"2020-08-17T00:00:00+00:00","time":1597622400000.0,"open":11916.5,"high":12486.0,"low":9863.5,"close":10164.5,"volume":0.0},{"startTime":"2020-09-06T00:00:00+00:00","time":1599350400000.0,"open":10164.5,"high":11185.5,"low":9843.5,"close":10693.0,"volume":0.0},{"startTime":"2020-09-26T00:00:00+00:00","time":1601078400000.0,"open":10693.0,"high":11729.5,"low":10378.0,"close":11508.5,"volume":0.0},{"startTime":"2020-10-16T00:00:00+00:00","time":1602806400000.0,"open":11508.0,"high":14278.0,"low":11212.5,"close":14161.5,"volume":0.0},{"startTime":"2020-11-05T00:00:00+00:00","time":1604534400000.0,"open":14161.0,"high":19432.5,"low":14113.0,"close":19169.5,"volume":0.0},{"startTime":"2020-11-25T00:00:00+00:00","time":1606262400000.0,"open":19169.5,"high":20088.0,"low":16233.0,"close":19272.5,"volume":0.0},{"startTime":"2020-12-15T00:00:00+00:00","time":1607990400000.0,"open":19272.5,"high":34833.5,"low":19041.0,"close":33065.0,"volume":0.0},{"startTime":"2021-01-04T00:00:00+00:00","time":1609718400000.0,"open":33062.5,"high":41990.5,"low":27762.5,"close":32090.0,"volume":0.0},{"startTime":"2021-01-24T00:00:00+00:00","time":1611446400000.0,"open":32090.0,"high":49053.0,"low":29250.0,"close":47407.0,"volume":0.0},{"startTime":"2021-02-13T00:00:00+00:00","time":1613174400000.0,"open":47407.0,"high":58335.0,"low":43003.0,"close":48373.0,"volume":0.0},{"startTime":"2021-03-05T00:00:00+00:00","time":1614902400000.0,"open":48373.0,"high":61810.0,"low":46276.0,"close":52307.0,"volume":0.0},{"startTime":"2021-03-25T00:00:00+00:00","time":1616630400000.0,"open":52307.0,"high":63782.0,"low":50419.0,"close":63593.0,"volume":0.0},{"startTime":"2021-04-14T00:00:00+00:00","time":1618358400000.0,"open":63593.0,"high":64945.0,"low":47005.0,"close":57169.0,"volume":0.0},{"startTime":"2021-05-04T00:00:00+00:00","time":1620086400000.0,"open":57202.0,"high":59627.0,"low":29325.0,"close":34714.0,"volume":0.0},{"startTime":"2021-05-24T00:00:00+00:00","time":1621814400000.0,"open":34717.0,"high":40887.0,"low":31021.0,"close":35527.0,"volume":0.0},{"startTime":"2021-06-13T00:00:00+00:00","time":1623542400000.0,"open":35496.0,"high":41320.0,"low":28829.0,"close":33803.0,"volume":0.0},{"startTime":"2021-07-03T00:00:00+00:00","time":1625270400000.0,"open":33803.0,"high":35979.0,"low":29300.0,"close":32295.0,"volume":0.0},{"startTime":"2021-07-23T00:00:00+00:00","time":1626998400000.0,"open":32295.0,"high":46753.0,"low":32005.0,"close":45551.0,"volume":0.0},{"startTime":"2021-08-12T00:00:00+00:00","time":1628726400000.0,"open":45551.0,"high":50537.0,"low":43800.0,"close":47121.0,"volume":0.0},{"startTime":"2021-09-01T00:00:00+00:00","time":1630454400000.0,"open":47121.0,"high":52948.0,"low":42267.0,"close":42992.0,"volume":0.0},{"startTime":"2021-09-21T00:00:00+00:00","time":1632182400000.0,"open":42992.0,"high":56633.0,"low":39544.0,"close":54688.0,"volume":0.0},{"startTime":"2021-10-11T00:00:00+00:00","time":1633910400000.0,"open":54686.0,"high":67033.0,"low":51410.0,"close":61890.0,"volume":0.0},{"startTime":"2021-10-31T00:00:00+00:00","time":1635638400000.0,"open":61890.0,"high":69045.0,"low":55611.0,"close":58112.0,"volume":0.0},{"startTime":"2021-11-20T00:00:00+00:00","time":1637366400000.0,"open":58108.0,"high":60054.0,"low":40301.0,"close":47554.0,"volume":0.0},{"startTime":"2021-12-10T00:00:00+00:00","time":1639094400000.0,"open":47554.0,"high":52069.0,"low":45456.0,"close":46460.0,"volume":0.0},{"startTime":"2021-12-30T00:00:00+00:00","time":1640822400000.0,"open":46460.0,"high":48571.0,"low":39661.0,"close":42366.0,"volume":0.0},{"startTime":"2022-01-19T00:00:00+00:00","time":1642550400000.0,"open":42366.0,"high":44528.0,"low":32856.0,"close":43879.0,"volume":0.0},{"startTime":"2022-02-08T00:00:00+00:00","time":1644278400000.0,"open":43879.0,"high":45867.0,"low":34333.0,"close":37705.0,"volume":0.0},{"startTime":"2022-02-28T00:00:00+00:00","time":1646006400000.0,"open":37705.0,"high":45343.0,"low":37167.0,"close":42229.0,"volume":0.0},{"startTime":"2022-03-20T00:00:00+00:00","time":1647734400000.0,"open":42229.0,"high":48220.0,"low":40486.0,"close":42257.0,"volume":0.0},{"startTime":"2022-04-09T00:00:00+00:00","time":1649462400000.0,"open":42257.0,"high":43435.0,"low":37711.0,"close":39745.0,"volume":0.0},{"startTime":"2022-04-29T00:00:00+00:00","time":1651190400000.0,"open":39745.0,"high":40066.0,"low":25358.0,"close":28662.0,"volume":0.0},{"startTime":"2022-05-19T00:00:00+00:00","time":1652918400000.0,"open":28662.0,"high":32389.0,"low":28001.0,"close":29841.0,"volume":0.0}]}'


        #ftx_response = json.dumps(ftx_response_str)
        ftx_response = ast.literal_eval(ftx_response_str)
        print(type(ftx_response))

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
