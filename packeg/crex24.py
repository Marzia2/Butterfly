# -*- coding: utf-8 -*-
import shutil

import StandartMethod
import re
import random
import time
import requests
from bs4 import BeautifulSoup
import lxml
import os
import sys
import json
class crex24_checker():


    @staticmethod
    def create_file(create_path: str, cook: str, path: str, balanc, file: str):

        balanc = StandartMethod.StandartMetod.validate(balanc)
        dir_path = create_path+f"\\Balance({balanc}) - System({random.randint(0,99999)})"
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

        settings = StandartMethod.headless.get_settings()['Filter_settings']['Crex24']
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
        StandartMethod.StandartMetod.create_file_all_list(f'{dict}')
        cook = {
            "connect.sid": account['connect.sid'],
        }
        req = requests.get('https://crex24.com/ru/account', cookies=cook, headers=headers)
        try:
            soup = BeautifulSoup(req.text, 'lxml')
            balans = soup.find('span', class_='currency--TgdVYHk05X0vANegUL0gu').text

            crex24_checker.create_file(f'{dict}',account['connect.sid'], path_log , balans, file)
        except Exception as ex:
            pass