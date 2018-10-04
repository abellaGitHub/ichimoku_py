import logging
import time
import sys

from binance.client import Client
from binance.websockets import BinanceSocketManager
from binance.enums import *

from ichimoku import Ichimoku
from candle import Candle

symbols = ['BTCUSDT']
candles = {}
ichimoku = {}

client = Client('', '')
bsm = BinanceSocketManager(client)

for symbol in symbols:
    klines = client.get_klines(symbol=symbol, interval=KLINE_INTERVAL_1MINUTE)
    candles[symbol] = list(
        map(
            lambda candle: Candle(candle[0], float(candle[1]), float(candle[4]), float(candle[2]), float(candle[3])),
            klines[len(klines) - 53:]
        )
    )

    # print(candles[symbol])
    ichimoku[symbol] = Ichimoku(candles[symbol][:-1])
    print('RESULT')
    print(ichimoku[symbol].result)


def handle_message(msg):
    if msg['e'] == 'error':
        print(str(msg))
    elif msg['e'] == 'kline':
        kline = msg['k']
        handle_new_candle(
            msg['s'],
            Candle(kline['t'], float(kline['o']), float(kline['c']), float(kline['h']), float(kline['l']))
        )


def handle_new_candle(symbol, new_candle):
    last_candle = candles[symbol][-1]

    if new_candle.time > last_candle.time:
        print('NEXT_RESULT')
        print(ichimoku[symbol].next_result(last_candle))
        print('APPEND')
        candles[symbol].append(new_candle)
    elif new_candle.time == last_candle.time:
        print('UPDATE')
        candles[symbol][-1] = new_candle

    print(new_candle)


bsm.start_kline_socket('BTCUSDT', handle_message, interval=KLINE_INTERVAL_1MINUTE)
bsm.start()
