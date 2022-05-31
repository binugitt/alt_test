import zerorpc
from enum import Enum
from datetime import datetime
from exchange import Exchange
from symbol import Symbol
from md_factory import MDFactory


class MarketData(object):

    def __init__(self):
        self.mdfactory = MDFactory()
        self.xchgs = {}

        # BINU TODO: Exchanges supprted should come from config file
        self.xchgs[Exchange.BINANCE.value] = self.mdfactory.createBinance()

    def get_klines(
        self,
        exchange: Exchange,
        symbol: Symbol,
        start_time: datetime,
        end_time: datetime
        ):

        if exchange not in self.xchgs:
            raise "Unsupported Exchange %s" % exchange

        return self.xchgs[exchange].get_hist_candles(symbol, 
                start_time, end_time)

    def get_order_book(self, exchange: Exchange, symbol: Symbol):
        """
        Returns 20 best bids and 20 best asks
        """
        return self.xchgs[exchange].get_order_book(symbol)

    # For testing only
    def hello(self):
        print ("Got hello request!")
        return "Hello"

    @zerorpc.stream
    def streaming_range(self, fr, to, step):
        return range(fr, to, step)

def main():
    server = zerorpc.Server(MarketData())
    server.bind("tcp://0.0.0.0:1234") # BINU TODO: Port should come from config
    try:
        # Log and restart the server even if error servicing a request
        while True:
            server.run()
    except Exception as e:
        print("An error occurred: %s" % e)

if "__main__" == __name__:
    main()

