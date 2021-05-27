from multiprocessing import Process
from datetime import datetime
from time import time,sleep

class Graphic():
               
    def stop(self):
        return self.joel.kill()
    
    def candles(self, currency):
        candles = []
        candles.append(self.API.get_candles(currency, 60, 5, time()))
        candles = candles[0]

        for candle in candles:
            candle_index = (candles.index(candle))
            if candle['open'] > candle['close']: candle = 'RED'
            elif candle['open'] < candle['close'] : candle = 'GREEN'
            else : candle = 'DOJI'
            candles[candle_index] = candle
        return candles

    def next_candle(self,currency, favourable):
        candles = self.candles(currency)
        if candles.count('GREEN') > candles.count('RED') and candles.count('DOJI') == 0 : 
           if favourable == 'MAJORITY': return 'call'
           else :return 'put'
        elif candles.count('GREEN') < candles.count('RED') and candles.count('DOJI') == 0 : 
            if favourable == 'MINORITY' :return 'call'
            else :return 'put'
    
    def delay(self):
        return int(self.API.get_server_timestamp() - time())

    def its_time(self):
        delay = self.delay()
        while True:
            if self.check == False:
                return 'Ture'
            date = datetime.fromtimestamp(time() + delay).strftime('%M')[1:]
            if date == '5' or date == '0':
                return True

    def buy_binary(self,value, currency, action):
        print(f'iniciando compra, {value}, {currency}, {action}')
        check, id = self.API.buy(value, currency, action, 1)
        return self.API.check_win_v3(id)
    
    def buy_digital(self, value, currency, action):
        print(f'iniciando compra, {value}, {currency}, {action}')
        id, check = self.API.buy_digital_spot(currency, value, action, 1)
        if check:
            while True:
                status, result = self.API.check_win_digital_v2(id)               
                if status:
                    return result
    @property
    def get_open(self):
        all = (self.API.get_all_open_time())
        return {'Binary': self.specify(all, 'turbo'), 'Digital': self.specify(all, 'digital')}
    
    def specify(self, all, type):
        all_open = []
        for one in all[type]:
            if(all[type][one]['open'] == True):
                all_open.append(one)       
        return all_open  
    
    