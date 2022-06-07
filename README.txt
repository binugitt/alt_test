Design:
    Market data can be requested from MktData class. This class will contain
    instances of all supported exchanges. It creates them using a factory(MDFactory).
    The aim is to provide this data in a normalised form to clients of this class.
    Normalised form should be a class but zerorpc uses msgpack and that needs only
    basic types, but we can look for enhancing this or even can be a pandas dataframe perhaps.

    Currently using zerorpc for communication across services, but ideally we
    should have a wrapper around so that we can change the underlying middleware
    without having to change application code.

    Note that the whole design is based on web urls and not websockets. The design would
    change a lot when going for that which is what should be done ideally. So the
    clients to mkt data will have to be in accordance with this streaming data
    as well. We would need subscribe/unsubscribe mechanisms implemented with caching
    and proper book building in the MktData class(each exchange will have its current
    orderbook etc for example.

    Mysql client will connect to MktData and pull data for 5 mins and write to DB.
    It waits for mkt data service to be up prior to doing so. Once connected,
    it will create OrderBook table if not already there and write to that.
    Have created a grafana dashboard for (bid+ask)/2 plot - the data is fetched from mysql
    Have created candlesticks plot using
        1) mplfinance(file:jupyter/notebooks/plot_candles_using_mplfinance.ipynb)
        2) plotly(file:jupyter/notebooks/plot_candles_using_plotly.ipynb)

    Both Orderbook and Historical candles are implemented for both Binance and FTX.
    FTX did not work with "requests" package and had to use curl directly

    TODO:
    1) The pre-init of sql server with tables pre-created. This did not work due to 
       permission issues.
    2) Tidy up of the entire code base

DB: MySQL
    DB: TestDB
    Table:
        OrderBook:
        +------------+-------------+------+-----+---------+-------+
        | Field      | Type        | Null | Key | Default | Extra |
        +------------+-------------+------+-----+---------+-------+
        | time       | timestamp   | YES  |     | NULL    |       |
        | symbol     | varchar(50) | YES  |     | NULL    |       |
        | ecn        | varchar(20) | YES  |     | NULL    |       |
        | ecn_symbol | varchar(50) | YES  |     | NULL    |       |
        | level      | int         | YES  |     | NULL    |       |
        | bid_price  | double      | YES  |     | NULL    |       |
        | bid_qty    | double      | YES  |     | NULL    |       |
        | ask_price  | double      | YES  |     | NULL    |       |
        | ask_qty    | double      | YES  |     | NULL    |       |
        +------------+-------------+------+-----+---------+-------+

    Grafana dashboard query:
        SELECT
          time AS "time",
          (bid_price + ask_price)/2
        FROM OrderBook
        WHERE
          level = 1
          and ecn = "BINANCE"
          and symbol = "BTCUSDT"
        ORDER BY time

Build:
    From root folder(altonomy_test):
    docker compose build

Run:
    From root folder(altonomy_test):
    docker compose up


Confession:
    The whole thing was a new concept for me starting from docker! Even python I have
    not used to the level as the main application(used it only as side application).
    This is caused me to take more time.
