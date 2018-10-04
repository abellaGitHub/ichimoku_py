

class Ichimoku:

    def __init__(self, candles, tenkan=9, kijun=26, senkou_b=52, displacement=26):
        self.__config = {'tenkan': tenkan, 'kijun': kijun, 'senkou_b': senkou_b, 'displacement': displacement}
        self.__candles = list(candles)
        self.__result = Ichimoku.calculate(candles, tenkan, kijun, senkou_b)

    @staticmethod
    def calculate_ichimoku_line(candles, period):
        result = []
        for i in range(0, len(candles) - period + 1):
            period_candles = candles[i: i + period]
            result.append(
                (min(candle.low for candle in period_candles) + max(candle.high for candle in period_candles)) / 2
            )
        return result

    @staticmethod
    def calculate(candles, tenkan=9, kijun=26, senkou_b=52):
        result = {
            'tenkan': Ichimoku.calculate_ichimoku_line(candles, tenkan),
            'kijun': Ichimoku.calculate_ichimoku_line(candles, kijun),
            'senkou_a': [],
            'senkou_b': Ichimoku.calculate_ichimoku_line(candles, senkou_b)
        }

        # senkou_a
        for i in range(0, len(result['kijun'])):
            result['senkou_a'].append(
                (result['tenkan'][i - len(result['kijun'])] + result['kijun'][i - len(result['kijun'])]) / 2
            )

        return result

    @property
    def result(self):
        return self.__result

    def result_by_index_with_displacement(self, index):
        return {
            'tenkan': self.result['tenkan'][index],
            'kijun': self.result['kijun'][index],
            'senkou_a': self.result['senkou_a'][index - self.__config['displacement']],
            'senkou_b': self.result['senkou_b'][index - self.__config['displacement']]
        }

    def next_result(self, candle):
        self.__candles.append(candle)
        result = {
            'tenkan': Ichimoku.calculate_ichimoku_line(self.__candles[-self.__config['tenkan']:], self.__config['tenkan']).pop(),
            'kijun': Ichimoku.calculate_ichimoku_line(self.__candles[-self.__config['kijun']:], self.__config['kijun']).pop(),
            'senkou_b': Ichimoku.calculate_ichimoku_line(self.__candles[-self.__config['senkou_b']:], self.__config['senkou_b']).pop()
        }
        result['senkou_a'] = (result['tenkan'] + result['kijun']) / 2

        self.__result['tenkan'].append(result['tenkan'])
        self.__result['kijun'].append(result['kijun'])
        self.__result['senkou_a'].append(result['senkou_a'])
        self.__result['senkou_b'].append(result['senkou_b'])

        return result

    def check_signals(self):
        prev_res = self.result_by_index_with_displacement(-2)
        curr_res = self.result_by_index_with_displacement(-1)

        prev_candle = self.__candles[-2]
        curr_candle = self.__candles[-1]
