# -*- coding: utf-8 -*-
import re
import random
import shutil
import time
import requests
from bs4 import BeautifulSoup
import lxml
import os
import sys
import json
import StandartMethod

class freebitco_checker():


    @staticmethod
    def create_file(create_path: str, cook: str, path: str, balanc, file: str):
        balanc = StandartMethod.StandartMetod.validate(balanc)
        dir_path = create_path + f"\\Balance({balanc}) - System({random.randint(0, 99999)})"
        try:
            os.mkdir(dir_path)
        except OSError as error:
            pass
        data = {
            'Path': path,
            'Cookie': cook,
            'Account Info': {
                'Total-balanc': balanc,
            }
        }
        with open(f'{dir_path}\\MainInfo.json', 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, indent=4, ensure_ascii=False)
        shutil.copy(f'{file}\\{path}', f'{dir_path}\\{path}')


        settings = StandartMethod.headless.get_settings()['Filter_settings']['FreeBitco']
        try:
            os.mkdir(f'{create_path}\\{settings["Full_log"]}')
        except:
            pass
        try:
            os.mkdir(f'{create_path}\\{settings["Balanc_path"]}')
        except:
            pass
        st = ''
        for i in balanc:
            if str(i).isdigit() or str(i) == '.':
                st += i
        path_balanc_log = f'{create_path}\\{settings["Balanc_path"]}\\Balance({balanc}) - System({random.randint(0,99999)})'
        if float(st) >= float(settings['Filter_balanc']):
            try:
                os.mkdir(path_balanc_log)
            except:
                pass
            with open(f'{path_balanc_log}\\MainInfo.json', 'w', encoding='utf-8') as outfile:
                json.dump(data, outfile, indent=4, ensure_ascii=False)
            shutil.copy(f'{file}\\{path}', f'{path_balanc_log}\\{path}')
        shutil.copy(f'{file}\\{path}', f'{create_path}\\{settings["Full_log"]}\\{path}')
    @staticmethod
    def checker(dict, account, path_log, file):
        headers = StandartMethod.StandartMetod.get_headers()
        try:
            cook = {
                "fbtc_session": account['fbtc_session'],
                "fbtc_userid": account['fbtc_userid'],
            }
            req = requests.get('https://freebitco.in/', cookies=cook, headers=headers)

            soup = BeautifulSoup(req.text, 'lxml')
            balanc = soup.find('span', id='balance').text

            log = f'fbtc_session={account["fbtc_session"]}; fbtc_userid={account["fbtc_userid"]}'
            freebitco_checker.create_file(f'{dict}',log, path_log , balanc, file)
        except Exception as ex:
            pass