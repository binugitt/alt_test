import zerorpc
from exchange import Exchange
from symbol import Symbol


c = zerorpc.Client()
#c.connect("tcp://mktdata:1234")
c.connect("tcp://127.0.0.1:1234")
print("Connection established")

try:
    print(c.hello())

    #print(c.get_order_book(9, Symbol.BTCUSDT.value)) # Should produce exception
    print(c.get_order_book(Exchange.BINANCE.value, Symbol.BTCUSDT.value))

    for item in c.streaming_range(10, 20, 2):
        print(item)
except Exception as e:
    print("An error occurred: %s" % e)
