# BRH BOT

# Extern Funcions

from typing import Text
from iqoptionapi.stable_api import IQ_Option
from PySimpleGUI import PySimpleGUI as sg
from multiprocessing import Process, Manager, freeze_support

# Local Classes

from classes.account import Account
from classes.operate import Operate
from classes.main import Main

# Nuilt-in Functions

from datetime import datetime
from time import time, sleep
import os

# Local Functions

import layouts
import functions

if __name__ == '__main__':
    freeze_support()
    operating_state = False
    link_state = False
    txt_state = False
    account = Main()

    # Process declaration
    
    txt = Process(target=functions.open_txt)  
    
    # Manager of returns
    manager = Manager()
    return_dict = manager.dict()
    jobs = []

    astroend, window_login, pop_up, window_option, window_trading, window_finalize = layouts.window_BRH_BOT(), None, None, None, None, None

    while True:

        window, event, values = sg.read_all_windows(timeout=25)

        if window == BRH BOT and event == sg.WIN_CLOSED:
            break

        if window == BRH BOT and event == 'TERMOS':
            link = Process(target= functions.open_link)
            link.start()
            link_state = True

        if window == BRH BOT and event == 'ACEITO OS TERMOS':
            if link_state == True:
                link.terminate()
            astroend.close()
            window_login = layouts.window_login()

        if window == window_login and event == sg.WIN_CLOSED:
            break

        if window == window_login and event == 'Entrar':

            window_login.close()
            loading = Process(target  = functions.gif)
                
            loading.start()
            if(account.connect(values['login'], values['password'])):
                loading.terminate()
                window_option = layouts.window_option()
            else:
                pop_up = layouts.pop_up()
                loading.terminate()
                window_login = layouts.window_login()

        if window == window_option and event == sg.WIN_CLOSED:
            break

        if window == window_option and event == 'Operate':
            account.type('PRACTICE' if values['account_practice'] else 'REAL')
            account.option('BINARY' if values['option_binary'] else 'DIGITAL')
            account.favourable('MAJORITY' if values['favourable_majority'] else 'MINORITY')
            account.value(float(((str(values['value'])).replace(',','.'))))
            account.stop_win(float(((str(values['stop_win'])).replace(',','.'))))
            account.stop_loss(float((str(values['stop_loss'])).replace(',','.')))
            account.martingale(int(values['martingale']))
            account.exchange(str(values['exchange']).upper())

            window_option.close()
    
            trading_ = Process(target=Operate, args=(account.get_email, 
                account.get_password, account.get_stop_win_complete, account.get_stop_loss_complete, 
                account.get_exchange , account.get_option, account.get_favourable, 
                account.get_martingale, account.get_value, account.get_type, return_dict, 'trading_'))

            trading_.start()
            jobs.append(trading_)
            
            operating_state = True
            window_trading = layouts.window_trading(account.get_type ,account.get_balance ,
                account.get_value, account.get_exchange, account.get_martingale, 
                account.get_option, account.get_favourable, account.get_stop_win_complete,
                account.get_stop_loss_complete)


        if window == window_trading and event == sg.WIN_CLOSED:
            trading_.terminate()
            break
        if operating_state:
            window_trading['-balance-'].update(f"Banca: {account.get_balance}")
            window_trading['-status-'].update('Your Goal Hit' if account.get_balance >= account.get_stop_win_complete else 'Stop Hit' if account.get_balance <= account.get_stop_loss_complete else f'Working ...' if account.get_balance > 0 else 'Sem fundos.')

        if window == window_trading and event == 'Finalize':
            operating_state = False
            print('Mission Completed')
            trading_.terminate()  
            try:
                if not txt_state: 
                    txt.start()
            except: pass
            window_trading.close()
            window_finalize = layouts.window_finalize(account.get_balance)

        if window == window_finalize and event == sg.WIN_CLOSED:
            txt.terminate()
            break

        if window == window_finalize and event == 'Fechar':
            txt.terminate()
            break
            
