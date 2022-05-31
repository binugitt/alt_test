from binance_req_resp import Binance

# Add all exchanges to be supported here
class MDFactory(object):

    def createBinance(self):
        self.binance_xchg = Binance()
        return self.binance_xchg

