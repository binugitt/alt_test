from binance_req_resp import Binance
from ftx_req_resp import FTX
from datetime import datetime
import time


def main():
    xchg = Binance()
    #xchg = FTX()
    while True:
        print("=======================================================================")
        print("=======================================================================")
        print("=======================================================================")

        book = xchg.get_order_book(0, 5)
        print(book)
        time.sleep(1)

    #hist_cdls = xchg.get_hist_candles(0, start_time = datetime.fromisoformat('2022-05-01'), end_time = datetime.fromisoformat('2022-05-08'))
    #print(hist_cdls)

if "__main__" == __name__:
    main()

