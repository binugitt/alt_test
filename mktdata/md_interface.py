import requests
from datetime import datetime
from symbol import Symbol
from dataclasses import dataclass


class MDExchange:
    
    def get_historical_candles(
        self,
        symbol: Symbol,
        start_time: datetime,
        end_time: datetime
        ):
        raise Exception("Not Implemented")
    
    # Normalised OrderBook Data
    # BINU TODO Unforuntaely zerorpc does not supprt custom objects! so will go with a simple dict
    @dataclass
    class OrderBookData:
        timestamp: str # As string since zerorpc doesnt serialise! BINU TODO: FIX this - Need a wrapper around zerorpc or any middleware we use
        symbol: str
        ecn: str
        ecn_symbol: str
        bids: dict
        asks: dict

    # Will return the normalised orderbook
    def get_order_book(self, symbol: Symbol, depth: int):
        raise Exception("Not Implemented")


