from iqoptionapi.stable_api import IQ_Option
from classes.graphics import Graphic

class Account():
    def connect(self, email, senha):
        self._email(email)
        self._password(senha)
        self.API = IQ_Option(email, senha)
        status, message = self.API.connect()
        return status
    
    def type(self, balance):
        self.__account_type = balance
        if balance.upper() != 'REAL' or balance.upper() != 'PRACTICE':
            return f'{balance} é inválido.' 
        return self.API.change_balance(balance.upper())
    
    @property
    def get_type(self):
        return self.__account_type
    
    @property    
    def get_connected(self):
        return self.API.check_connect()
    
    @property
    def get_balance(self):
        return self.API.get_balance()
    
    