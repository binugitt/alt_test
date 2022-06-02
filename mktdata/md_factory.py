from binance_req_resp import Binance
from ftx_req_resp import FTX

# Add all exchanges to be supported here
class MDFactory(object):

    def createBinance(self):
        xchg = Binance()
        return xchg

    def createFTX(self):
        xchg = FTX()
        return xchg

