from multiprocessing import Process
from classes.account import Account
from classes.graphics import Graphic

from time import sleep

class Main(Account, Graphic):
    def _process(self):
        self.check, status = self.stop()
        while self.check == True:
            print('rodando')
            self.check, status = self.stop()
            if(self.its_time() == True):
                self.check, status = self.stop()
                candle = self.next_candle(self.__exchange, self.__favorable)
                for trie in range((self.__martingale + 1)):
                    print(trie, candle)
                    if self.__option == 'BINARY':
                        result = self.buy_binary((self.__value + (self.__value*trie)), self.__exchange, candle) 
                        if result > 0:
                            break                         
                    if self.__option == 'DIGITAL':
                        if result > 0:
                            break    
                        result = self.buy_digital((self.__value+  (self.__value*trie)), self.__exchange, candle)
            elif(self.its_time() == 'Ture'):
                return ' ' 
        return self.check,status

    def check(self, boolean):
        self.check = boolean
    
    def stop_win(self, num):
        self.__stop_win = num
        self.__stop_win_complete = self.API.get_balance() + num
           
    def stop_loss(self, num):
        self.__stop_loss = num
        self.__stop_loss_complete = self.API.get_balance() - num
    
    def value(self, num):
        self.__value = num
        
    def martingale(self, num):
        self.__martingale = num
        
    def option(self, type):
        self.__option = type
        
    def favourable(self, type):
        self.__favorable = type
        
    def exchange(self, string):
        self.__exchange = string
        
    def _email(self, string):
        self.__email = string
    
    def _password(self, string):
        self.__password = string
    
    @property
    def get_options(self):
        return self.API.get_option_open_by_other_pc()
    
    @property
    def get_stop_loss_complete(self):
        #retorna valor do stop loss + banca (stop = 10 + banca = 100: retorna 90)
        return self.__stop_loss_complete
        
    @property    
    def get_stop_win_complete(self):
        #retorna valor do stop win + banca (win = 10 + banca = 100: retorna 110)
        return self.__stop_win_complete
        
    @property
    def get_api(self):
        return self.API
    
    @property
    def get_stop_win(self):
        #retorna valor do stop win (win = 10 : retorna 10)
        return self.__stop_win
        
    @property
    def get_stop_loss(self):
        #retorna valor do stop loss (loss = 10 : retorna 10)
        return self.__stop_loss
        
    @property
    def get_value(self):
        return self.__value
    
    @property
    def get_martingale(self):
        return self.__martingale
    
    @property
    def get_option(self):
        return self.__option
    
    @property
    def get_favourable(self):
        return self.__favorable
        
    @property
    def get_exchange(self):
        return self.__exchange 
    
    @property
    def get_email(self):
        return self.__email
    
    @property
    def get_password(self):
        return self.__password
    
    def get_time(self):
        return self.API.get_server_timestamp()