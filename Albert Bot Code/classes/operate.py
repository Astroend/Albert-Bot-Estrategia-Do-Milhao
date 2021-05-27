from iqoptionapi.stable_api import IQ_Option
from datetime import  datetime
from time import time, sleep
import os

class Operate():
    def __init__(self, email, password, win_balance, stop_balance, currency, option, favourable, martingale, value, balance_type, return_dict, id):
        self.API = IQ_Option(email, password)
        self.API.connect()
        
        # Trading info
        self.__currency = currency # Current Pair
        self.__favorable = favourable # favourable to majority or minority?
        self.__martingale = martingale # numbers of martingales
        self.__value = value # value of operation
        self.__win_balance = win_balance  # win balance to stop this code
        self.__stop_balance = stop_balance  # stop balance to stop this code
        self.__option = option # binary or digital
        
        self.__balance_type = balance_type # type of balance ( REAL or PRACTICE )
        
        self.return_dict = return_dict # Return variable
        self.id = id # ID of process
        
        self._process()
        
    
    
    def _process(self):
        self.return_dict[self.id] = {'Status': True}
        print('------------  NÃO FECHE ESTE TERMINAL  ------------')
        print(f' Par selecionado: {self.__currency} | {self.__option}\n {self.__martingale} gales\n Valor: {self.__value}\n Stop Win/Loss : {self.__stop_balance} / {self.__win_balance}')
        while True:
            print(' Aviso de funcionamento do Robô')
            self.stop()
            value = self.__value
            if(self.its_time() == True):
                operation_time = time()
                candle = self.next_candle(self.__currency, self.__favorable)
                for trie in range((self.__martingale + 1)):
                    self.stop()
                    print(trie, candle)
                    if candle == None:
                        sleep(60)
                        continue
                    if self.__option == 'BINARY':
                        result = self.buy_binary(value, self.__currency, candle)
                        self.write_doc(f"{datetime.fromtimestamp(operation_time)} | {self.__currency} | Operação: {candle.upper()} | Entrada : {value} | Gale: {trie} |  Resultado : {result} | {self.__balance_type}")
                        if result > 0:
                            sleep(10)
                            break
                        if result < 0:
                            value *= 2.4                         
                    if self.__option == 'DIGITAL':
                        result = self.buy_digital(value, self.__currency, candle)
                        self.write_doc(f"{datetime.fromtimestamp(operation_time)} | {self.__currency} | Operação: {candle.upper()} | Entrada : {value} | Gale: {trie} |  Resultado : {result} | {self.__balance_type}")
                        if result > 0:
                            sleep(10)
                            break    
                        if result < 0:
                            value *= 2.4   
            elif(self.its_time() == 'Ture'):
                return 'Código parado' 
    
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
        else: return None

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
                
    def delay(self):
        return int(self.API.get_server_timestamp() - time())

    def its_time(self):
        delay = self.delay()
        while True:
            date = datetime.fromtimestamp(time() + delay).strftime('%M')[1:]
            if date == '5' or date == '0':
                return True
            
    def stop(self):
        balance = self.API.get_balance()
        if balance >= self.__win_balance or balance <= self.__stop_balance:
            print('Limites foram batidos. Parando o código')
            self.return_dict[self.id] = {'Status': False}
            return exit()
   
    def type(self, balance):
        self.__account_type = balance
        if balance.upper() != 'REAL' or balance.upper() != 'PRACTICE':
            return f'{balance} é inválido.' 
        return self.API.change_balance(balance.upper()) 
    
    def write_doc(self,string):
        while True:
            now = datetime.now()
            file_name = int(datetime(int(now.strftime('%Y')), int(now.strftime('%m')), int(now.strftime('%d'))).timestamp())
            try:
                os.makedirs(f"{os.getenv('APPDATA')}\.Astroend")
                os.makedirs(f"{os.getenv('APPDATA')}\.Astroend/registers")
            except :
                try:
                    file = open(f"'{os.getenv('APPDATA')}/.Astroend/registers/{file_name}.txt'", "x")
                    file.close()
                    with open(f"{os.getenv('APPDATA')}\.Astroend/registers\{file_name}.txt", 'a', encoding='utf-8') as file:
                        file.write(f"Histórico de operações {datetime.fromtimestamp(file_name).strftime('%d/%m/%Y')} \n\n")
                except :
                    with open(f"{os.getenv('APPDATA')}\.Astroend/registers\{file_name}.txt", 'a',encoding='utf-8') as file:
                        file.write(f'{string} \n')
                        return 'Sucefull'