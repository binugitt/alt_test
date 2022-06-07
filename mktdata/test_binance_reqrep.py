from binance_req_resp import Binance
from ftx_req_resp import FTX
from datetime import datetime
import time
import zerorpc

# NOTE: To make this run directly(without docker) just copy the files
# from common folder into mkdata folder

def test_direct():
    #xchg = Binance()
    xchg = FTX()
    hist_cdls = xchg.get_historical_candles(0, 
            start_time = datetime.timestamp(datetime.fromisoformat('2022-05-01'))*1000, 
            end_time = datetime.timestamp(datetime.fromisoformat('2022-05-08'))*1000)
            #start_time = datetime.fromisoformat('2022-05-01'), 
            #end_time = datetime.fromisoformat('2022-05-08'))
    print(hist_cdls)
    #return

    while True:
        print("=======================================================================")
        print("=======================================================================")
        print("=======================================================================")

        book = xchg.get_order_book(0, 5)
        print(book)
        time.sleep(1)

def test_via_zerorpc():
    md_client = zerorpc.Client()
    md_client.connect("tcp://127.0.0.1:1234")
    print("Connection established")

    #print(md_client.hello())
    print((datetime.timestamp(datetime.fromisoformat('2022-05-01'))*1000))
    print((datetime.timestamp(datetime.fromisoformat('2022-05-08'))*1000))
    hist_cdls = md_client.get_historical_candles(0, 0,
            #1651334400000, 1651939200000)
            int(round(datetime.timestamp(datetime.fromisoformat('2022-05-01'))*1000)), 
            int(round(datetime.timestamp(datetime.fromisoformat('2022-05-08'))*1000)))
            #start_time = datetime.fromisoformat('2022-05-01'), 
            #end_time = datetime.fromisoformat('2022-05-08'))
    print(hist_cdls)

def main():
    test_direct()
    #test_via_zerorpc()

if "__main__" == __name__:
    main()

