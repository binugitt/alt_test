from binance_req_resp import Binance
from datetime import datetime


def main():
    xchg = Binance()
    #book = xchg.get_order_book(0)
    #print(book)
    hist_cdls = xchg.get_hist_candles(0, start_time = datetime.fromisoformat('2022-05-01'), end_time = datetime.fromisoformat('2022-05-08'))
    print(hist_cdls)

if "__main__" == __name__:
    main()

