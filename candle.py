class Candle:

    def __init__(self, time, open, close, high, low):
        self.__time = time
        self.__open = open
        self.__close = close
        self.__high = high
        self.__low = low

    @property
    def time(self):
        return self.__time

    @property
    def open(self):
        return self.__open

    @property
    def close(self):
        return self.__close

    @property
    def high(self):
        return self.__high

    @property
    def low(self):
        return self.__low

    def __repr__(self):
        return str({'time': self.time, 'open': self.open, 'close': self.close, 'high': self.high, 'low': self.low})
