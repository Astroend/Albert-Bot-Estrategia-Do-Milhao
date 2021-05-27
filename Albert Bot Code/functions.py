from iqoptionapi.stable_api import IQ_Option
from datetime import datetime
from time import time, sleep
import os

import layouts
import variables

def gif():
    window = layouts.window_loading()

    while True:
        event = window.Read(timeout=25)
        if event in (None, ''):
            break
        window.Element('_IMAGE_').UpdateAnimation(variables.gif,  time_between_frames=50)

def open_txt():
    now = datetime.now()
    file_name = int(datetime(int(now.strftime('%Y')), int(now.strftime('%m')), int(now.strftime('%d'))).timestamp())
    os.system(f'''"{os.getenv('APPDATA')}\.Astroend/registers\{file_name}.txt"''')

def open_link():
    os.system('start www.astroend.xyz/termos.html')