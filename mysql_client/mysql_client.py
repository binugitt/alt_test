import zerorpc
from exchange import Exchange
from symbol import Symbol
from datetime import datetime
import mysql.connector
import time
import itertools



# Application to pull mktdata(order book) and write to MySQL DB

class MktDataDBWriter:
    def connect_mktdata_server(self):
        # connect to mkt data server
        self.md_client = zerorpc.Client()
        #self.md_client.connect("tcp://mktdata:1234")
        self.md_client.connect("tcp://127.0.0.1:1234")
        print("Connection established")


    def connect_db(self):
        self.mydb = mysql.connector.connect(
          host="localhost",
          user="root",
          password="password",
          database="TestDB"
        )
        print(self.mydb)

    def init_db(self):
        # Create table for OrderBook if not present
        mycursor = self.mydb.cursor()
        mycursor.execute("CREATE TABLE IF NOT EXISTS OrderBook ( \
                time TIMESTAMP, \
                symbol VARCHAR(50), \
                ecn VARCHAR(20), \
                ecn_symbol VARCHAR(50), \
                level INT, \
                bid_price DOUBLE, \
                bid_qty DOUBLE, \
                ask_price DOUBLE, \
                ask_qty DOUBLE \
                )")


    # Pull mktdata(order book) and write to DB
    def md_pull_n_write(self):
        try:
            # Test
            #print(self.md_client.hello())

            #print(self.md_client.get_order_book(9, Symbol.BTCUSDT.value)) # Should produce exception
            #print(self.md_client.get_order_book(Exchange.BINANCE.value, Symbol.BTCUSDT.value))
            normalised_ob = self.md_client.get_order_book(Exchange.BINANCE.value, Symbol.BTCUSDT.value)
            #print("normalised_ob=%s" % type(normalised_ob))
            #print("normalised_ob['bids']=%s" % type(normalised_ob['bids']))
            #print(normalised_ob)

            sql = "INSERT INTO OrderBook (time, symbol, ecn, ecn_symbol, level, bid_price, bid_qty, ask_price, ask_qty) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            vals = []
            level = 1;
            print("Levels:")
            #for item in normalised_ob['bids']:
            #for (bid,ask) in itertools.zip_longest(list01, list02): BINU TODO: Use this to be able to take in missing bids/asks!
            for (bid,ask) in zip(normalised_ob['bids'], normalised_ob['asks']):
                print (bid,ask)
                #print(item)
                #print("Types: symbol=%s item=%s" % type(normalised_ob['symbol']), type(item))
                vals.append((
                    datetime.strptime(normalised_ob['timestamp'], "%d-%m-%Y, %H:%M:%S"),
                    normalised_ob['symbol'],
                    normalised_ob['ecn'],
                    normalised_ob['ecn_symbol'],
                    level,
                    bid[0],
                    bid[1],
                    ask[0],
                    ask[1]))
                level = level+1


            '''
            print("ASKS:")
            level = 1;
            for item in normalised_ob['asks']:
                print(item)
                #print("normalised_ob['symbol']=%s" % type(normalised_ob['symbol']))
                vals.append((
                    #datetime.strptime(normalised_ob['timestamp'][0]+' '+normalised_ob['timestamp'][1], "%d-%m-%Y, %H:%M:%S"),
                    #datetime.strptime(normalised_ob['timestamp'][0], "%d-%m-%Y, %H:%M:%S"),
                    datetime.strptime(normalised_ob['timestamp'], "%d-%m-%Y, %H:%M:%S"),
                    normalised_ob['symbol'],
                    normalised_ob['ecn'],
                    normalised_ob['ecn_symbol'],
                    "A",
                    level,
                    item[0],
                    item[1]))
                level = level+1

            print(vals)
            for item in vals:
                print(item)
            print(normalised_ob['bids'])
            print(normalised_ob['asks'])
            print("reached here")
            '''

            mycursor = self.mydb.cursor()
            mycursor.executemany(sql, vals)
            self.mydb.commit()
            print(mycursor.rowcount, "record inserted.")

            #for item in self.md_client.streaming_range(10, 20, 2):
                #print(item)
        except Exception as e:
            print("An error occurred: %s" % e)


        '''
        from datetime import datetime

        #sql = "INSERT INTO OrderBook (time, symbol, ecn, ecn_symbol, side, level, price, qty) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        sql = "INSERT INTO OrderBook (time, symbol, ecn, ecn_symbol, level, bid_price, bid_qty, ask_price, ask_qty) VALUES (%s, %s, %s, %s, %s, %s, %s, %s %s)"
        val = (datetime.now(), "BTCUSDT", "Binance", "BTCUSDT", 1, 31677.96000000, 5.21776000, 31677.96000000, 5.21776000)
        mycursor.execute(sql, val)
        vals = [
                (datetime.now(), "BTCUSDT", "Binance", "BTCUSDT", 1, 31677.96000000, 5.21776000, 31677.96000000, 5.21776000),
                (datetime.now(), "BTCUSDT", "Binance", "BTCUSDT", 1, 31677.96000000, 5.21776000, 31677.96000000, 5.21776000)
                #(datetime.now(), "BTCUSDT", "Binance", "BTCUSDT", "B", 1, 31677.96000000, 5.21776000),
                #(datetime.now(), "BTCUSDT", "Binance", "BTCUSDT", "B", 2, 31677.96000000, 5.21776000)
              ]
        mycursor.executemany(sql, vals)

        self.mydb.commit()

        print(mycursor.rowcount, "record inserted.")
        '''

    # Pull historical candles for testing
    def cdls_pull(self):
        try:
            # Test
            #print(self.md_client.hello())

            #print("normalised_ob=%s" % type(normalised_ob))
            #print("normalised_ob['bids']=%s" % type(normalised_ob['bids']))
            #print(normalised_ob)

            normalised_ob = self.md_client.get_order_book(Exchange.BINANCE.value, Symbol.BTCUSDT.value)
            hist_cdls = self.md_client.get_historical_candles(Exchange.BINANCE.value, Symbol.BTCUSDT.value,
                    #datetime.fromisoformat('2022-05-01'), datetime.fromisoformat('2022-05-08'))
                    int(round(datetime.timestamp(datetime.fromisoformat('2022-05-01'))*1000)), 
                    int(round(datetime.timestamp(datetime.fromisoformat('2022-05-08'))*1000)))
            print(hist_cdls)
        except Exception as e:
            print("An error occurred: %s" % e)

def main():
    try:
        # Wait for a while till mysql server is up
        time.sleep(2)

        md_writer = MktDataDBWriter()
        md_writer.connect_mktdata_server()
        md_writer.connect_db()
        md_writer.init_db()

        # Poll mkt data every sec for 5 mins and write to DB
        cnt = 1
        while cnt <= 300:
            md_writer.md_pull_n_write()
            time.sleep(1)
            cnt = cnt + 1

        # Test candles
        #md_writer.cdls_pull()

    except Exception as e:
        print("An error occurred: %s" % e)

if "__main__" == __name__:
    main()

